# 🚀 ACS Data Collection Service

**AbovyansConsultingServices - Профессиональный сервис сбора данных с маркетплейсов в ClickHouse**

---

## 📋 Поддерживаемые платформы

- **Wildberries** (WB) - товары, заказы, аналитика
- **Ozon** - товары, заказы, реклама, аналитика  
- **МойСклад** (MSKLD) - складской учет, продажи
- **Яндекс.Маркет** (YM) - товары, заказы
- **Яндекс.Директ** (YD) - рекламные кампании
- **VK** - реклама, статистика
- **Bitrix24** - CRM данные
- **AlfaCRM** - клиентская база
- **GetCourse** - обучающие курсы
- **Google Sheets** - интеграция с таблицами

---

## 🏗️ Архитектура

```
┌────────────────────────────────────────────────────────────┐
│  Docker Hub (abovyansconsulting/data-collection)          │
│  ├── upload_data:latest                                   │
│  └── clickhouse:latest                                    │
└─────────────────┬──────────────────────────────────────────┘
                  │
                  │ docker pull
                  ▼
┌────────────────────────────────────────────────────────────┐
│  Клиентский сервер                                         │
│  ├── ClickHouse (порт 8123)                               │
│  ├── upload_data контейнеры (по клиентам)                 │
│  └── settings.xlsx (конфигурация)                         │
└────────────────────────────────────────────────────────────┘
```

---

## 🚀 Быстрый старт

### 1. Установка Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# macOS
# Скачать Docker Desktop с https://docker.com
```

### 2. Запуск системы
```bash
# Скачать готовый docker-compose.yml
wget https://raw.githubusercontent.com/abovyansconsulting/data-collection-service/main/client/docker-compose.yml

# Запустить
docker-compose up -d
```

### 3. Настройка
1. Скачать `settings.xlsx` из examples/
2. Заполнить токены API
3. Перезапустить контейнеры

---

## 📊 Мониторинг

- **ClickHouse**: http://localhost:8123
- **Логи**: `docker-compose logs -f`
- **Статус**: `docker-compose ps`

---

## 🔧 Конфигурация

### settings.xlsx структура:
- **Лист 1**: Настройки БД и Telegram
- **Лист 2+**: Конфигурация платформ (токены, даты, отчеты)

### Примеры конфигураций:
- `settingsOneMarkets.xlsx` - Ozon + Wildberries
- `settingsTATTOOFEELandLinePro.xlsx` - МойСклад + Ozon
- `settingsbeYoo.xlsx` - Яндекс.Директ + VK

---

## 📈 Преимущества

✅ **Готовые Docker образы** - развертывание за 5 минут  
✅ **Автоматические обновления** - GitHub Actions  
✅ **Поддержка всех платформ** - WB, Ozon, MSKLD, Yandex  
✅ **Telegram уведомления** - мониторинг в реальном времени  
✅ **Масштабируемость** - один сервер = много клиентов  
✅ **Безопасность** - токены хранятся у клиента  

---

## 💰 Стоимость

**Для клиентов:**
- Сервер: от 200₽/мес (1 vCPU, 1GB RAM)
- Настройка: бесплатно
- Поддержка: по запросу

**Для вас (как сервис-провайдера):**
- Docker Hub: бесплатно (публичные образы)
- GitHub: бесплатно
- Время настройки: 1-2 часа на клиента

---

## 🆚 Сравнение с morinad

| Параметр | morinad | Ваш сервис |
|----------|---------|------------|
| **Доступность** | Зависит от morinad | Полная независимость |
| **Обновления** | Ручные | Автоматические |
| **Поддержка** | Через morinad | Прямая поддержка от ACS |
| **Кастомизация** | Ограниченная | Полная |
| **Стоимость** | Подписка | Прозрачная |

---

## 📞 Поддержка

- **GitHub Issues**: https://github.com/abovyansconsulting/data-collection-service/issues
- **Telegram**: @abovyansconsulting
- **Email**: info@abovyansconsulting.com

---

## 📄 Лицензия

Использует библиотеку [morin](https://github.com/morinad/morin) v0.4.45  
Автор: Александр Морин (y.director@yandex.ru)

---

**Создано с ❤️ для автоматизации сбора данных**
