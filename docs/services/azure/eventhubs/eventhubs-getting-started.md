# Getting Started

=== "Python: Async"

    ```python
    import logging
    import asyncio
    from azure.eventhub.aio import EventHubConsumerClient

    connection_str = '<< CONNECTION STRING FOR THE EVENT HUBS NAMESPACE >>'
    consumer_group = '<< CONSUMER GROUP >>'
    eventhub_name = '<< NAME OF THE EVENT HUB >>'

    logger = logging.getLogger("azure.eventhub")
    logging.basicConfig(level=logging.INFO)

    async def on_event(partition_context, event):
        logger.info("Received event from partition {}".format(partition_context.partition_id))
        await partition_context.update_checkpoint(event)

    async def receive():
        client = EventHubConsumerClient.from_connection_string(connection_str, consumer_group, eventhub_name=eventhub_name)
        async with client:
            await client.receive(
                on_event=on_event,
                starting_position="-1",  # "-1" is from the beginning of the partition.
            )
            # receive events from specified partition:
            # await client.receive(on_event=on_event, partition_id='0')

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(receive())
    ```

=== "Python: Batches Async"

    ```python
    import logging
    import asyncio
    from azure.eventhub.aio import EventHubConsumerClient

    connection_str = '<< CONNECTION STRING FOR THE EVENT HUBS NAMESPACE >>'
    consumer_group = '<< CONSUMER GROUP >>'
    eventhub_name = '<< NAME OF THE EVENT HUB >>'

    logger = logging.getLogger("azure.eventhub")
    logging.basicConfig(level=logging.INFO)

    async def on_event_batch(partition_context, events):
        logger.info("Received event from partition {}".format(partition_context.partition_id))
        await partition_context.update_checkpoint()

    async def receive_batch():
        client = EventHubConsumerClient.from_connection_string(connection_str, consumer_group, eventhub_name=eventhub_name)
        async with client:
            await client.receive_batch(
                on_event_batch=on_event_batch,
                starting_position="-1",  # "-1" is from the beginning of the partition.
            )
            # receive events from specified partition:
            # await client.receive_batch(on_event_batch=on_event_batch, partition_id='0')

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(receive_batch())
    ```

=== "Python: Checkpoint"

    ```python
    import asyncio
    from azure.eventhub.aio import EventHubConsumerClient
    from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore

    connection_str = '<< CONNECTION STRING FOR THE EVENT HUBS NAMESPACE >>'
    consumer_group = '<< CONSUMER GROUP >>'
    eventhub_name = '<< NAME OF THE EVENT HUB >>'
    storage_connection_str = '<< CONNECTION STRING FOR THE STORAGE >>'
    container_name = '<<NAME OF THE BLOB CONTAINER>>'

    async def on_event(partition_context, event):
        # do something
        await partition_context.update_checkpoint(event)  # Or update_checkpoint every N events for better performance.

    async def receive(client):
        await client.receive(
            on_event=on_event,
            starting_position="-1",  # "-1" is from the beginning of the partition.
        )

    async def main():
        checkpoint_store = BlobCheckpointStore.from_connection_string(storage_connection_str, container_name)
        client = EventHubConsumerClient.from_connection_string(
            connection_str,
            consumer_group,
            eventhub_name=eventhub_name,
            checkpoint_store=checkpoint_store,  # For load balancing and checkpoint. Leave None for no load balancing
        )
        async with client:
            await receive(client)

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    ```

## Connect with Kafka

[Read More on Connector Document](https://github.com/Azure/azure-event-hubs-for-kafka/tree/master/tutorials/spark#running-spark)

```python
# Source: https://github.com/Azure/azure-event-hubs-for-kafka/tree/master/tutorials/spark#running-spark
EH_NAME_SPACE = "eventhubs-name-space"
EH_NAME = "eventhubs-name"
EH_SASL = (
    f'org.apache.kafka.common.security.plain.PlainLoginModule required'
    f'username="$ConnectionString" '
    f'password="Endpoint=sb://{EH_NAME_SPACE}.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=****";'
)
(
    df.write
        .format("kafka")
        .option("kafka.sasl.mechanism", "PLAIN")
        .option("kafka.security.protocol", "SASL_SSL")
        .option("kafka.sasl.jaas.config", EH_SASL)
        .option("kafka.batch.size", 5000)
        .option("kafka.bootstrap.servers", f"{EH_NAME_SPACE}.servicebus.windows.net:9093")
        .option("kafka.request.timeout.ms", 120000)
        .option("topic", EH_NAME)
        .option("checkpointLocation", "/mnt/telemetry/cp.txt")
        .save()
)
```

## References

- [:material-microsoft: Azure Event Hubs Features](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-features)
- [:simple-pypi: PyPI: `azure-eventhub`](https://pypi.org/project/azure-eventhub/)
- [:material-stack-overflow: Set startingPosition in Event Hub on Databricks](https://stackoverflow.com/questions/64028177/set-startingposition-in-event-hub-on-databricks)
- [How to format a Pyspark connection string for Azure Eventhub with Kafka](https://stackoverflow.com/questions/57547184/how-to-format-a-pyspark-connection-string-for-azure-eventhub-with-kafka)
