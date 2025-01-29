import json
import pika

def add_task_to_queue(task_id: str, equipment_id: str, parameters: dict):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()

        channel.queue_declare(queue='task_queue', durable=True)

        message = json.dumps({
            "task_id": task_id,
            "equipment_id": equipment_id,
            "parameters": parameters
        })

        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

        print(f"Задача {task_id} для устройства {equipment_id} отправлена в очередь")
        connection.close()

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Ошибка подключения к RabbitMQ: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка при отправке задачи: {e}")
