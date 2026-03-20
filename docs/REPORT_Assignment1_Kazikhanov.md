# Отчёт по Assignment 1
## Quality Assurance: Risk Assessment & Environment Setup

---

**Студент:** Казиханов Диас
**Группа:** CSE-2506M
**Дата:** март 2026

---

## Содержание

1. Введение
2. Описание тестируемой системы
3. Анализ рисков
4. Стратегия тестирования
5. Настройка окружения
6. Написанные тесты
7. CI/CD Pipeline
8. Базовые метрики
9. Выводы
10. Приложения

---

## 1. Введение

В рамках первого задания по курсу Quality Assurance была выполнена работа по анализу рисков и настройке тестового окружения для выбранной системы.

Цели работы:
- Изучить разницу между QA и QC
- Определить критичные компоненты системы
- Настроить инструменты для тестирования
- Создать CI/CD pipeline
- Задокументировать процесс

---

## 2. Описание тестируемой системы

Для тестирования была выбрана система **Habaneras de Lino** — это REST API для интернет-магазина одежды.

Репозиторий: https://github.com/Ceci-Aguilera/habaneras-de-lino-drf-api

### Технологии

| Компонент | Технология |
|-----------|-----------|
| Backend | Django 4.0.6 |
| API | Django REST Framework 3.13.1 |
| База данных | PostgreSQL 13 |
| Контейнеризация | Docker, Docker Compose |
| Web-сервер | Nginx |
| Платежи | Stripe |
| Изображения | Cloudinary |

### Основные функции системы

- Каталог товаров с категориями и коллекциями
- Корзина покупок (по токену)
- Оформление заказов
- Обработка платежей через Stripe
- Админ-панель для управления магазином

---

## 3. Анализ рисков

### Методология

Для оценки рисков использовалась формула:

**Risk Score = Вероятность отказа x Влияние отказа**

Каждый параметр оценивается по шкале от 1 до 5.

### Выявленные модули

В системе было выделено 10 основных модулей:

| # | Модуль | Описание |
|---|--------|----------|
| M1 | Order & Checkout | Создание заказа, связь с корзиной и оплатой |
| M2 | Stripe Payment | Обработка платежей |
| M3 | Cart Management | Управление корзиной |
| M4 | Product Catalog | Список и детали товаров |
| M5 | Collections API | Коллекции и категории |
| M6 | Data Validation | Валидация входных данных |
| M7 | Admin Panel | Панель администратора |
| M8 | Tax Calculation | Расчёт налогов и цен |
| M9 | Image Upload | Загрузка изображений |
| M10 | Infrastructure | Docker и Nginx |

### Матрица рисков

| Модуль | Вероятность | Влияние | Score | Приоритет |
|--------|-------------|---------|-------|-----------|
| M1 Order & Checkout | 4 | 5 | 20 | Критичный |
| M6 Data Validation | 4 | 4 | 16 | Критичный |
| M2 Stripe Payment | 3 | 5 | 15 | Критичный |
| M8 Tax Calculation | 3 | 4 | 12 | Высокий |
| M3 Cart Management | 3 | 4 | 12 | Высокий |
| M10 Infrastructure | 2 | 5 | 10 | Средний |
| M4 Product Catalog | 2 | 3 | 6 | Средний |
| M7 Admin Panel | 2 | 3 | 6 | Средний |
| M9 Image Upload | 2 | 2 | 4 | Низкий |
| M5 Collections API | 1 | 2 | 2 | Низкий |

### Обоснование критичных модулей

**M1 — Order & Checkout (Score: 20)**

Это главная бизнес-операция системы. Один endpoint объединяет несколько действий: проверку корзины, сохранение адреса, отправку email и создание платежа в Stripe. Если что-то пойдёт не так, клиент потеряет деньги или не получит заказ.

**M6 — Data Validation (Score: 16)**

Сериализаторы DRF — единственный барьер между пользовательским вводом и базой данных. Если валидация работает неправильно, в БД попадут некорректные данные.

**M2 — Stripe Payment (Score: 15)**

Модуль работает с реальными деньгами. Ошибка может привести к двойному списанию или потере платежа.

---

## 4. Стратегия тестирования

### Уровни тестирования

| Уровень | Инструменты | Что тестируем |
|---------|-------------|---------------|
| Unit | pytest, pytest-django | Модели, валидаторы, методы |
| Integration | pytest, requests | API endpoints |
| E2E | Playwright | Админ-панель в браузере |

### Приоритет тестирования

Тесты пишутся в порядке risk score:

1. Order & Checkout — POST /orders/
2. Data Validation — граничные значения
3. Tax Calculation — edge cases GlobalModel
4. Cart Management — полный цикл
5. Product Catalog — пагинация, 404
6. Admin Panel — логин, навигация

### Автоматизация vs Ручное тестирование

| Тип | Подход | Причина |
|-----|--------|---------|
| API тесты | Автоматизация | Быстро, повторяемо |
| Unit тесты | Автоматизация | Не требует инфраструктуры |
| Admin panel | Автоматизация (Playwright) | Есть готовые инструменты |
| Stripe webhook | Ручное | Нужен ngrok для тестов |
| Визуальные баги | Ручное | Сложно автоматизировать |

---

## 5. Настройка окружения

### Структура репозитория

```
qa_as1/
├── sut/                    # Тестируемая система
│   ├── store_app/          # Основное приложение
│   ├── admin_app/          # Админ-панель
│   ├── docker-compose.yml
│   └── Dockerfile
├── tests/
│   ├── conftest.py         # Общие fixtures
│   ├── unit/               # Unit тесты
│   ├── integration/        # API тесты
│   └── e2e/                # Browser тесты
├── docs/                   # Документация
├── .github/workflows/      # CI/CD
├── pytest.ini
└── requirements-test.txt
```

### Установленные инструменты

| Инструмент | Версия | Назначение |
|------------|--------|------------|
| pytest | 7.4.3 | Запуск тестов |
| pytest-django | 4.7.0 | Интеграция с Django |
| pytest-cov | 4.1.0 | Покрытие кода |
| requests | 2.31.0 | HTTP-запросы |
| Playwright | latest | Браузерные тесты |
| Faker | 20.1.0 | Генерация данных |

### Конфигурация pytest

Файл pytest.ini:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = habaneras_de_lino_drf_api.settings.settings
pythonpath = sut
testpaths = tests
```

### Запуск системы

```bash
cd sut
cp habaneras_de_lino_drf_api/settings/simple_env_conf.env \
   habaneras_de_lino_drf_api/settings/.env
docker compose up --build
```

После запуска система доступна на http://localhost:8001

---

## 6. Написанные тесты

### Unit тесты (tests/unit/test_models.py)

Всего: 9 тестов

| Тест | Что проверяет |
|------|---------------|
| test_valid_hex_6 | Валидный цвет #FF5733 |
| test_valid_hex_3 | Валидный цвет #FFF |
| test_valid_hex_8_alpha | Валидный цвет с alpha |
| test_invalid_no_hash | Цвет без # выдаёт ошибку |
| test_invalid_too_short | Короткий цвет #FF выдаёт ошибку |
| test_invalid_non_hex_chars | #GGGGGG выдаёт ошибку |
| test_empty_cart_total_is_zero | Пустая корзина = 0 |
| test_cart_str_contains_ip | Строковое представление корзины |
| test_create_valid_address | Создание адреса |

### Integration тесты (tests/integration/test_api_endpoints.py)

Всего: 14 тестов

| Класс | Тесты |
|-------|-------|
| TestProductListAPI | 4 теста (200, JSON, pagination, invalid page) |
| TestProductDetailAPI | 1 тест (404 на несуществующий товар) |
| TestCollectionsAPI | 2 теста (200, list) |
| TestCategoriesAPI | 2 теста (200, title field) |
| TestCartAPI | 1 тест (404 на неверный токен) |
| TestOrderCreateAPI | 2 теста (400 на пустой payload, missing email) |

### E2E тесты (tests/e2e/test_admin_panel.py)

Всего: 4 теста

| Тест | Что проверяет |
|------|---------------|
| test_login_page_loads | Страница логина открывается |
| test_invalid_credentials_shows_error | Неверный пароль показывает ошибку |
| test_valid_login_redirects_to_dashboard | Успешный логин редиректит |
| test_dashboard_shows_store_app_models | Dashboard показывает модели |

---

## 7. CI/CD Pipeline

### Платформа

GitHub Actions

### Файл конфигурации

.github/workflows/ci.yml

### Этапы pipeline

```
Push/PR to main
       |
       v
+------------------+
|   Unit Tests     |  <- PostgreSQL service
|   + Coverage     |
+--------+---------+
         |
         v (если успешно)
+------------------+
| Integration Tests|  <- docker compose up
+------------------+
```

### Job 1: Unit Tests

- Поднимает PostgreSQL в контейнере
- Устанавливает зависимости
- Запускает pytest tests/unit/
- Собирает coverage report

### Job 2: Integration Tests

- Запускает docker compose up
- Ждёт 25 секунд пока приложение поднимется
- Запускает pytest tests/integration/
- Останавливает контейнеры

---

## 8. Базовые метрики

### Сложность системы

| Метрика | Значение |
|---------|----------|
| Django приложений | 2 |
| Моделей | 10 |
| API endpoints | 13 |
| Внешних интеграций | 2 |
| Строк кода (store_app) | ~900 |

### Распределение по рискам

| Уровень риска | Количество модулей |
|---------------|-------------------|
| Критичный (15+) | 3 |
| Высокий (10-14) | 3 |
| Средний (5-9) | 2 |
| Низкий (<5) | 2 |

### Покрытие тестами

| Показатель | Значение |
|------------|----------|
| Написано тестов | 27 |
| Планируется тестов | 48 |
| Текущее покрытие | ~25% |
| Целевое покрытие | 60% |

### Известные проблемы для следующих заданий

1. GlobalModel — упадёт если нет активной записи
2. Cart token — нет аутентификации
3. Order endpoint — нет защиты от дублей
4. Stripe webhook — нет проверки подписи

---

## 9. Выводы

В ходе выполнения Assignment 1 было сделано следующее:

1. Выбрана и развёрнута тестируемая система (Habaneras de Lino API)

2. Проведён анализ рисков — выявлено 3 критичных модуля из 10

3. Написана стратегия тестирования с тремя уровнями (unit, integration, e2e)

4. Настроено QA-окружение:
   - Docker для запуска системы
   - pytest для тестирования
   - Playwright для browser-тестов

5. Создан CI/CD pipeline в GitHub Actions

6. Написано 27 автотестов:
   - 9 unit тестов
   - 14 integration тестов
   - 4 e2e теста

Проект готов к расширению в следующих заданиях.

---

## 10. Приложения

### Приложение А. Команды для запуска

```bash
# Запуск системы
cd qa_as1/sut
docker compose up --build

# Unit тесты
pytest tests/unit/ -v

# Integration тесты (система должна работать)
pytest tests/integration/ -v

# E2E тесты
pytest tests/e2e/ -v

# Все тесты с coverage
pytest --cov=sut/store_app --cov-report=term-missing
```

### Приложение Б. API Endpoints

| Метод | Endpoint | Риск |
|-------|----------|------|
| GET | /clothing-products/page/ | Средний |
| GET | /clothing-products/items/id/ | Средний |
| GET | /clothing-collections/ | Низкий |
| GET | /categories/ | Низкий |
| POST | /product-variations/ | Высокий |
| GET | /cart/token/ | Высокий |
| POST | /orders/ | Критичный |
| POST | /stripe-webhook/ | Критичный |

### Приложение В. Список файлов проекта

- docs/1_risk_assessment.md — анализ рисков
- docs/2_test_strategy.md — стратегия тестирования
- docs/3_environment_setup.md — настройка окружения
- docs/4_baseline_metrics.md — базовые метрики
- .github/workflows/ci.yml — CI/CD конфигурация
- tests/unit/test_models.py — unit тесты
- tests/integration/test_api_endpoints.py — API тесты
- tests/e2e/test_admin_panel.py — browser тесты

---

**Конец отчёта**
