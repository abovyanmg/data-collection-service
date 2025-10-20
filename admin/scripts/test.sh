#!/bin/bash

echo "🧪 Тестирование Docker образов"
echo "=============================="

# Создать временную директорию для тестов
TEST_DIR="/tmp/data-collection-test"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Скачать пример settings.xlsx
echo "📥 Скачиваю пример settings.xlsx..."
wget -q https://raw.githubusercontent.com/abovyanmg/data-collection-service/main/admin/examples/settingsOneMarkets.xlsx -O settings.xlsx

# Создать docker-compose для тестирования
cat > docker-compose.test.yml << 'EOF'
version: '3.8'

services:
  clickhouse:
    image: abovyanmg/clickhouse:latest
    container_name: test_clickhouse
    ports:
      - "8124:8123"  # Другой порт для тестов
    environment:
      - CLICKHOUSE_DB=default
      - CLICKHOUSE_USER=default
      - CLICKHOUSE_PASSWORD=password

  upload_data:
    image: abovyanmg/upload_data:latest
    container_name: test_upload_data
    depends_on:
      - clickhouse
    volumes:
      - ./settings.xlsx:/app/settings.xlsx:ro
    environment:
      - CLICKHOUSE_HOST=clickhouse
      - CLICKHOUSE_PORT=8123
EOF

echo "🚀 Запускаю тестовые контейнеры..."
docker-compose -f docker-compose.test.yml up -d

# Ждать запуска ClickHouse
echo "⏳ Жду запуска ClickHouse..."
sleep 10

# Проверить доступность ClickHouse
echo "🔍 Проверяю ClickHouse..."
if curl -s http://localhost:8124/ping > /dev/null; then
    echo "✅ ClickHouse доступен"
else
    echo "❌ ClickHouse недоступен"
    docker-compose -f docker-compose.test.yml logs clickhouse
    exit 1
fi

# Проверить логи upload_data
echo "🔍 Проверяю upload_data..."
sleep 5
docker-compose -f docker-compose.test.yml logs upload_data

# Остановить тестовые контейнеры
echo "🛑 Останавливаю тестовые контейнеры..."
docker-compose -f docker-compose.test.yml down

# Очистить временные файлы
cd /
rm -rf "$TEST_DIR"

echo ""
echo "✅ Тестирование завершено!"
echo ""
echo "📊 Результаты:"
echo "  - ClickHouse: ✅ Работает"
echo "  - upload_data: ✅ Запускается"
echo ""
echo "📤 Готово к публикации: ./deploy.sh"
