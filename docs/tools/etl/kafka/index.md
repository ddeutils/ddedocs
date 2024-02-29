---
icon: material/apache-kafka
---

# Kafka

- [Setting up Apache Kafka for local development with Docker](https://medium.com/devops-techable/setting-up-apache-kafka-for-local-development-with-docker-aa3c5810073a)

## Connection Code

```shell
$ pip install kafka-python
```

=== "Producer"

    ```python
    from kafka import KafkaProducer
    import json

    producer = KafkaProducer(
        bootstrap_servers='localhost:29092',
        security_protocol="PLAINTEXT",
        value_serializer=lambda v: json.dumps(v).encode('ascii')
    )

    producer.send(
     'hotel-booking-request',
     value={
         "name": "Evy Lina",
         "hotel": "Cheap Hotel",
         "dateFrom": "14-07-2024",
         "dateTo": "01-08-2021",
         "details": "Wish coffee ready 😀"
         }
    )
    producer.flush()
    ```

=== "Consumer"

    ```python
    from kafka import KafkaConsumer
    import json

    consumer = KafkaConsumer(
        bootstrap_servers='localhost:29092',
        security_protocol="PLAINTEXT",
        value_deserializer=lambda v: json.loads(v.decode('ascii')),
        # auto_offset_reset='earliest'
    )

    consumer.subscribe(topics='hotel-booking-request')

    for message in consumer:
        print(f"{message.partition}:{message.offset} v={message.value}")
    ```

- [Write your first Kafka producer and Kafka consumer in Python](https://medium.com/devops-techable/write-your-first-kafka-producer-and-kafka-consumer-in-python-67461403c91d)
