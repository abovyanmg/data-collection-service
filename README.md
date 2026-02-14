# ACS Data Collection Service

**AbovyansConsultingServices — сервис сбора данных с маркетплейсов в ClickHouse**

Коннекторы загружают данные из API. Проект работает на Docker и пишет в ClickHouse; библиотеку можно использовать и отдельно.

### Поддерживаемые платформы

WB, Ozon, МойСклад, Яндекс.Маркет, Яндекс.Директ, VK, Bitrix24, AlfaCRM, Google Sheets.

### Быстрый старт

1. Установите Docker.
2. Скачайте [docker-compose.yml](https://raw.githubusercontent.com/abovyanmg/data-collection-service/main/docker-compose.yml) в папку с настройками.
3. Положите туда же `settings.xlsx` (структура: лист db — БД и Telegram, остальные листы — платформы).
4. Запуск: `docker-compose up -d`

Подробнее по Docker: [DOCKER.md](DOCKER.md)

### Конфигурация

- **settings.xlsx** — лист «db»: host, port, user, password, database, bot_token, chats; листы платформ: токены, отчёты, расписание.
- ClickHouse: порт 8123 (HTTP), логи: `docker-compose logs -f`

### Поддержка

- Issues: https://github.com/abovyanmg/data-collection-service/issues
- Email: abovyan.mg@gmail.com

### Лицензия

Разработано: AbovyansConsultingServices. Основано на открытых технологиях.

### Контекст для разработки

- **Библиотека:** `admin/library/acs_data_library/`; точка входа в контейнере: `admin/docker/upload_main.py`. Пакет PyPI: `acs-data-collection` (при старте контейнера: `pip install --upgrade acs-data-collection`).
- **Сделано:** логика отчётов WB синхронизирована с референсом Morin (voronka_week/voronka_all, get_table_data, get_chunks, sleep 90 в рекламе); версия в setup.py и Dockerfile; публикация на PyPI вручную (см. scripts/); чувствительные данные в .gitignore.

### Безопасность

Владелец может передавать логины и пароли агентам (ИИ или людям) для выполнения и проверки проекта. **Ни при каких обстоятельствах** не размещать эти логины и пароли в общедоступных местах: в репозитории на GitHub, в файлах, которые выгружаются и могут стать доступны третьим лицам, в примерах кода, в коммитах и т.п. Только локально или в защищённых каналах.

### Благодарности

**Спасибо за базис: Morinad**

**Особая благодарность Александру Морину (@alexdirect)** — за знания и вдохновение.
