# Assignment 1 Defense Guide
## QA Landscape, Risk Assessment & Environment Setup

---

## 1. Краткое описание проекта (2 мин)

**System Under Test:** Habaneras de Lino — Django REST API для e-commerce магазина одежды.

**Технологии:**
- Backend: Django 4.0.6 + Django REST Framework 3.13.1
- Database: PostgreSQL 13
- Infrastructure: Docker, Nginx
- External: Stripe (платежи), Cloudinary (изображения)

**Что мы сделали:**
1. Провели анализ рисков (10 модулей)
2. Написали тестовую стратегию
3. Настроили QA-окружение (Docker + pytest + Playwright)
4. Создали CI/CD pipeline (GitHub Actions)
5. Написали 27 тестов (unit + integration + e2e)

---

## 2. Демонстрация запуска SUT (3 мин)

### Шаг 1: Настройка .env файла
```bash
cd qa_as1/sut
cp habaneras_de_lino_drf_api/settings/simple_env_conf.env habaneras_de_lino_drf_api/settings/.env
```

### Шаг 2: Запуск через Docker Compose
```bash
docker compose up --build
```

**Что происходит:**
- `db` — PostgreSQL контейнер
- `api` — Django приложение (порт 8000 внутренний)
- `nginx` — Reverse proxy (порт 8001 → внешний)

### Шаг 3: Проверка работоспособности
```bash
# В новом терминале
curl http://localhost:8001/clothing-products/1/
curl http://localhost:8001/categories/
```

**URL для демонстрации:**
- API Products: http://localhost:8001/clothing-products/1/
- API Categories: http://localhost:8001/categories/
- Admin Panel: http://localhost:8001/admin/

---

## 3. Risk Assessment — Объяснение (5 мин)

### Методология
**Risk Score = Probability × Impact** (шкала 1-5)

### Топ-4 критических модуля:

| # | Модуль | Prob | Impact | Score | Почему критичен |
|---|--------|------|--------|-------|-----------------|
| 1 | Order & Checkout | 4 | 5 | **20** | Основная бизнес-транзакция, потеря денег |
| 2 | Data Validation | 4 | 4 | **16** | Единственный барьер от плохих данных в БД |
| 3 | Stripe Payment | 3 | 5 | **15** | Реальные деньги, юридические риски |
| 4 | Tax Calculation | 3 | 4 | **12** | GlobalModel singleton — упадёт весь pricing |

### Пример объяснения M1 (Order & Checkout):
> "Этот модуль имеет наивысший risk score 20, потому что:
> - **Probability = 4**: Сложная логика — объединяет корзину, адрес, email, Stripe charge в одной операции
> - **Impact = 5**: Отказ = потеря заказа = потеря денег клиента и репутации
> - **Failure scenarios**:
>   - Cart token mismatch принят
>   - Order создан, но payment не записан
>   - Email notification упал молча"

### Документ: `docs/1_risk_assessment.md`

---

## 4. Test Strategy — Объяснение (3 мин)

### Три уровня тестирования:

| Уровень | Инструмент | Когда запускать | Что тестирует |
|---------|-----------|-----------------|---------------|
| Unit | pytest-django | Каждый commit | Модели, валидаторы, бизнес-логика |
| Integration | pytest + requests | Каждый commit | API endpoints, contracts |
| E2E | Playwright | На PR merge | Admin panel через браузер |

### Risk-Based приоритет:
1. Order & Checkout — POST /orders/ (valid/invalid payloads)
2. Data Validation — Boundary tests на serializers
3. Tax Calculation — GlobalModel edge cases
4. Cart Management — Full lifecycle

### Документ: `docs/2_test_strategy.md`

---

## 5. Environment Setup — Демонстрация (3 мин)

### Структура репозитория:
```
qa_as1/
├── sut/                    # System Under Test (клонированный репо)
├── tests/
│   ├── unit/               # pytest-django (9 тестов)
│   ├── integration/        # requests (14 тестов)
│   └── e2e/                # Playwright (4 теста)
├── docs/                   # 4 deliverable документа
├── .github/workflows/ci.yml
├── pytest.ini
└── requirements-test.txt
```

### Установка тестовых зависимостей:
```bash
pip install -r requirements-test.txt
playwright install chromium
```

### pytest.ini конфигурация:
```ini
[pytest]
DJANGO_SETTINGS_MODULE = habaneras_de_lino_drf_api.settings.settings
pythonpath = sut
testpaths = tests
```

### Документ: `docs/3_environment_setup.md`

---

## 6. Запуск тестов — Демонстрация (5 мин)

### Unit тесты (без запущенного приложения):
```bash
cd qa_as1
pytest tests/unit/ -v
```

**Ожидаемый результат:** 9 passed

**Что тестируется:**
- `TestCustomColorValidator` — валидация hex-цветов (#FFF, #FF5733, #GGGGGG)
- `TestCartTotalAmount` — пустая корзина = 0
- `TestAddressModel` — создание адреса

### Integration тесты (приложение должно быть запущено):
```bash
# Убедитесь что docker compose up работает
pytest tests/integration/ -v
```

**Ожидаемый результат:** 14 passed

**Что тестируется:**
- GET /clothing-products/1/ → 200, JSON, pagination
- GET /categories/ → 200, list with titles
- POST /orders/ с пустым payload → 400
- GET /cart/invalidtoken/ → 404

### E2E тесты (Playwright):
```bash
pytest tests/e2e/ -v
```

**Что тестируется:**
- Admin login page loads
- Invalid credentials → error message
- Valid login → redirect to dashboard
- Logout works

---

## 7. CI/CD Pipeline — Объяснение (3 мин)

### Файл: `.github/workflows/ci.yml`

### Pipeline stages:

```
Push to main/PR
      │
      ▼
┌─────────────────┐
│   Unit Tests    │  ← PostgreSQL service container
│   + Coverage    │    pytest tests/unit/ --cov
└────────┬────────┘
         │ (on success)
         ▼
┌─────────────────────┐
│ Integration Tests   │  ← docker compose up
│                     │    pytest tests/integration/
└─────────────────────┘
```

### Ключевые моменты:
1. **PostgreSQL service** — для unit тестов с реальной БД
2. **docker compose up** — поднимает SUT для integration тестов
3. **Coverage report** — загружается как artifact

---

## 8. Baseline Metrics (2 мин)

| Метрика | Значение |
|---------|----------|
| Всего модулей | 10 |
| Critical risk модулей | 3 |
| High risk модулей | 3 |
| API endpoints | 13 |
| Тестов написано | 27 |
| Планируемых тестов | 48 |
| Текущий coverage | ~25% (только unit) |
| Целевой coverage | ≥60% |

### Known Design Concerns (для следующих assignments):
- `GlobalModel` singleton — crash если 0 или 2+ active records
- Cart token — нет аутентификации, риск collision
- Order endpoint — нет idempotency key (дубликаты при retry)

### Документ: `docs/4_baseline_metrics.md`

---

## 9. Частые вопросы на защите

### Q: Почему выбрали именно эту систему?
> "Habaneras de Lino — реальный e-commerce API с полным набором критичных функций:
> платежи (Stripe), корзина, заказы, каталог. Это позволяет продемонстрировать
> risk-based подход на реальных бизнес-сценариях."

### Q: Почему Order & Checkout имеет highest risk score?
> "Risk Score = 4 × 5 = 20. Probability высокая из-за сложности: один endpoint
> объединяет cart validation, address, email, Stripe charge. Impact максимальный —
> это прямая потеря денег и репутации."

### Q: Почему unit тесты не требуют запущенного приложения?
> "pytest-django использует in-memory SQLite для изоляции. Мы тестируем только
> Python-код моделей и валидаторов, без HTTP-запросов."

### Q: Как CI/CD помогает в QA?
> "Автоматический запуск тестов на каждый push/PR гарантирует, что регрессии
> обнаруживаются сразу. Coverage report показывает, какой код не покрыт тестами."

### Q: Что будет в Assignment 2?
> "Расширение test coverage, добавление тестов для critical modules (Order, Stripe),
> defect tracking, и возможно performance testing."

---

## 10. Чеклист перед защитой

- [ ] Docker Desktop запущен
- [ ] `docker compose up --build` работает без ошибок
- [ ] http://localhost:8001/clothing-products/1/ возвращает JSON
- [ ] `pytest tests/unit/ -v` — все тесты проходят
- [ ] `pytest tests/integration/ -v` — все тесты проходят (SUT запущен)
- [ ] Открыты файлы документации в `docs/`
- [ ] GitHub репозиторий доступен (если требуется показать CI)

---

## Полезные команды

```bash
# Запуск SUT
cd qa_as1/sut && docker compose up --build

# Остановка SUT
docker compose down

# Все тесты с coverage
pytest --cov=sut/store_app --cov-report=term-missing

# Только unit тесты
pytest tests/unit/ -v

# Только integration тесты
pytest tests/integration/ -v

# Только e2e тесты
pytest tests/e2e/ -v

# Просмотр логов Django
docker compose logs -f api
```
