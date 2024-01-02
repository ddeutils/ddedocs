# Azure EventHubs: _Produce Data_

```python
import asyncio
import aiohttp
import json
import logging
from azure.eventhub import EventHubClient, EventData

async def get_weather(city, state, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{state}&appid={api_key}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

async def send_to_event_hub(event_hub_client, weather_data):
    event = EventData(json.dumps(weather_data).encode("utf-8"))
    await event_hub_client.send(event)

async def main(api_key, event_hub_client):
    # List of cities in the USA
    cities = [
        {"city": "New York", "state": "NY"},
        {"city": "Los Angeles", "state": "CA"},
        {"city": "Chicago", "state": "IL"},
        {"city": "Houston", "state": "TX"},
        {"city": "Phoenix", "state": "AZ"},
        {"city": "Philadelphia", "state": "PA"},
        {"city": "San Antonio", "state": "TX"},
        {"city": "San Diego", "state": "CA"},
        {"city": "Dallas", "state": "TX"},
        {"city": "San Jose", "state": "CA"}
    ]

    tasks = []
    for city_data in cities:
        task = asyncio.create_task(get_weather(city_data["city"], city_data["state"], api_key))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    for weather_data in results:
        await send_to_event_hub(event_hub_client, weather_data)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Event Hub Configuration
event_hub_namespace = "<Your Azure Event Hub Namespace>"
event_hub_name = "eh_sample_01"
event_hub_key = "<Your Azure Event Hub Key>"
event_hub_endpoint = f"amqps://{event_hub_namespace}.servicebus.windows.net/{event_hub_name}"

api_key = "<Your OpenWeatherMap API Key>"
interval = 5 * 60 # 5 minutes in seconds
event_hub_client = EventHubClient.from_connection_string(event_hub_endpoint, event_hub_key)

while True:
    asyncio.run(main(api_key, event_hub_client))
    await asyncio.sleep(interval)
```
