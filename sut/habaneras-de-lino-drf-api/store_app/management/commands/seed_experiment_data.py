from decimal import Decimal
import datetime

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from store_app.models import (
    Cart,
    Category,
    ClothingCollection,
    ClothingProduct,
    ClothingProductImage,
    CustomColor,
    GlobalModel,
    ProductVariation,
)


SMALL_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!"
    b"\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00"
    b"\x00\x02\x02D\x01\x00;"
)


class Command(BaseCommand):
    help = "Seed deterministic data for Assignment 3 performance and chaos experiments."

    def add_arguments(self, parser):
        parser.add_argument("--products", type=int, default=120)
        parser.add_argument("--carts", type=int, default=20)
        parser.add_argument("--admin-user", default="admin")
        parser.add_argument("--admin-password", default="admin1234")

    def handle(self, *args, **options):
        product_count = options["products"]
        cart_count = options["carts"]

        GlobalModel.objects.update(active=False)
        seed_date = datetime.date(2026, 4, 24)
        global_model = GlobalModel.objects.filter(last_updated=seed_date).first()
        if global_model is None:
            global_model = GlobalModel(last_updated=seed_date)
        global_model.active = True
        global_model.mx_value = Decimal("18.0000")
        global_model.us_sales_taxes = Decimal("0.0700")
        global_model.save()

        colors = []
        color_values = [
            ("A3 Black", "#000000"),
            ("A3 White", "#FFFFFF"),
            ("A3 Navy", "#001F5B"),
            ("A3 Olive", "#556B2F"),
            ("A3 Sand", "#D6C2A1"),
            ("A3 Rose", "#C08081"),
            ("A3 Sky", "#87CEEB"),
            ("A3 Linen", "#FAF0E6"),
        ]
        for nickname, code in color_values:
            color, _ = CustomColor.objects.update_or_create(
                nickname=nickname,
                defaults={"code": code},
            )
            colors.append(color)

        collections = []
        for index in range(1, 6):
            collection, _ = ClothingCollection.objects.update_or_create(
                title=f"A3 Collection {index}",
                year=str(2020 + index),
                defaults={"description": f"Assignment 3 seeded collection {index}"},
            )
            self._ensure_image(collection.image, f"a3_collection_{index}.gif")
            collection.save()
            collections.append(collection)

        categories = []
        for index in range(1, 11):
            category, _ = Category.objects.update_or_create(
                title=f"A3 Category {index}",
                defaults={"description": f"Assignment 3 seeded category {index}"},
            )
            self._ensure_image(category.image, f"a3_category_{index}.gif")
            category.save()
            categories.append(category)

        products = []
        for index in range(1, product_count + 1):
            product, _ = ClothingProduct.objects.update_or_create(
                name=f"A3 Product {index:03d}",
                defaults={
                    "code": f"A3P{index:03d}",
                    "tag": ["SHIRT", "PANTS", "DRESS"][index % 3],
                    "base_pricing": Decimal("20.0000") + Decimal(index % 45),
                    "production_cost": Decimal("8.0000") + Decimal(index % 20),
                    "amount_sold": index % 17,
                },
            )
            product.collections.set(collections[index % len(collections):(index % len(collections)) + 1] or collections[:1])
            product.categories.set(categories[index % len(categories):(index % len(categories)) + 1] or categories[:1])
            product.available_colors.set(colors[: min(4, len(colors))])
            self._ensure_product_images(product, index)
            products.append(product)

        for index in range(1, cart_count + 1):
            cart, _ = Cart.objects.update_or_create(
                token=f"a3-cart-token-{index:03d}",
                defaults={"ip_address": f"10.0.3.{index}", "is_active": True},
            )
            product = products[index % len(products)]
            ProductVariation.objects.get_or_create(
                product=product,
                principal_color=colors[index % len(colors)],
                size="M",
                sleeve="None",
                quantity=(index % 3) + 1,
                cart=cart,
            )

        self._ensure_admin(options["admin_user"], options["admin_password"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded Assignment 3 data: {len(products)} products, "
                f"{len(categories)} categories, {len(collections)} collections, "
                f"{cart_count} carts."
            )
        )

    def _ensure_image(self, image_field, filename):
        if not image_field:
            image_field.save(filename, ContentFile(SMALL_GIF), save=False)

    def _ensure_product_images(self, product, index):
        for image_type in ("PRIMARY", "SECONDARY", "EXTRA"):
            image, _ = ClothingProductImage.objects.get_or_create(
                product=product,
                type_of_image=image_type,
            )
            if not image.image:
                image.image.save(
                    f"a3_product_{index:03d}_{image_type.lower()}.gif",
                    ContentFile(SMALL_GIF),
                    save=True,
                )

    def _ensure_admin(self, username, password):
        User = get_user_model()
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={"email": f"{username}@example.com"},
        )
        user.email = f"{username}@example.com"
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()
