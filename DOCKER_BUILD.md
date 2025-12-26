# Инструкция по сборке и публикации Docker образов

## 🐳 Сборка Docker образа

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
# Сборка образа из корня проекта
docker build -f admin/docker/Dockerfile.upload_data -t abovyanmg/acs-upload-data:latest .
```

**Важно:** Dockerfile должен собираться из корня проекта (`.`), чтобы правильно скопировать все файлы.

### Шаг 4: Создание тегов (опционально)

```powershell
# Стабильная версия
docker tag abovyanmg/acs-upload-data:latest abovyanmg/acs-upload-data:stable

# Версия с номером
docker tag abovyanmg/acs-upload-data:latest abovyanmg/acs-upload-data:v1.0.0
```

### Шаг 5: Публикация в Docker Hub

```powershell
# Публикуем latest
docker push abovyanmg/acs-upload-data:latest

# Публикуем stable (если создали тег)
docker push abovyanmg/acs-upload-data:stable
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

## 📝 Примечания

- Сборка образа занимает 5-10 минут
- Размер образа: ~500-800 MB
- После публикации клиенты могут обновить контейнеры командой: `docker pull abovyanmg/acs-upload-data:stable`

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

