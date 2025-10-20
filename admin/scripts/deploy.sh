#!/bin/bash

echo "📤 Публикация Docker образов на Docker Hub"
echo "=========================================="

# Проверить авторизацию в Docker Hub
echo "🔐 Проверяю авторизацию в Docker Hub..."
if ! docker info | grep -q "Username"; then
    echo "❌ Не авторизован в Docker Hub"
    echo "🔑 Выполните: docker login"
    exit 1
fi

echo "✅ Авторизован в Docker Hub"

# Публиковать upload_data
echo "📦 Публикую upload_data:latest..."
docker push abovyanmg/upload_data:latest

if [ $? -eq 0 ]; then
    echo "✅ upload_data опубликован"
else
    echo "❌ Ошибка публикации upload_data"
    exit 1
fi

# Публиковать clickhouse
echo "📦 Публикую clickhouse:latest..."
docker push abovyanmg/clickhouse:latest

if [ $? -eq 0 ]; then
    echo "✅ clickhouse опубликован"
else
    echo "❌ Ошибка публикации clickhouse"
    exit 1
fi

echo ""
echo "🎉 Все образы опубликованы!"
echo ""
echo "📊 Опубликованные образы:"
echo "  - abovyanmg/upload_data:latest"
echo "  - abovyanmg/clickhouse:latest"
echo ""
echo "🌐 Доступны на: https://hub.docker.com/u/abovyanmg"
echo ""
echo "📢 Уведомите клиентов об обновлении:"
echo "  docker-compose pull"
echo "  docker-compose up -d"
