## 🚀 Как развернуть проект локально

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/morozgit/testRT.git
   ```

1. ** Создайте SSL сертификат и ключ  в директории certs/ **
   ```bash
   openssl genpkey -algorithm RSA -out localhost.key -pkeyopt rsa_keygen_bits:2048

   openssl req -new -x509 -key localhost.key -out localhost.crt -days 365 -subj "/C=RU/ST=Some-State/O=Internet Widgits Pty Ltd/CN=localhost"
   ```
2. **Запуск**
   ```bash
   cd testRT/app
   docker compose up --build
   ```
3. **Запустите worker:**
   ```bash
   cd testRT/app/scripts
   python3 python3 worker.py 
   ```
   **POST запрос** https://localhost:444/api/v1/equipment/cpe/123456?timeoutInSeconds=60


4. **Успешный ответ от сервера А**
    ```
    Ответ от сервера: 200
    Тело ответа: {"code":200,"message":"success"}
    Задача 796e195e-e79b-4b71-bc1c-f9ed5719f743 завершена с результатом: successall
   ```
