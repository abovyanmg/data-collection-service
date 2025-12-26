# 🔧 Диагностика и исправление GitHub Actions

**Дата:** 2025-12-26  
**Проблема:** GitHub Actions workflow падает с ошибкой

---

## 🔍 Диагностика проблемы

### Возможные причины:

1. **Не настроены GitHub Secrets** (наиболее вероятно)
   - `DOCKER_HUB_USERNAME` не установлен
   - `DOCKER_HUB_TOKEN` не установлен или неверный

2. **Проблема с авторизацией в Docker Hub**
   - Неверный токен
   - Токен истек
   - Недостаточно прав у токена

3. **Проблема с путями в Dockerfile**
   - Файлы не найдены при сборке
   - Неправильные пути COPY

4. **Проблема с кэшем Docker**
   - Кэш недоступен
   - Проблемы с registry

---

## ✅ Решение: Настройка GitHub Secrets

### Шаг 1: Создать Docker Hub Access Token

1. Перейдите: https://hub.docker.com/settings/security
2. Нажмите **"New Access Token"**
3. Введите описание: `GitHub Actions for ACS`
4. Выберите права: **Read & Write** (или **Read, Write & Delete**)
5. Нажмите **"Generate"**
6. **ВАЖНО:** Скопируйте токен сразу! Он показывается только один раз!

### Шаг 2: Добавить Secrets в GitHub

1. Перейдите: https://github.com/abovyanmg/data-collection-service/settings/secrets/actions
2. Нажмите **"New repository secret"**

#### Secret 1: DOCKER_HUB_USERNAME
- **Name:** `DOCKER_HUB_USERNAME`
- **Secret:** `abovyanmg`
- Нажмите **"Add secret"**

#### Secret 2: DOCKER_HUB_TOKEN
- **Name:** `DOCKER_HUB_TOKEN`
- **Secret:** `<ваш_access_token_из_шага_1>`
- Нажмите **"Add secret"**

### Шаг 3: Проверить настройки

Убедитесь, что оба secrets созданы:
- ✅ `DOCKER_HUB_USERNAME`
- ✅ `DOCKER_HUB_TOKEN`

---

## 🧪 Тестирование

### Вариант 1: Ручной запуск

1. Перейдите: https://github.com/abovyanmg/data-collection-service/actions
2. Выберите workflow **"Build and Push Docker Images"**
3. Нажмите **"Run workflow"**
4. Выберите ветку `main`
5. Нажмите **"Run workflow"**
6. Проверьте логи выполнения

### Вариант 2: Автоматический запуск

После настройки secrets, сделайте небольшое изменение в коде и push:

```bash
# Создать тестовый коммит
echo "# Test" >> README.md
git add README.md
git commit -m "Test: trigger GitHub Actions"
git push origin main
```

---

## 🔍 Проверка логов ошибки

Если workflow все еще падает:

1. Перейдите: https://github.com/abovyanmg/data-collection-service/actions
2. Откройте упавший workflow run
3. Посмотрите логи шага, который упал
4. Типичные ошибки:

### Ошибка: "unauthorized: authentication required"
**Причина:** Неверный токен или токен не установлен  
**Решение:** Проверьте `DOCKER_HUB_TOKEN` в secrets

### Ошибка: "file not found"
**Причина:** Неправильные пути в Dockerfile  
**Решение:** Проверьте пути в `Dockerfile.upload_data`

### Ошибка: "permission denied"
**Причина:** Недостаточно прав у токена  
**Решение:** Создайте новый токен с правами Read & Write

---

## 📋 Чеклист исправления

- [ ] Создан Docker Hub Access Token
- [ ] Добавлен secret `DOCKER_HUB_USERNAME` = `abovyanmg`
- [ ] Добавлен secret `DOCKER_HUB_TOKEN` = `<ваш_токен>`
- [ ] Проверены пути в Dockerfile
- [ ] Проверена структура проекта
- [ ] Запущен тестовый workflow
- [ ] Проверены логи на ошибки

---

## 🎯 Ожидаемый результат

После настройки secrets:
- ✅ Workflow запускается автоматически при push в `main`
- ✅ Docker образ собирается успешно
- ✅ Образ публикуется в Docker Hub с тегами: `latest`, `stable`
- ✅ Ошибки не приходят на почту

---

## ⚠️ Если проблема сохраняется

1. Проверьте логи workflow в GitHub Actions
2. Убедитесь, что токен не истек
3. Проверьте права токена в Docker Hub
4. Попробуйте создать новый токен

---

**Дата:** 2025-12-26

