import asyncio
import aiohttp
import datetime
import json

async def get_currency_rates(date):
    try:
        url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date.strftime('%d.%m.%Y')}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    # Check content type before decoding
                    if response.content_type == 'application/json':
                        data = await response.json()
                        # Фільтруємо дані за EUR та USD
                        filtered_data = {
                            'date': data['date'],
                            'exchangeRate': [rate for rate in data['exchangeRate'] if rate['currency'] in ('EUR', 'USD')]
                        }
                        return filtered_data
                    else:
                        print(f"Unexpected content type: {response.content_type}")
                else:
                    print(f"HTTP error: {response.status} - {response.reason}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise




async def main():
  """
  Отримати курси валют ПриватБанку за останні 10 днів.
  """
  today = datetime.date.today()
  dates = [today - datetime.timedelta(days=i) for i in range(10)]

  tasks = [get_currency_rates(date) for date in dates]
  results = await asyncio.gather(*tasks)

  print(json.dumps(results, indent=2))


if __name__ == "__main__":
  asyncio.run(main())
