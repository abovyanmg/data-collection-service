# Инструкция по обновлению Docker Hub после актуализации с Morin

## 📋 Что было обновлено

После актуализации проекта ACS с Morin были внесены изменения в следующие файлы:
- `admin/library/acs_data_library/common.py` - синхронизация с Morin, сохранена поддержка Airflow
- `admin/library/acs_data_library/ozon_reklama.py` - обновлена обработка ошибок
- `admin/library/acs_data_library/wb_reklama.py` - исправлен delay (90 → 61)
- Добавлены `setup.py` и `LICENSE`

## 🐳 Обновление Docker Hub

### Шаг 1: Авторизация в Docker Hub

```powershell
docker login -u abovyan.mg@gmail.com
# Введите пароль при запросе
```

### Шаг 2: Переход в директорию проекта

```powershell
cd C:\Users\RAIDER\Desktop\ACS\repos\acs-project
```

### Шаг 3: Сборка образа upload_data

```powershell
# Сборка образа с обновленным кодом
docker build -f admin/docker/Dockerfile.upload_data -t abovyanmg/acs-upload-data:latest .
```

**Важно:** Dockerfile должен собираться из корня проекта, чтобы правильно скопировать все файлы.

### Шаг 4: Создание тегов для версионирования

```powershell
# Создаем тег stable (стабильная версия)
docker tag abovyanmg/acs-upload-data:latest abovyanmg/acs-upload-data:stable

# Создаем тег с версией
docker tag abovyanmg/acs-upload-data:latest abovyanmg/acs-upload-data:v1.0.0
```

### Шаг 5: Публикация образов в Docker Hub

```powershell
# Публикуем latest версию
docker push abovyanmg/acs-upload-data:latest

# Публикуем stable версию
docker push abovyanmg/acs-upload-data:stable

# Публикуем версию v1.0.0
docker push abovyanmg/acs-upload-data:v1.0.0
```

## 🔍 Проверка после публикации

### Проверка локальных образов

```powershell
docker images | Select-String "abovyanmg"
```

### Проверка в Docker Hub

Откройте в браузере: https://hub.docker.com/repositories/abovyanmg

Должны быть видны обновленные образы с новыми тегами.

## 📝 Примечания

1. **Время сборки:** Сборка образа может занять 5-10 минут в зависимости от скорости интернета
2. **Размер образа:** Ожидаемый размер образа ~500-800 MB
3. **Обновление ClickHouse:** Если нужно обновить образ ClickHouse, используйте:
   ```powershell
   docker build -f admin/docker/Dockerfile.clickhouse -t abovyanmg/acs-clickhouse:latest .
   docker push abovyanmg/acs-clickhouse:latest
   ```

## 🚀 Автоматизация (рекомендуется)

Для автоматической сборки при каждом коммите рекомендуется настроить GitHub Actions:

1. Создать файл `.github/workflows/docker-build.yml`
2. Настроить автоматическую сборку при push в main
3. Использовать GitHub Secrets для хранения Docker Hub credentials

## ✅ Чеклист

- [ ] Авторизован в Docker Hub
- [ ] Образ успешно собран
- [ ] Теги созданы (latest, stable, v1.0.0)
- [ ] Образы опубликованы в Docker Hub
- [ ] Проверены образы в Docker Hub веб-интерфейсе
- [ ] Клиенты могут обновить свои контейнеры командой `docker pull abovyanmg/acs-upload-data:stable`

---

**Дата обновления:** 2025-12-26  
**Версия:** 1.0.0

