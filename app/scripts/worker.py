import json
import pika
import httpx
import asyncio

SSL_CERTFILE = "../certs/localhost.crt"
SSL_KEYFILE = "../certs/localhost.key"


async def process_task(task_data):
    task_id = task_data.get("task_id")
    equipment_id = task_data.get("equipment_id")
    timeout_in_seconds = task_data["parameters"].get("timeoutInSeconds", 60)

    if not task_id or not equipment_id:
        print("Отсутствуют обязательные данные в сообщении: task_id или equipment_id")
        return None, None

    request_body = {
        "username": "admin",
        "password": "password123",
        "vlan": 10,
        "interfaces": [1, 2, 3],
        "key1": "value1",
        "key2": "value2"
    }

    custom_params = task_data["parameters"].get("parameters", {})
    request_body.update(custom_params)

    print(f"Обработка задачи {task_id} для оборудования {equipment_id}")
    print(f"Отправляемый JSON: {json.dumps(request_body, indent=2)}")

    url = f"https://localhost:443/api/v1/equipment/cpe/{equipment_id}?timeoutInSeconds={timeout_in_seconds}"

    try:
        async with httpx.AsyncClient(
            verify=SSL_CERTFILE,
            cert=(SSL_CERTFILE, SSL_KEYFILE)
        ) as client:
            response = await client.post(url, json=request_body, timeout=timeout_in_seconds)

            task_status = "success" if response.status_code == 200 else f"Ошибка: {response.status_code}, {response.text}"
            print(f"Ответ от сервера: {response.status_code}")
            print(f"Тело ответа: {response.text}")

    except httpx.RequestError as e:
        print(f"Ошибка при запросе к серверу A: {e}")
        task_status = f"Ошибка сети: {str(e)}"
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        task_status = f"Ошибка: {str(e)}"

    return task_id, task_status


async def handle_message(ch, body):
    try:
        message = body.decode('utf-8')
        print(f"Получено сообщение: {message}")

        if not message.strip():
            print("Пустое сообщение!")
            return

        task_data = json.loads(message)
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")
        return
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return

    task_id, task_status = await process_task(task_data)

    if task_id is None:
        print("Ошибка при обработке задачи")
        return

    print(f"Задача {task_id} завершена с результатом: {task_status}")
    ch.basic_publish(
        exchange='',
        routing_key='task_status_queue',
        body=json.dumps({"task_id": task_id, "status": task_status})
    )


def on_message(ch, method, properties, body):
    asyncio.run(handle_message(ch, body))


def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='task_queue', durable=True)
        channel.basic_consume(queue='task_queue', on_message_callback=on_message, auto_ack=True)

        print('Ожидание сообщений. Для выхода нажмите CTRL+C')
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Ошибка подключения к RabbitMQ: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
    finally:
        if 'connection' in locals():
            connection.close()


if __name__ == "__main__":
    main()
