#!/bin/bash

echo "🚀 Data Collection Service - Быстрый старт"
echo "=========================================="

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    echo "📥 Установите Docker: https://docker.com"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен!"
    echo "📥 Установите Docker Compose"
    exit 1
fi

echo "✅ Docker найден"

# Скачать docker-compose.yml если его нет
if [ ! -f "docker-compose.yml" ]; then
    echo "📥 Скачиваю docker-compose.yml..."
    wget -q https://raw.githubusercontent.com/abovyanmg/data-collection-service/main/client/docker-compose.yml
fi

# Скачать пример settings.xlsx если его нет
if [ ! -f "settings.xlsx" ]; then
    echo "📥 Скачиваю пример settings.xlsx..."
    wget -q https://raw.githubusercontent.com/abovyanmg/data-collection-service/main/client/examples/settings_example.xlsx -O settings.xlsx
    echo "⚠️  ВАЖНО: Отредактируйте settings.xlsx с вашими токенами!"
fi

# Запустить систему
echo "🚀 Запускаю систему..."
docker-compose up -d

# Проверить статус
echo "📊 Статус контейнеров:"
docker-compose ps

echo ""
echo "✅ Система запущена!"
echo ""
echo "📊 Мониторинг:"
echo "  - ClickHouse: http://localhost:8123"
echo "  - Логи: docker-compose logs -f"
echo "  - Статус: docker-compose ps"
echo ""
echo "⚠️  Не забудьте отредактировать settings.xlsx с вашими API токенами!"
echo "🔄 После редактирования: docker-compose restart"
