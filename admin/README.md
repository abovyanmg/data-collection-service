# 🔧 Админская часть - ACS Data Collection Service

**AbovyansConsultingServices - Инструменты для разработки, сборки и обновления Docker образов**

---

## 📁 Структура

```
admin/
├── docker/                    # Dockerfiles для сборки образов
│   ├── Dockerfile.upload_data
│   └── Dockerfile.clickhouse
├── library/                   # Исходники библиотеки morin
│   └── morin/
├── scripts/                   # Скрипты автоматизации
│   ├── build.sh              # Сборка образов
│   ├── test.sh               # Тестирование
│   └── deploy.sh             # Публикация на Docker Hub
├── configs/                   # Конфигурации для разработки
├── examples/                  # Примеры settings.xlsx
└── docs/                      # Документация для разработки
```

---

## 🚀 Быстрый старт для админа

### 1. Локальное тестирование
```bash
# Собрать образ локально
cd admin/docker
docker build -t test-upload-data -f Dockerfile.upload_data .

# Протестировать
docker run --rm -v $(pwd)/../examples/settingsOneMarkets.xlsx:/app/settings.xlsx test-upload-data
```

### 2. Сборка для продакшена
```bash
# Собрать все образы
./scripts/build.sh

# Протестировать
./scripts/test.sh

# Опубликовать на Docker Hub
./scripts/deploy.sh
```

### 3. GitHub Actions
```bash
# Автоматическая сборка при push в main
git push origin main
# → GitHub Actions соберет и опубликует образы
```

---

## 🔄 Workflow обновлений

1. **Разработка** → Изменения в коде
2. **Тестирование** → `./scripts/test.sh`
3. **Сборка** → `./scripts/build.sh`
4. **Публикация** → `./scripts/deploy.sh` или GitHub Actions
5. **Уведомление клиентов** → Обновление документации

---

## 📊 Мониторинг

- **Docker Hub**: https://hub.docker.com/u/your_username
- **GitHub Actions**: https://github.com/YOUR_USERNAME/data-collection-service/actions
- **Тесты**: Локальные + CI/CD

---

## 🛠️ Инструменты

- **Docker**: Сборка образов
- **GitHub Actions**: Автоматизация
- **Docker Hub**: Хранение образов
- **Git**: Версионирование

---

**Для разработчиков и администраторов сервиса**
