import discord
import requests
from bs4 import BeautifulSoup
import re
import os
import asyncio  # Import asyncio for background tasks

# Supported currencies
SUPPORTED_CURRENCIES = ['USD', 'NZD', 'CAD', 'BDT', 'MYR', 'MUR', 'EUR', 'EGP', 'SAR', 'TRY']

# Mapping of currency codes to (singular name, plural name)
CURRENCY_NAMES = {
    'USD': ('United States Dollar', 'United States Dollars'),
    'NZD': ('New Zealand Dollar', 'New Zealand Dollars'),
    'CAD': ('Canadian Dollar', 'Canadian Dollars'),
    'BDT': ('Bangladeshi Taka', 'Bangladeshi Taka'),
    'MYR': ('Malaysian Ringgit', 'Malaysian Ringgit'),
    'MUR': ('Mauritian Rupee', 'Mauritian Rupees'),
    'EUR': ('Euro', 'Euros'),
    'EGP': ('Egyptian Pound', 'Egyptian Pounds'),
    'SAR': ('Saudi Riyal', 'Saudi Riyals'),
    'TRY': ('Turkish Lira', 'Turkish Lira')
}

def get_exchange_rate(from_currency, to_currency):
    url = f"https://wise.com/us/currency-converter/{from_currency.lower()}-to-{to_currency.lower()}-rate?amount=1000"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the exchange rate
        rate_text = soup.find('span', class_='text-success')
        rate = float(re.search(r"\d+\.\d+", rate_text.text.strip()).group()) if rate_text else None

        # Extract the 30-day high, low, average, and change
        table_rows = soup.select('table tr')
        high_30 = float(table_rows[1].find_all('td')[1].text)
        low_30 = float(table_rows[2].find_all('td')[1].text)
        average_30 = float(table_rows[3].find_all('td')[1].text)
        change_30 = table_rows[4].find_all('td')[1].text.strip()
        
        return rate, high_30, low_30, average_30, change_30, url
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return None, None, None, None, None, None

# Initialize Discord bot with intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Placeholder for error logging channel and startup message channel
ERROR_CHANNEL_ID = 1305733544261455882  # Replace with the actual channel ID for error logs
STARTUP_CHANNEL_ID = 1305733544261455882  # Replace with the actual channel ID for startup message
PERIODIC_CHANNEL_ID = 1305815351069507604  # Channel to send periodic messages

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    # Send a startup message to the designated channel
    startup_channel = client.get_channel(STARTUP_CHANNEL_ID)
    if startup_channel:
        await startup_channel.send("Bot has started and is ready to convert currencies!")
    
    # Start background task for periodic messages
    client.loop.create_task(send_periodic_message())

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Handle 'convert' or variations like 'Convert' and 'conv'
    if message.content.lower().startswith(('convert', 'conv')):
        try:
            parts = message.content.split()
            amount = float(parts[1])
            from_currency = parts[2].upper()
            to_currency = parts[4].upper()

            if from_currency not in SUPPORTED_CURRENCIES or to_currency not in SUPPORTED_CURRENCIES:
                supported_currencies = "\n".join(
                    f"{i+1}. {CURRENCY_NAMES[c][1]} ({c})" for i, c in enumerate(SUPPORTED_CURRENCIES)
                )
                await message.channel.send(
                    f"**That's not a currency dumbfuck. Supported currencies are:**\n{supported_currencies}\n\n"
                    "**To use the currency converter, type:**\n`conv [amount] [from_currency] to [target_currency]`"
                )
                return

            rate, high_30, low_30, average_30, change_30, url = get_exchange_rate(from_currency, to_currency)

            if rate:
                converted_amount = amount * rate

                from_currency_singular, from_currency_plural = CURRENCY_NAMES[from_currency]
                to_currency_singular, to_currency_plural = CURRENCY_NAMES[to_currency]

                from_currency_name = from_currency_singular if amount == 1 else from_currency_plural
                to_currency_name = to_currency_singular if round(converted_amount, 2) == 1.00 else to_currency_plural

                await message.channel.send(
                    f"**{amount} {from_currency_name}** is approximately **{converted_amount:.2f} {to_currency_name}** at an exchange rate of **{rate:.4f}**.\n"
                    f"In the past 30 days, the **high** was {high_30}, the **low** was {low_30}, with an **average** of {average_30} and a **change** of {change_30}%.\n"
                    f"Click here for additional info: [source]({url})"
                )
            else:
                await send_error("Exchange rate or historical data not found.", message)
        except Exception as e:
            await send_error(f"Error: {str(e)}", message)

    # Handle 'listcur' for listing supported currencies
    elif message.content.lower().startswith('listcur'):
        currency_list = "\n".join(
            f"{i+1}. {CURRENCY_NAMES[c][1]} ({c})" for i, c in enumerate(SUPPORTED_CURRENCIES)
        )
        await message.channel.send(
            f"**Supported currencies:**\n{currency_list}\n\n"
            "**To use the currency converter, type:**\n`conv [amount] [from_currency] to [target_currency]`"
        )

async def send_error(error_message, original_message):
    error_channel = client.get_channel(ERROR_CHANNEL_ID)
    if error_channel:
        await error_channel.send(f"Error in processing request from {original_message.author}: {error_message}")
    else:
        print("Error channel not found. Please set a valid ERROR_CHANNEL_ID.")

async def send_periodic_message():
    await client.wait_until_ready()  # Ensure bot is fully ready
    channel = client.get_channel(PERIODIC_CHANNEL_ID)
    while True:
        if channel:
            await channel.send("This is a periodic message sent every 28 minutes. Prevents dynos sleeping on heroku.")
        await asyncio.sleep(28 * 60)  # Wait 28 minutes

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
client.run(DISCORD_TOKEN)
