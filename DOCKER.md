# Docker Setup Guide - ACS Data Collection Service

## 🐳 Полное руководство по настройке Docker для ACS сервиса

### 📋 Содержание
1. [Установка Docker](#установка-docker)
2. [Быстрый старт](#быстрый-старт)
3. [Настройка конфигурации](#настройка-конфигурации)
4. [Управление контейнерами](#управление-контейнерами)
5. [Мониторинг и логи](#мониторинг-и-логи)
6. [Устранение неполадок](#устранение-неполадок)
7. [Продвинутые настройки](#продвинутые-настройки)

---

## Установка Docker

### 🖥️ Системные требования (сервер)
- **ОС:** Ubuntu 20.04+ / CentOS 7+
- **RAM:** минимум 2GB, рекомендуется 4GB+
- **Диск:** минимум 10GB свободного места
- **CPU:** 2 ядра, рекомендуется 4+
- **Доступ:** SSH подключение

### 📦 Установка Docker Engine

#### Ubuntu/Debian:
```bash
# Обновляем пакеты
sudo apt update

# Устанавливаем зависимости
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Добавляем официальный GPG ключ Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Добавляем репозиторий Docker (автоматическое определение архитектуры)
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Обновляем список пакетов
sudo apt update

# Устанавливаем Docker
sudo apt install -y docker-ce

# Проверяем статус Docker (нажмите Ctrl+C для выхода)
sudo systemctl status docker

# Добавляем пользователя в группу docker
sudo usermod -aG docker $USER

# Перезагружаемся или выходим/входим в систему для применения изменений
```

#### Установка Docker Compose:
```bash
# Скачиваем Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Делаем файл исполняемым
sudo chmod +x /usr/local/bin/docker-compose

# Проверяем установку
docker-compose --version
```

#### CentOS/RHEL:
```bash
# Устанавливаем yum-utils
sudo yum install -y yum-utils

# Добавляем репозиторий Docker
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Устанавливаем Docker
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Запускаем и включаем Docker
sudo systemctl start docker
sudo systemctl enable docker

# Добавляем пользователя в группу docker
sudo usermod -aG docker $USER
```


### ✅ Проверка установки
```bash
# Проверяем версию Docker
docker --version

# Проверяем версию Docker Compose
docker-compose --version

# Проверяем статус Docker
sudo systemctl status docker

# Тестируем работу Docker
docker run hello-world

# Проверяем, что пользователь добавлен в группу docker
groups $USER
```

---

## Настройка сервера

### 🔧 Подготовка сервера

#### 1. Подключение к серверу
```bash
# Подключаемся к серверу по SSH
ssh root@your-server-ip

# Или если используете пользователя с sudo правами
ssh username@your-server-ip
```

#### 2. Обновление системы
```bash
# Обновляем пакеты
sudo apt update && sudo apt upgrade -y

# Устанавливаем необходимые пакеты
sudo apt install -y curl wget git unzip
```

#### 3. Настройка файрвола (опционально)
```bash
# Разрешаем SSH
sudo ufw allow ssh

# Разрешаем порты для ClickHouse
sudo ufw allow 8123
sudo ufw allow 9000

# Включаем файрвол
sudo ufw enable
```

#### 4. Создание пользователя для Docker (рекомендуется)
```bash
# Создаем пользователя
sudo adduser acsuser

# Добавляем в группу sudo
sudo usermod -aG sudo acsuser

# Переключаемся на нового пользователя
su - acsuser
```

---

## Быстрый старт

### 🚀 Развертывание ACS сервиса

#### 1. Клонирование репозитория на сервер
```bash
# Клонируем репозиторий ACS на сервер
git clone https://github.com/abovyanmg/data-collection-service.git
cd data-collection-service

# Переходим в папку клиентской части
cd client
```

#### 2. Скачивание готовых конфигураций
```bash
# Скачиваем готовый docker-compose.yml для клиентов
wget https://raw.githubusercontent.com/abovyanmg/data-collection-service/main/client/docker-compose.yml

# Скачиваем пример настроек
wget https://raw.githubusercontent.com/abovyanmg/data-collection-service/main/admin/examples/settings.xlsx
```

#### 3. Настройка переменных окружения на сервере
```bash
# Создаем файл .env на сервере
cat > .env << EOF
# ClickHouse настройки
CLICKHOUSE_HOST=my_clickhouse
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=your_secure_password

# Telegram уведомления
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Настройки проекта
PROJECT_NAME=MyProject
PLATFORM=ozon,wb,mskld,yandex,vk,getcourse

# Настройки сервера
TZ=Europe/Moscow
EOF

# Устанавливаем права доступа
chmod 600 .env
```

#### 4. Настройка файла settings.xlsx на сервере
```bash
# Копируем пример настроек
cp settings.xlsx settings_my_project.xlsx

# Устанавливаем права доступа
chmod 644 settings_my_project.xlsx

# Для редактирования на сервере устанавливаем LibreOffice (опционально)
sudo apt install -y libreoffice

# Или редактируем локально и загружаем на сервер
# scp settings_my_project.xlsx user@server:/path/to/project/
```

#### 4.5. Подготовка Docker ресурсов
```bash
# Создаем Docker volume для ClickHouse
docker volume create clickhouse_volume

# Создаем Docker network для контейнеров
docker network create --driver bridge chnet

# Проверяем созданные ресурсы
docker volume ls | grep clickhouse_volume
docker network ls | grep chnet

# Проверяем детали volume
docker volume inspect clickhouse_volume

# Проверяем детали network
docker network inspect chnet
```

#### 5. Запуск сервисов на сервере

##### Способ 1: Через Docker Compose (рекомендуется)
```bash
# Запускаем все сервисы в фоновом режиме
docker compose up -d

# Проверяем статус контейнеров
docker compose ps

# Проверяем использование ресурсов
docker stats --no-stream
```

##### Способ 2: Прямые команды docker run
```bash
# Если Docker Compose не работает, используйте прямые команды:

# ВАЖНО: Сначала остановите и удалите существующие контейнеры (если есть)
docker stop my_clickhouse upload_data 2>/dev/null || true
docker rm my_clickhouse upload_data 2>/dev/null || true

# 1. Запуск ClickHouse с конфигурацией
docker run -d --name my_clickhouse --network chnet \
  -p 8123:8123 -p 9000:9000 \
  -v clickhouse_volume:/var/lib/clickhouse \
  -v "/root/data-collection-service/client/config.xml:/etc/clickhouse-server/config.xml" \
  -v "/root/data-collection-service/client/users.xml:/etc/clickhouse-server/users.xml" \
  --user clickhouse abovyanmg/acs-clickhouse:latest

# 2. Подождите 30 секунд для запуска ClickHouse
sleep 30

# 3. Проверьте, что ClickHouse запустился
curl http://localhost:8123/ping

# 4. Запуск сбора данных
docker run -d --name upload_data --network chnet \
  -v "/root/data-collection-service/client/settings.xlsx:/app/settings.xlsx" \
  abovyanmg/acs-upload-data:latest

# 5. Проверка запущенных контейнеров
docker ps

# 6. Проверка логов ClickHouse
docker logs my_clickhouse

# 7. Проверка логов сбора данных
docker logs upload_data

# 8. Проверка подключения к ClickHouse
curl http://localhost:8123/ping

# 9. Создание базы данных (если нужно)
# Подключитесь к ClickHouse и создайте базу данных
docker exec -it my_clickhouse clickhouse-client --query "CREATE DATABASE IF NOT EXISTS acs_data"

# 10. Проверка создания базы данных
docker exec -it my_clickhouse clickhouse-client --query "SHOW DATABASES"
```

##### Запуск дополнительных контейнеров
```bash
# Для запуска дополнительных контейнеров сбора данных:

# Запуск второго контейнера сбора (с другими настройками)
docker run -d --name upload_data2 --network chnet \
  -v "/root/data-collection-service/client/settings2.xlsx:/app/settings.xlsx" \
  abovyanmg/acs-upload-data:latest

# Запуск третьего контейнера сбора
docker run -d --name upload_data3 --network chnet \
  -v "/root/data-collection-service/client/settings3.xlsx:/app/settings.xlsx" \
  abovyanmg/acs-upload-data:latest

# Проверка всех контейнеров
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

#### 6. Проверка работы на сервере
```bash
# Проверяем логи ClickHouse
docker compose logs my_clickhouse

# Проверяем логи сбора данных
docker compose logs upload_data

# Проверяем подключение к ClickHouse
curl http://localhost:8123/ping

# Проверяем доступность извне (если нужно)
curl http://your-server-ip:8123/ping
```

---

## Настройка конфигурации

### 📝 Структура settings.xlsx

#### Лист "settings"
| Поле | Описание | Пример |
|------|----------|--------|
| project_name | Название проекта | MyCompany |
| platform | Платформы (через запятую) | ozon,wb |
| clickhouse_host | Хост ClickHouse | my_clickhouse |
| clickhouse_port | Порт ClickHouse | 8123 |
| clickhouse_user | Пользователь ClickHouse | default |
| clickhouse_password | Пароль ClickHouse | your_password |

#### Лист "users"
| Поле | Описание | Пример |
|------|----------|--------|
| user_id | ID пользователя | 1 |
| user_name | Имя пользователя | admin |
| telegram_chat_id | Chat ID для уведомлений | 123456789 |
| is_active | Активен ли пользователь | true |

#### Лист "ozon"
| Поле | Описание | Пример |
|------|----------|--------|
| client_id | Client ID Ozon | your_client_id |
| api_key | API ключ Ozon | your_api_key |
| user_id | ID пользователя | 1 |
| is_active | Активен ли аккаунт | true |

#### Лист "wb"
| Поле | Описание | Пример |
|------|----------|--------|
| api_key | API ключ WB | your_api_key |
| user_id | ID пользователя | 1 |
| is_active | Активен ли аккаунт | true |

### 🔧 Настройка Telegram уведомлений

#### 1. Создание бота
1. Напишите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Сохраните полученный токен

#### 2. Получение Chat ID
```bash
# Отправьте сообщение боту, затем выполните:
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates"
```

#### 3. Настройка в settings.xlsx
Добавьте в лист "settings":
- `telegram_bot_token`: токен вашего бота
- `telegram_chat_id`: ваш Chat ID

---

## Управление контейнерами

### 🎛️ Основные команды

#### Запуск и остановка
```bash
# Запуск всех сервисов
docker compose up -d

# Остановка всех сервисов
docker compose down

# Перезапуск конкретного сервиса
docker compose restart upload_data

# Остановка конкретного сервиса
docker compose stop upload_data
```

#### Просмотр статуса
```bash
# Статус всех контейнеров
docker compose ps

# Подробная информация
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

# Использование ресурсов
docker stats
```

#### Управление образами
```bash
# Просмотр образов
docker images

# Удаление неиспользуемых образов
docker image prune

# Обновление образов
docker compose pull
docker compose up -d
```

### 🔄 Обновление сервиса

#### Автоматическое обновление
```bash
# Создаем скрипт обновления
cat > update_acs.sh << 'EOF'
#!/bin/bash
echo "🔄 Обновление ACS сервиса..."

# Останавливаем сервисы
docker compose down

# Обновляем образы
docker compose pull

# Запускаем с новыми образами
docker compose up -d

echo "✅ Обновление завершено!"
EOF

chmod +x update_acs.sh
```

#### Ручное обновление
```bash
# Останавливаем сервисы
docker compose down

# Удаляем старые образы
docker rmi abovyanmg/acs-upload-data:latest abovyanmg/acs-clickhouse:latest

# Скачиваем новые образы
docker compose pull

# Запускаем обновленные сервисы
docker compose up -d
```

---

## Мониторинг и логи

### 📊 Просмотр логов

#### Основные команды
```bash
# Логи всех сервисов
docker compose logs

# Логи конкретного сервиса
docker compose logs upload_data

# Логи в реальном времени
docker compose logs -f upload_data

# Последние 100 строк логов
docker compose logs --tail 100 upload_data
```

#### Фильтрация логов
```bash
# Логи за последний час
docker compose logs --since 1h upload_data

# Логи с определенной даты
docker compose logs --since 2024-01-01 upload_data

# Поиск по ключевым словам
docker compose logs upload_data | grep "ERROR"
docker compose logs upload_data | grep "SUCCESS"
```

### 📈 Мониторинг производительности

#### Системные ресурсы
```bash
# Использование ресурсов
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"

# Информация о контейнерах
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
```

#### Проверка здоровья
```bash
# Проверка ClickHouse
curl -s http://localhost:8123/ping

# Проверка подключения к ClickHouse
curl -s "http://localhost:8123/?query=SELECT%201"

# Проверка логов на ошибки
docker compose logs upload_data | grep -i error
```

### 🔔 Настройка уведомлений

#### Telegram уведомления
```bash
# Проверка отправки уведомлений
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage" \
  -d chat_id="<YOUR_CHAT_ID>" \
  -d text="Тестовое сообщение от ACS"
```

#### Мониторинг скрипт
```bash
# Создаем скрипт мониторинга
cat > monitor_acs.sh << 'EOF'
#!/bin/bash

# Проверяем статус ClickHouse
if ! curl -s http://localhost:8123/ping | grep -q "Ok"; then
    echo "❌ ClickHouse недоступен"
    # Отправляем уведомление в Telegram
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
      -d chat_id="$TELEGRAM_CHAT_ID" \
      -d text="🚨 ACS: ClickHouse недоступен!"
fi

# Проверяем статус контейнеров
if ! docker compose ps | grep -q "Up"; then
    echo "❌ Контейнеры не запущены"
    # Отправляем уведомление в Telegram
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
      -d chat_id="$TELEGRAM_CHAT_ID" \
      -d text="🚨 ACS: Контейнеры не запущены!"
fi

echo "✅ Мониторинг завершен"
EOF

chmod +x monitor_acs.sh
```

---

## Устранение неполадок

### 🚨 Частые проблемы

#### 1. Контейнеры не запускаются
```bash
# Проверяем логи
docker compose logs

# Проверяем конфигурацию
docker compose config

# Перезапускаем с пересборкой
docker compose down
docker compose up --build
```

#### 2. Ошибки подключения к ClickHouse
```bash
# Проверяем доступность ClickHouse
curl http://localhost:8123/ping

# Проверяем логи ClickHouse
docker compose logs my_clickhouse

# Проверяем сеть Docker
docker network ls
docker network inspect acs_default
```

#### 3. Ошибки сбора данных
```bash
# Проверяем настройки
docker compose exec upload_data cat /app/settings.xlsx

# Проверяем подключение к API
docker compose exec upload_data python -c "import requests; print(requests.get('https://api.ozon.ru').status_code)"

# Проверяем логи сбора данных
docker compose logs upload_data | grep -i error
```

#### 4. Проблемы с памятью
```bash
# Проверяем использование памяти
docker stats

# Очищаем неиспользуемые ресурсы
docker system prune -a

# Увеличиваем лимиты памяти в docker-compose.yml
```

### 🔧 Диагностика

#### Полная диагностика системы
```bash
# Создаем скрипт диагностики
cat > diagnose_acs.sh << 'EOF'
#!/bin/bash

echo "🔍 Диагностика ACS сервиса"
echo "=========================="

# Проверяем Docker
echo "📦 Docker версия:"
docker --version
docker compose version

# Проверяем контейнеры
echo "🐳 Статус контейнеров:"
docker compose ps

# Проверяем сеть
echo "🌐 Docker сеть:"
docker network ls

# Проверяем ClickHouse
echo "🗄️ ClickHouse:"
curl -s http://localhost:8123/ping || echo "❌ ClickHouse недоступен"

# Проверяем логи
echo "📋 Последние ошибки:"
docker compose logs --tail 20 | grep -i error

# Проверяем ресурсы
echo "💾 Использование ресурсов:"
docker stats --no-stream

echo "✅ Диагностика завершена"
EOF

chmod +x diagnose_acs.sh
./diagnose_acs.sh
```

---

## Безопасность и оптимизация ClickHouse

### 🔒 Настройка безопасности

#### 1. Ограничение доступа по IP
```bash
# Настройте файрвол для ограничения доступа к ClickHouse
sudo ufw allow from YOUR_IP to any port 8123
sudo ufw allow from YOUR_IP to any port 9000
sudo ufw deny 8123
sudo ufw deny 9000
```

#### 2. Сложные пароли
```bash
# Измените пароли в users.xml на сложные
# Рекомендуется использовать пароли длиной 16+ символов
# с буквами, цифрами и специальными символами
```

#### 3. Создание таблицы для отслеживания сбора данных
```sql
CREATE TABLE IF NOT EXISTS acs_data.collection (
    platform String,
    client_name String,
    report_name String,
    date Date,
    status String,
    created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (platform, client_name, report_name, date)
```

### 📊 Работа с данными в ClickHouse

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

#### 4. Мониторинг размера таблиц
```sql
-- Проверка размера таблиц
SELECT 
    database,
    table,
    formatReadableSize(sum(bytes)) as size
FROM system.parts 
WHERE active = 1
GROUP BY database, table
ORDER BY sum(bytes) DESC
```

### 📱 Настройка Telegram уведомлений

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

## Продвинутые настройки

### ⚙️ Кастомизация docker-compose.yml

#### Добавление дополнительных сервисов
```yaml
version: '3.8'

services:
  my_clickhouse:
    image: abovyanmg/acs-clickhouse:latest
    container_name: my_clickhouse
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - clickhouse_data:/var/lib/clickhouse
    networks:
      - chnet

  upload_data:
    image: abovyanmg/acs-upload-data:latest
    container_name: upload_data
    depends_on:
      - my_clickhouse
    volumes:
      - ./settings.xlsx:/app/settings.xlsx:ro
      - ./logs:/app/logs
    environment:
      - CLICKHOUSE_HOST=my_clickhouse
      - CLICKHOUSE_PORT=8123
    networks:
      - chnet
    restart: unless-stopped

  # Дополнительный сервис для мониторинга
  monitoring:
    image: prom/prometheus:latest
    container_name: acs_monitoring
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - chnet

volumes:
  clickhouse_data:

networks:
  chnet:
    driver: bridge
```

#### Настройка ресурсов
```yaml
services:
  upload_data:
    image: abovyanmg/acs-upload-data:latest
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
```

### 🔐 Безопасность

#### Настройка секретов
```bash
# Создаем файл с секретами
cat > .env.secrets << EOF
CLICKHOUSE_PASSWORD=your_secure_password
TELEGRAM_BOT_TOKEN=your_bot_token
OZON_API_KEY=your_ozon_api_key
WB_API_KEY=your_wb_api_key
EOF

# Устанавливаем права доступа
chmod 600 .env.secrets

# Добавляем в .gitignore
echo ".env.secrets" >> .gitignore
```

#### Настройка сети
```yaml
networks:
  chnet:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### 📊 Мониторинг и алерты

#### Настройка Prometheus
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'acs-clickhouse'
    static_configs:
      - targets: ['my_clickhouse:8123']
  
  - job_name: 'acs-upload'
    static_configs:
      - targets: ['upload_data:8000']
```

#### Настройка Grafana
```yaml
  grafana:
    image: grafana/grafana:latest
    container_name: acs_grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    networks:
      - chnet
```

---

## 📚 Дополнительные ресурсы

### 🔗 Полезные ссылки
- [Официальная документация Docker](https://docs.docker.com/)
- [Docker Compose документация](https://docs.docker.com/compose/)
- [ClickHouse документация](https://clickhouse.com/docs/)
- [ACS GitHub репозиторий](https://github.com/abovyanmg/data-collection-service)

### 📞 Поддержка
- **Email:** abovyan.mg@gmail.com
- **GitHub Issues:** [Создать issue](https://github.com/abovyanmg/data-collection-service/issues)
- **Telegram:** @abovyanmg

### 🏆 Благодарности
**Спасибо за базис:** Morinad  
**Особая благодарность Александру Морину (@alexdirect)** - это сенсей и человек, которому я очень благодарен за знания и вдохновение.

---

**Разработано:** AbovyansConsultingServices  
**Основано на открытых технологиях**
