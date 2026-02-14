# Запуск в Docker

**Важно:** в `docker-compose.yml` указан пример пароля ClickHouse (`password`). Для продакшена задайте свой пароль через переменные окружения или `users.xml`.

## Установка Docker

- **Компьютер:** установите Docker Desktop для вашей ОС.
- **Сервер (Ubuntu):** `sudo apt update`, затем установка по https://docs.docker.com/engine/install/ubuntu/

## Вариант 1: docker-compose (рекомендуется)

Скачайте в папку с настройками файл [docker-compose.yml](https://raw.githubusercontent.com/abovyanmg/data-collection-service/main/docker-compose.yml). Положите туда же `settings.xlsx`.

```bash
docker-compose up -d
```

Дополнительные контейнеры сбора — скопируйте сервис `upload_data` в docker-compose с новым именем и своим файлом настроек (например `settings2.xlsx`).

## Вариант 2: docker run

### Подготовка

```bash
docker volume create clickhouse_volume
docker network create --driver bridge chnet
```

### ClickHouse (официальный образ)

**Linux (папка /home):**

```bash
docker run -d --name my_clickhouse --network chnet -p 8123:8123 -p 9000:9000 \
  -v clickhouse_volume:/var/lib/clickhouse \
  -v "/home/config.xml:/etc/clickhouse-server/config.xml" \
  -v "/home/users.xml:/etc/clickhouse-server/users.xml" \
  --user clickhouse clickhouse/clickhouse-server:stable \
  --config-file=/etc/clickhouse-server/config.xml
```

Примеры config.xml и users.xml — в `admin/examples/`.

### Контейнер сбора данных

**Linux:**

```bash
docker run -d --name upload_data --network chnet \
  -v "/home/settings.xlsx:/app/settings.xlsx" \
  abovyanmg/acs-upload-data:stable
```

Ещё один контейнер с другим файлом настроек:

```bash
docker run -d --name upload_data2 --network chnet \
  -v "/home/settings2.xlsx:/app/settings.xlsx" \
  abovyanmg/acs-upload-data:stable
```

**Windows:** укажите свою папку вместо `/home`, например `C:/path/to/settings.xlsx`.

---

## Обновление образа и перезапуск

Подтянуть новый образ и пересоздать контейнер:

```bash
docker pull abovyanmg/acs-upload-data:stable
docker stop <имя_контейнера>
docker rm <имя_контейнера>
docker run -d --name <имя_контейнера> --network chnet \
  -v "/путь/к/settings.xlsx:/app/settings.xlsx:ro" \
  --restart unless-stopped \
  abovyanmg/acs-upload-data:stable
```

Только перезапуск без пересоздания: `docker restart <имя_контейнера>`.

Пересборка образа из репо (корень репо — папка с `admin/`):

```bash
docker build -f admin/docker/Dockerfile.upload_data -t abovyanmg/acs-upload-data:stable .
docker push abovyanmg/acs-upload-data:stable   # при необходимости
```

---

## Как клиенты получают обновления библиотеки

У нас библиотека **не зашита в образ**: при каждом старте контейнер ставит пакет с PyPI (`pip install --upgrade acs-data-collection`). Поэтому:

**Обновление кода сбора (новые отчёты, правки API):** клиенту достаточно **перезапустить контейнер** — при следующем запуске подтянется новая версия с PyPI.

```bash
docker restart <имя_контейнера>
# или для docker-compose:
docker-compose restart upload_data
```

**Обновление самого образа** (меняли Dockerfile или `upload_main.py`): тогда нужны `docker pull` и пересоздание контейнера (как в блоке «Обновление образа и перезапуск» выше).

**У Морина:** образ `morinad/upload_data` — библиотека, скорее всего, вшита в образ. Обновления у клиентов = новый образ, т.е. `docker pull morinad/upload_data` и пересоздание контейнера. У нас клиенты получают обновления без смены образа — только перезапуск.

---

## Релиз новой версии (для разработчиков)

1. **Версия:** поднять `version` в `setup.py` и при необходимости `LABEL version` в `admin/docker/Dockerfile.upload_data`.
2. **PyPI:** из корня репо:
   ```bash
   pip install build twine
   python -m build
   twine upload dist/*
   ```
   (нужны учётные данные PyPI для пакета `acs-data-collection`).
3. **Docker Hub (по желанию):** если меняли Dockerfile или `upload_main.py`:
   ```bash
   docker build -f admin/docker/Dockerfile.upload_data -t abovyanmg/acs-upload-data:stable .
   docker push abovyanmg/acs-upload-data:stable
   ```
4. **Клиентам:** сообщить, что для получения обновления достаточно перезапустить контейнер сбора (`docker restart ...`).
