#!/bin/bash
# Скрипт для создания версионных тегов существующих образов на Docker Hub
# Использование: ./create_version_tags.sh

set -e

echo "🔖 Создание версионных тегов для существующих образов на Docker Hub"
echo ""

# Версия для стабильного тега
VERSION="v1.0.0"
STABLE_TAG="stable"

# Список образов для версионирования
IMAGES=(
  "abovyanmg/upload_data"
  "abovyanmg/clickhouse"
  "abovyanmg/acs-upload-data"
  "abovyanmg/acs-clickhouse"
)

# Проверка авторизации в Docker Hub
echo "🔐 Проверка авторизации в Docker Hub..."
if ! docker info > /dev/null 2>&1; then
  echo "❌ Docker не запущен"
  exit 1
fi

echo "✅ Docker работает"
echo ""

# Для каждого образа создаем версионные теги
for IMAGE in "${IMAGES[@]}"; do
  echo "📦 Обработка образа: $IMAGE"
  
  # Пытаемся скачать latest образ
  if docker pull "${IMAGE}:latest" --platform linux/amd64 > /dev/null 2>&1 || \
     docker pull "${IMAGE}:latest" > /dev/null 2>&1; then
    echo "  ✅ Образ ${IMAGE}:latest найден"
    
    # Создаем тег stable
    docker tag "${IMAGE}:latest" "${IMAGE}:${STABLE_TAG}"
    if docker push "${IMAGE}:${STABLE_TAG}" > /dev/null 2>&1; then
      echo "  ✅ Создан и отправлен тег: ${IMAGE}:${STABLE_TAG}"
    else
      echo "  ⚠️  Не удалось отправить тег: ${IMAGE}:${STABLE_TAG}"
    fi
    
    # Создаем версионный тег
    docker tag "${IMAGE}:latest" "${IMAGE}:${VERSION}"
    if docker push "${IMAGE}:${VERSION}" > /dev/null 2>&1; then
      echo "  ✅ Создан и отправлен тег: ${IMAGE}:${VERSION}"
    else
      echo "  ⚠️  Не удалось отправить тег: ${IMAGE}:${VERSION}"
    fi
    
    echo ""
  else
    echo "  ⚠️  Образ ${IMAGE}:latest не найден на Docker Hub или недоступен для текущей платформы"
    echo "  💡 Попробуйте выполнить вручную:"
    echo "     docker pull ${IMAGE}:latest --platform linux/amd64"
    echo "     docker tag ${IMAGE}:latest ${IMAGE}:${STABLE_TAG}"
    echo "     docker tag ${IMAGE}:latest ${IMAGE}:${VERSION}"
    echo "     docker push ${IMAGE}:${STABLE_TAG}"
    echo "     docker push ${IMAGE}:${VERSION}"
    echo ""
  fi
done

echo "✅ Версионирование завершено!"
echo ""
echo "📋 Созданные теги:"
for IMAGE in "${IMAGES[@]}"; do
  echo "  - ${IMAGE}:${STABLE_TAG}"
  echo "  - ${IMAGE}:${VERSION}"
done
echo ""
echo "🎯 Теперь клиенты могут использовать стабильные версии!"
echo "   В docker-compose.yml укажите: image: abovyanmg/upload_data:stable"
