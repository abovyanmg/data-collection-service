# 🚀 Руководство для новых клиентов

## 📋 Подключение новой системы

### Шаг 1: Установка Docker

Убедитесь, что Docker установлен на вашем сервере:

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# macOS
# Скачать Docker Desktop с https://docker.com

# Проверка установки
docker --version
```

### Шаг 2: Скачивание конфигурации

```bash
# Создайте директорию для проекта
mkdir -p ~/acs-data-collection
cd ~/acs-data-collection

# Скачайте docker-compose.yml
wget https://raw.githubusercontent.com/abovyanmg/data-collection-service/main/client/docker-compose.yml

# Скачайте пример settings.xlsx
wget https://raw.githubusercontent.com/abovyanmg/data-collection-service/main/admin/examples/settings_template.xlsx -O settings.xlsx
```

### Шаг 3: Настройка конфигурации

Откройте `settings.xlsx` и заполните:

1. **Лист 1 (Настройки БД)**:
   - ClickHouse настройки (обычно уже настроены)
   - Telegram токен и chat_id для уведомлений

2. **Лист 2+ (Платформы)**:
   - Выберите нужные платформы (Ozon, Wildberries, МойСклад и т.д.)
   - Укажите API токены
   - Настройте даты и типы отчетов

### Шаг 4: Запуск системы

```bash
# Запуск с автоматической загрузкой стабильных образов
docker-compose up -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f
```

## 🔖 Выбор версии образа

В `docker-compose.yml` указана стабильная версия по умолчанию:

```yaml
services:
  upload_data_example:
    image: abovyanmg/acs-upload-data:stable  # ✅ Рекомендуется
```

### Варианты версий:

1. **`stable`** (рекомендуется) - стабильная версия для production
   ```yaml
   image: abovyanmg/acs-upload-data:stable
   ```

2. **`latest`** - последняя версия (может быть нестабильной)
   ```yaml
   image: abovyanmg/acs-upload-data:latest
   ```

3. **Конкретная версия** - максимальная стабильность
   ```yaml
   image: abovyanmg/acs-upload-data:v1.0.0
   ```

## 🔄 Обновление системы

### Автоматическое обновление (если используете `stable` или `latest`):

```bash
docker-compose pull
docker-compose up -d
```

### Откат на предыдущую версию:

```bash
# Остановить текущие контейнеры
docker-compose down

# Откатиться на конкретную версию
docker-compose pull abovyanmg/acs-upload-data:v1.0.0

# Запустить с конкретной версией
docker-compose up -d
```

## 📊 Мониторинг

### Проверка работы системы:

```bash
# Статус контейнеров
docker-compose ps

# Логи в реальном времени
docker-compose logs -f upload_data_example

# Проверка ClickHouse
curl http://localhost:8123

# Здоровье контейнеров
docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
```

### Доступ к ClickHouse:

- **HTTP интерфейс**: http://localhost:8123
- **Native интерфейс**: localhost:9000

## 🛠️ Устранение проблем

### Контейнер не запускается:

```bash
# Проверить логи
docker-compose logs upload_data_example

# Проверить конфигурацию
docker-compose config

# Пересоздать контейнеры
docker-compose down
docker-compose up -d
```

### Проблемы с подключением к ClickHouse:

```bash
# Проверить доступность ClickHouse
docker-compose ps clickhouse

# Проверить логи ClickHouse
docker-compose logs clickhouse

# Перезапустить ClickHouse
docker-compose restart clickhouse
```

### Откат на предыдущую версию:

```bash
# 1. Остановить систему
docker-compose down

# 2. Указать конкретную версию в docker-compose.yml
# Изменить image: abovyanmg/acs-upload-data:stable
# На: image: abovyanmg/acs-upload-data:v1.0.0

# 3. Запустить
docker-compose up -d
```

## 📞 Поддержка

Если возникли проблемы:

1. **Проверьте логи**: `docker-compose logs -f`
2. **Создайте Issue**: https://github.com/abovyanmg/data-collection-service/issues
3. **Напишите на email**: abovyan.mg@gmail.com

## ✅ Чеклист для нового клиента

- [ ] Docker установлен и работает
- [ ] `docker-compose.yml` скачан
- [ ] `settings.xlsx` заполнен с токенами API
- [ ] Контейнеры запущены (`docker-compose up -d`)
- [ ] ClickHouse доступен (http://localhost:8123)
- [ ] Логи показывают успешную работу
- [ ] Telegram уведомления работают (если настроены)

---

**Создано с ❤️ для автоматизации сбора данных**

