# Данные API в ClickHouse на Python Docker Connectors: WB, Ozon, Яндекс и другие платформы

## ACS Data Collection Service - Профессиональный сервис сбора данных с маркетплейсов

**Автор:** AbovyansConsultingServices  
**Дата:** Октябрь 2025  
**Версия:** 1.0

---

## 🎯 Что это такое?

**ACS Data Collection Service** - это профессиональный сервис для автоматического сбора данных с популярных маркетплейсов и платформ в ClickHouse. Полная альтернатива существующим решениям с независимой архитектурой.

### Поддерживаемые платформы:

- **Wildberries (WB)** - товары, заказы, аналитика
- **Ozon** - товары, заказы, реклама, аналитика  
- **МойСклад (MSKLD)** - складской учет, продажи
- **Яндекс.Маркет (YM)** - товары, заказы
- **Яндекс.Директ (YD)** - рекламные кампании
- **VK** - реклама, статистика
- **Bitrix24** - CRM данные
- **AlfaCRM** - клиентская база
- **Google Sheets** - интеграция с таблицами

---

## 🏗️ Архитектура решения

### Docker-контейнеры:
- **`abovyanmg/acs-upload-data:latest`** - основной контейнер сбора данных
- **`abovyanmg/acs-clickhouse:latest`** - ClickHouse сервер

### Преимущества:
✅ **Независимость** - полная автономность от внешних сервисов  
✅ **Масштабируемость** - один сервер = много клиентов  
✅ **Безопасность** - токены хранятся у клиента  
✅ **Автоматизация** - Telegram уведомления  
✅ **Простота** - запуск в 5 минут  

---

## ⚡ Быстрый старт (5 минут)

### 1. Подготовка сервера

**Рекомендуемые серверы:**
- **Hostland** - от 200₽/месяц (первый месяц)
- **Timeweb** - от 350₽/месяц
- **Selectel** - от 400₽/месяц

**Минимальные требования:**
- Ubuntu 20.04+ / CentOS 7+
- 2GB RAM (рекомендуется 4GB+)
- 10GB диска
- SSH доступ

### 2. Установка Docker

```bash
# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем зависимости
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Добавляем официальный GPG ключ Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Добавляем репозиторий Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Устанавливаем Docker
sudo apt update
sudo apt install -y docker-ce

# Проверяем установку
sudo systemctl status docker
```

### 3. Запуск ACS системы

```bash
# Скачать проект
git clone https://github.com/abovyanmg/data-collection-service.git
cd data-collection-service/client

# Запустить систему
./quick-start.sh
```

### 4. Настроить API токены

Отредактируйте файл `settings.xlsx` с вашими токенами:

| Платформа | Токен | Статус |
|-----------|-------|--------|
| Wildberries | `your_wb_token` | ✅ |
| Ozon | `your_ozon_token` | ✅ |
| Яндекс.Директ | `your_yd_token` | ✅ |
| VK | `your_vk_token` | ✅ |

### 3. Перезапустить

```bash
docker-compose restart
```

---

## 🔧 Детальная настройка

### Docker Compose конфигурация

```yaml
version: '3.8'

services:
  clickhouse:
    image: abovyanmg/clickhouse:latest
    container_name: my_clickhouse
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - clickhouse_data:/var/lib/clickhouse
      - clickhouse_logs:/var/log/clickhouse
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8123/ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  upload_data:
    image: abovyanmg/upload_data:latest
    container_name: upload_data_example
    depends_on:
      clickhouse:
        condition: service_healthy
    volumes:
      - ./settings.xlsx:/app/settings.xlsx:ro
    environment:
      - CLICKHOUSE_HOST=clickhouse
      - CLICKHOUSE_PORT=8123
    restart: unless-stopped

volumes:
  clickhouse_data:
  clickhouse_logs:
```

### Настройка ClickHouse

```sql
-- Создание базы данных
CREATE DATABASE IF NOT EXISTS marketplace_data;

-- Создание таблицы для WB
CREATE TABLE IF NOT EXISTS marketplace_data.wb_orders (
    order_id String,
    sku String,
    name String,
    price Float64,
    quantity UInt32,
    date Date,
    status String
) ENGINE = MergeTree()
ORDER BY (date, order_id);
```

---

## 📊 Мониторинг и уведомления

### Telegram уведомления

```python
# Настройка в settings.xlsx
TELEGRAM_BOT_TOKEN = "your_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"
```

### Логи и мониторинг

```bash
# Просмотр логов
docker-compose logs -f

# Статус контейнеров
docker-compose ps

# Подключение к ClickHouse
curl "http://localhost:8123/?query=SELECT%20*%20FROM%20marketplace_data.wb_orders%20LIMIT%2010"
```

---

## 🆚 Сравнение с аналогами

| Параметр | Другие решения | ACS сервис |
|----------|----------------|------------|
| **Доступность** | Зависит от провайдера | Полная независимость |
| **Обновления** | Ручные | Автоматические |
| **Поддержка** | Через посредников | Прямая поддержка от ACS |
| **Кастомизация** | Ограниченная | Полная |
| **Стоимость** | Подписка | Прозрачная |

---

## 🚀 Продвинутые возможности

### Кастомные запросы

```python
# Пример кастомного сбора данных
from morin import WBbyDate

wb = WBbyDate(
    token="your_token",
    clickhouse_host="localhost",
    clickhouse_port=8123
)

# Сбор данных за последние 30 дней
wb.collect_data(days=30)
```

### Интеграция с BI системами

```sql
-- Создание представления для аналитики
CREATE VIEW marketplace_data.sales_summary AS
SELECT 
    date,
    platform,
    COUNT(*) as orders_count,
    SUM(price * quantity) as total_revenue
FROM marketplace_data.all_orders
GROUP BY date, platform;
```

---

## 🔧 Устранение неполадок

### Частые проблемы

**1. ClickHouse не запускается**
```bash
# Проверить логи
docker-compose logs clickhouse

# Перезапустить
docker-compose restart clickhouse
```

**2. Ошибки API токенов**
```bash
# Проверить настройки
cat settings.xlsx

# Обновить токены и перезапустить
docker-compose restart upload_data
```

**3. Проблемы с сетью**
```bash
# Проверить сеть Docker
docker network ls

# Пересоздать контейнеры
docker-compose down && docker-compose up -d
```

---

## 🔒 Безопасность и оптимизация

### Настройка безопасности ClickHouse

#### 1. Ограничение доступа по IP
```bash
# Настройте файрвол для ограничения доступа к ClickHouse
sudo ufw allow from YOUR_IP to any port 8123
sudo ufw allow from YOUR_IP to any port 9000
sudo ufw deny 8123
sudo ufw deny 9000
```

#### 2. Сложные пароли
- Измените пароли в `users.xml` на сложные (16+ символов)
- Используйте буквы, цифры и специальные символы
- Регулярно обновляйте пароли

### Работа с данными в ClickHouse

#### 1. Таблицы Merge для объединения данных
```sql
-- Создание таблицы Merge для объединения однотипных таблиц
CREATE TABLE acs_data.ozon_all AS acs_data.ozon_test_1
ENGINE = Merge(currentDatabase(), '^ozon_')
```

#### 2. Представления (Views) для аналитики
```sql
-- Создание представления для аналитики
CREATE VIEW acs_data.sales_summary AS
SELECT 
    platform,
    client_name,
    toDate(created_at) as date,
    count() as records_count
FROM acs_data.collection
WHERE status = 'success'
GROUP BY platform, client_name, date
ORDER BY date DESC
```

#### 3. Управление пересбором данных
```sql
-- Удаление данных для пересбора (замените дату на нужную)
DELETE FROM acs_data.collection WHERE date = '2025-10-23'

-- Оптимизация таблиц
OPTIMIZE TABLE acs_data.collection
```

### Telegram уведомления

#### 1. Создание бота
1. Найдите @BotFather в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Сохраните полученный токен

#### 2. Получение Chat ID
```bash
# Для личного чата: используйте @userinfobot
# Для группового чата: добавьте бота в группу с админскими правами
# Получите chat_id через API:
curl "https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates"
```

#### 3. Настройка в settings.xlsx
- **TELEGRAM_BOT_TOKEN:** токен от BotFather
- **TELEGRAM_CHAT_ID:** ваш личный ID или ID группы (с минусом)
- **TELEGRAM_NOTIFICATIONS:** включить/выключить уведомления

---

## 📞 Поддержка

- **GitHub Issues**: https://github.com/abovyanmg/data-collection-service/issues
- **Email**: abovyan.mg@gmail.com
- **Документация**: https://github.com/abovyanmg/data-collection-service

---

## 📄 Лицензия

Разработано: AbovyansConsultingServices  
Основано на открытых технологиях

---

## 🙏 Благодарности

**Спасибо за базис: Morinad**

**Особая благодарность Александру Морину (@alexdirect)** - это сенсей и человек, которому я очень благодарен за знания и вдохновение.

---

**Создано с ❤️ для автоматизации сбора данных**

---

## 🔗 Полезные ссылки

- **GitHub репозиторий**: https://github.com/abovyanmg/data-collection-service
- **Docker Hub**: https://hub.docker.com/u/abovyanmg
- **Быстрый старт**: https://github.com/abovyanmg/data-collection-service/blob/main/client/quick-start.sh
- **Примеры настроек**: https://github.com/abovyanmg/data-collection-service/tree/main/admin/examples

---

*Статья обновлена: Октябрь 2025*
