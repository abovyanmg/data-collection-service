#!/bin/bash

echo "🔨 Сборка Docker образов"
echo "========================"

# Перейти в директорию с Dockerfiles
cd "$(dirname "$0")/../docker"

# Собрать образ upload_data
echo "📦 Сборка upload_data..."
docker build -t abovyanmg/upload_data:latest -f Dockerfile.upload_data .

if [ $? -eq 0 ]; then
    echo "✅ upload_data собран успешно"
else
    echo "❌ Ошибка сборки upload_data"
    exit 1
fi

# Собрать образ clickhouse
echo "📦 Сборка clickhouse..."
docker build -t abovyanmg/clickhouse:latest -f Dockerfile.clickhouse .

if [ $? -eq 0 ]; then
    echo "✅ clickhouse собран успешно"
else
    echo "❌ Ошибка сборки clickhouse"
    exit 1
fi

echo ""
echo "🎉 Все образы собраны успешно!"
echo ""
echo "📊 Список образов:"
docker images | grep abovyanmg

echo ""
echo "🧪 Для тестирования запустите: ./test.sh"
echo "📤 Для публикации запустите: ./deploy.sh"
