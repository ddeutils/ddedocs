# Azure Function: _To Azure Service Bus_

## Using Managed Identity

```yaml
ServiceBusConnection__clientID: <managedidenity client id>
ServiceBusConnection__credential: managedidentity
ServiceBusConnection__fullyQualifiedNamespace: <servicebusname>.servicebus.windows.net
```

### 1) Connection Code

```python
import os
import asyncio
from aiohttp import ClientSession
from azure.servicebus.aio import ServiceBusClient

conn_str = os.environ['SERVICE_BUS_CONNECTION_STR']
topic_name = os.environ['SERVICE_BUS_TOPIC_NAME']
subscription_name = os.environ['SERVICE_BUS_SUBSCRIPTION_NAME']

async def watch(
        topic_name,
        subscription_name,
):
    async with ServiceBusClient.from_connection_string(conn_str=conn_str) as service_bus_client:
        subscription_receiver = service_bus_client.get_subscription_receiver(
            topic_name=topic_name,
            subscription_name=subscription_name,
        )
    async with subscription_receiver:
         message = await subscription_receiver.receive_messages(max_wait_time=1)

    if message.body is not None:
        async with ClientSession() as session:
            await session.post('ip:port/endpoint',
                               headers={'Content-type': 'application/x-www-form-urlencoded'},
                               data={'data': message.body.decode()})

async def do():
    while True:
        for topic in ['topic1', 'topic2', 'topic3']:
            await watch(topic, 'watcher')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do())
```

## References

- https://stackoverflow.com/questions/63149310/azure-servicebus-using-async-await-in-python-seems-not-to-work
- https://iqan.medium.com/how-to-use-managed-identity-in-azure-functions-for-service-bus-trigger-fc61fb828b90
