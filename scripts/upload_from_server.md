# Загрузка на PyPI с сервера (если с ПК режет соединение)

Подставьте вместо `YOUR_SERVER_IP` IP или hostname вашего сервера.

На своём ПК:

1. Собрать пакет (если ещё не собран):
   ```
   python -m build
   ```

2. Скопировать на сервер папку `dist` и скрипт:
   ```powershell
   scp -r dist scripts/upload_to_pypi.py root@YOUR_SERVER_IP:/root/
   ```

3. Зайти на сервер и загрузить:
   ```bash
   ssh root@YOUR_SERVER_IP
   cd /root
   pip install requests
   python upload_to_pypi.py __token__ pypi-ВСТАВЬ_ТОКЕН
   ```

4. После успешной загрузки удалить с сервера (по желанию):
   ```bash
   rm -rf /root/dist /root/upload_to_pypi.py
   ```

Токен на сервер передаётся только в командной строке, в репозиторий не попадает.
