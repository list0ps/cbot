import discord
import aiohttp
import requests
from bs4 import BeautifulSoup #for currency web-scrapping
import re 
import os # Local testing with tokens in .env file
import asyncio  # Imported asyncio for background tasks
import pytz  # Adding this for timezone handling
from datetime import datetime  # Adding this for date and time handling
from data_mappings import (
    timezones_dict,
    USER_TIMEZONE_MAPPING,
    CURRENCY_NAMES,
    COUNTRY_ABBREVIATIONS,
    SUPPORTED_CURRENCIES,
    USER_LOCATION_MAPPING,
)
from readme_content import (
    get_readme_embed,
    get_weather_help_embed,
    get_currency_help_embed,
    get_time_help_embed,
    get_currency_list_embed,
    get_timezone_list_embed
)

#web scrapper bs from chatgpt to fetch conversion info 
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
    
    
# Updated get_current_time function with additional cities for more countries
def get_current_time(location):
    # Dictionary of countries, abbreviations, cities and GMT offsets
    # Only way to support country abbreviations was to list them as separate elements (because I suck at python)
 

    # Normalizing input for case-insensitive matching because my friend alex is weird
    location = location.strip().casefold()

    results = []

    # Check if location is a country or abbreviation 
    if location in timezones_dict:
        for city, abbreviation, timezone, gmt_offset in timezones_dict[location]:
            tz = pytz.timezone(timezone)
            city_time = datetime.now(tz)
            results.append(f"The current time is **{city_time.strftime('%I:%M %p')}** in {city.title()}, {location.upper()}. {gmt_offset}")
        return results

    # Check for a matching city or abbreviation
    for country, cities in timezones_dict.items():
        for city, abbreviation, timezone, gmt_offset in cities:
            if location in {city, abbreviation}:
                tz = pytz.timezone(timezone)
                city_time = datetime.now(tz)
                results.append(f"The current time is **{city_time.strftime('%I:%M %p')}** in {city.title()}, {country.upper()}. {gmt_offset}")
                return results

    return None


# Updated `time_conversion` function for accurate conversions, was broken because misalignment of full names
def convert_time(time_str, from_location, to_location):
    # Uses the same `timezones_dict` as in get_current_time

    # Normalizing inputs for case-insensitive matching
    from_location = from_location.strip().casefold()
    to_location = to_location.strip().casefold()

    # Gathering entries for source and destination locations
    from_entries = [entry for country, cities in timezones_dict.items() for entry in cities if from_location in {country, entry[0], entry[1]}]
    to_entries = [entry for country, cities in timezones_dict.items() for entry in cities if to_location in {country, entry[0], entry[1]}]

    if not from_entries or not to_entries:
        return [f"**Error:** Could not find timezone information for one of the locations."]

    converted_times = []
    
    # Group destination cities by timezone
    cities_by_timezone = {}
    for to_city, _, to_tz, gmt_offset in to_entries:
        if to_tz not in cities_by_timezone:
            cities_by_timezone[to_tz] = []
        cities_by_timezone[to_tz].append((to_city, gmt_offset))

    for from_city, _, from_tz, _ in from_entries:
        tz = pytz.timezone(from_tz)
        current_date = datetime.now()  # Get current date

        # Parse the input time
        time_str = time_str.strip().lower()

        # Check if time is in 12-hour or 24-hour format and parse accordingly
        if 'am' in time_str or 'pm' in time_str:  # 12-hour format
            try:
                naive_time = datetime.strptime(time_str, "%I:%M%p")  # 5:34pm
            except ValueError:
                naive_time = datetime.strptime(time_str, "%I%p")  # 5pm
        else:  # 24-hour format (e.g., 17:00, 1700)
            try:
                naive_time = datetime.strptime(time_str, "%H:%M")  # 17:00
            except ValueError:
                naive_time = datetime.strptime(time_str, "%H%M")  # 1700

        # Replacing current date to preserve year, month, day while parsing time
        naive_time = naive_time.replace(year=current_date.year, month=current_date.month, day=current_date.day)

        aware_time = tz.localize(naive_time)  # Localize to source timezone

        for to_tz, cities in cities_by_timezone.items():
            # Only take the first city from each timezone group
            to_city, gmt_offset = cities[0]
            target_tz = pytz.timezone(to_tz)
            converted_time = aware_time.astimezone(target_tz)  # Convert to target timezone

            # Format the time in HH:MM format (24-hour time) for consistency
            from_time = aware_time.strftime('%H:%M')  # Always format 24-hour time as HH:MM
            to_time = converted_time.strftime('%H:%M')  # Always format 24-hour time as HH:MM

            # Check if the original time format was 12-hour (contains 'am' or 'pm')
            if 'am' in time_str or 'pm' in time_str:
                # If the time was in 12-hour format, respond in 12-hour format
                from_time = format_time(aware_time, format_12hr=True)
                to_time = format_time(converted_time, format_12hr=True)
            else:
                # If the time was in 24-hour format, keep the 24-hour format
                from_time = format_time(aware_time, format_12hr=False)
                to_time = format_time(converted_time, format_12hr=False)

            converted_times.append(f"**{from_time}** in {from_city.title()} is **{to_time}** in {to_city.title()}, {gmt_offset}")

    return list(set(converted_times))  # Remove duplicates


# Function to format a time object to 12-hour or 24-hour time
def format_time(time_obj, format_12hr=True):
    """Formats a datetime object into 12-hour or 24-hour format string."""
    if format_12hr:
        return time_obj.strftime('%I:%M%p').lower()  # Convert to 12-hour format (AM/PM)
    else:
        return time_obj.strftime('%H:%M')  # Convert to 24-hour format


# Initialize Discord bot with intents - probably should've been at the very top but cuck it we ball
# Also this was introduced in 2023 most likely, wasn't required for discord.py
intents = discord.Intents.default()
intents.message_content = True
intents.members = True # needed for mlist and jdlist commands
client = discord.Client(intents=intents)

# Placeholder for error logging channel and startup message channel
ERROR_CHANNEL_ID = 1305733544261455882  # error logs
STARTUP_CHANNEL_ID = 1305733544261455882  # channel ID for startup messages
PERIODIC_CHANNEL_ID = 1305815351069507604  # messages every 28m so heroku doesn't bonk us

# startup message
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
    # Change the bot's presence
    await client.change_presence(activity=discord.Game(name='time and money.'))

    # Send a startup message to the designated channel
    startup_channel = client.get_channel(STARTUP_CHANNEL_ID)
    if startup_channel:
        await startup_channel.send("I am now online.")
    
    # Start background task for periodic messages so Heroku doesn't go bonkers
    client.loop.create_task(send_periodic_message())


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    

    # mlist command
    if message.content.lower() == 'mlist':
        # Check if the user has permission
        #if message.author.id != 340485392434200576:
        #    await message.channel.send("You do not have permission to use this command.")
        #    return

        guild = message.guild  # Get the guild (server) where the message was sent
        
        # Create a list to hold member names and join dates
        member_list = []
        
        # Fetch all members using an async for loop
        async for member in guild.fetch_members():
            # Use nickname if available, otherwise use username
            nickname = member.nick if member.nick else member.name
            
            # Format the join date with shortened month names
            join_date = member.joined_at.strftime('%b %d, %Y') if member.joined_at else 'N/A'
            member_list.append((nickname, join_date, member.joined_at))  # Store join date for sorting

        # Sort members by join date (oldest first)
        member_list.sort(key=lambda x: x[2])  # Sort by the actual join date

        # Create a formatted string with bullet numbers
        formatted_member_list = "\n".join(f"{i + 1}. {nickname} [{join_date}]" for i, (nickname, join_date, _) in enumerate(member_list))

        # Create an embed for the response with dark red color
        embed = discord.Embed(
            title="Members in this server",
            description="Member | When they joined the server\n" + formatted_member_list,  # Added clarification
            color=discord.Color.dark_red()  # Change color to dark red
        )

        # Send the embed in the channel
        await message.channel.send(embed=embed)

    

    # Checking if the message content is the trigger for listing join dates
    if message.content.lower() == 'jdlist':
        # Check if the user has permission
        #if message.author.id != 340485392434200576:
            #await message.channel.send("You do not have permission to use this command.")
            #return

        guild = message.guild  # Get the guild (server) where the message was sent
        
        # Create a list to hold member names and account creation dates
        account_list = []
        
        # Fetch all members using an async for loop
        async for member in guild.fetch_members():
            # Use nickname if available, otherwise use username
            nickname = member.nick if member.nick else member.name
            
            # Format the account creation date with shortened month names
            account_creation_date = member.created_at.strftime('%b %d, %Y') if member.created_at else 'N/A'
            account_list.append((nickname, account_creation_date, member.created_at))  # Store nickname, account creation date, and actual date

        # Sort members by account creation date (oldest first)
        account_list.sort(key=lambda x: x[2])  # Sort by the actual account creation date

        # Create a formatted string with bullet numbers
        formatted_account_list = "\n".join(f"{i + 1}. {nickname} [{account_creation_date}]" for i, (nickname, account_creation_date, _) in enumerate(account_list))

        # Create an embed for the response with dark red color
        embed = discord.Embed(
            title="Members' Account Creation Dates",
            description=formatted_account_list,
            color=discord.Color.dark_red()  # Change color to dark red
        )

        # Send the embed in the channel
        await message.channel.send(embed=embed)

    # weather stuff
    if message.content.lower().startswith('weather'):
        # Get the content after 'weather'
        query = message.content[7:].strip()
        
        if not query:
            await message.channel.send("Please provide a location or mention a user. Example: weather London,UK or weather @username")
            return

        # Check if it's a user mention
        if query.startswith('<@') and query.endswith('>'):
            # Extract user ID from mention
            user_id = query[2:-1]  # Remove <@ and >
            if user_id.startswith('!'): # Handle nicknames
                user_id = user_id[1:]
            
            # Look up user's location in mapping
            if user_id in USER_LOCATION_MAPPING:
                username, location = USER_LOCATION_MAPPING[user_id]
            else:
                await message.channel.send("This user's location isn't registered in my database.")
                return
        else:
            # Use the provided location directly
            location = query

        try:
            async with aiohttp.ClientSession() as session:
                # Get coordinates for location
                geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={WEATHER_API_KEY}"
                async with session.get(geocoding_url) as response:
                    if response.status != 200:
                        await message.channel.send("Sorry, I couldn't find that location.")
                        return
                    
                    geocode_data = await response.json()
                    if not geocode_data:
                        await message.channel.send("Sorry, I couldn't find that location.")
                        return

                    lat = geocode_data[0]['lat']
                    lon = geocode_data[0]['lon']
                    location_name = geocode_data[0]['name']
                    country = geocode_data[0]['country']

                # Get weather data
                weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
                async with session.get(weather_url) as response:
                    if response.status != 200:
                        await message.channel.send("Sorry, I couldn't fetch the weather data.")
                        return
                    
                    weather_data = await response.json()

            # Extract weather information
            temperature = round(weather_data['main']['temp'])
            condition = weather_data['weather'][0]['description']
            temp_max = round(weather_data['main']['temp_max'])
            temp_min = round(weather_data['main']['temp_min'])

            # Prepare weather message
            if query.startswith('<@'):
                # If it was a user mention, include their username
                weather_message = (
                    f"For **{username}**, it's **{condition}** and **{temperature} °C** in **{location_name}**, {country} today. "
                    f"They can expect highs of {temp_max} °C and lows of {temp_min} °C."
                )
            else:
                weather_message = (
                    f"It's **{condition}** and **{temperature} °C** in **{location_name}**, {country} today. "
                    f"Expect highs of {temp_max} °C and lows of {temp_min} °C."
                )
            
            await message.channel.send(weather_message)

        except Exception as e:
            await message.channel.send(f"An error occurred while fetching weather data: {str(e)}") 

  # DM forwarding, sends any content (text or attachments) sent to bot's DM - to specified channel  
  # Check if the message is in a DM (Direct Message)
    if isinstance(message.channel, discord.DMChannel):
        target_channel = client.get_channel(1306617117528952955)  # Replace with the target channel ID

        # Check if the target channel exists
        if target_channel:
            # Send the content of the DM (if there's any text)
            embed = discord.Embed(
                title="New DM Received",
                description=message.content if message.content else "[No Text]",
                color=discord.Color.dark_teal()  # Use a green color for DM notifications
            )
            embed.add_field(name="From", value=f"{message.author} (ID: {message.author.id})", inline=False)
            
            # Forward the message embed to the target channel
            await target_channel.send(embed=embed)

            # Forward any attachments (images, files)
            if message.attachments:
                for attachment in message.attachments:
                    await target_channel.send(f"Attachment: {attachment.url}")
        else:
            print("Target channel not found.")
    

    # formerly listserv command: Only accessible by the bot owner
    # lists all servers the bot is in

    if message.content.lower() in ["ww -guilds", "worldwise -guilds"]:
        if message.author.id != 340485392434200576: #admin ID
            await message.channel.send("You do not have permission to use this command.")
            return

        guilds = client.guilds
        if guilds:
            guild_list = "\n".join(
                [f"- **{guild.name}** (ID: {guild.id}, Members: **{guild.member_count}**)" for guild in guilds]
            )
            await message.channel.send(f"**The bot is in the following servers:**\n{guild_list}")
        else:
            await message.channel.send("**The bot is not in any servers.**")
        return

    # lists some basic server information - commented out admin restrictor for now 
    if message.content.lower() in ["serverinfo", "svinfo"]:
        #if message.author.id != 340485392434200576: #admin ID
            #await message.channel.send("You do not have permission to use this command.")
            #return

        guild = message.guild
        if guild:
            embed = discord.Embed(title=f"Server Info for **{guild.name}**", color=discord.Color.blue())
            embed.add_field(name="Server ID", value=guild.id, inline=False)
            embed.add_field(name="Owner", value="Who knows?", inline=False)
            embed.add_field(name="Member Count", value=guild.member_count, inline=False)
            embed.add_field(name="Boost Count", value=guild.premium_subscription_count, inline=False)
            embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=False)
            embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=False)
            embed.add_field(name="Created At", value=guild.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
            
            # Set server banner if available
            #if guild.banner:
            #    embed.set_image(url=guild.banner.url)

            # Set server icon as thumbnail if available
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)

            await message.channel.send(embed=embed)
        else:
            await message.channel.send("This command must be run in a server.")

    #Large read-me alike. Meant to have complete instructions no one will ever read.
    elif message.content.lower().startswith(('ww -readme', 'worldwise -readme', 'ww -rm')):
        embed = get_readme_embed()  # Get the README embed
        await message.channel.send(embed=embed)

    # Handle 'convert' or variations like 'Convert' and 'conv' (short response)
    if message.content.lower().startswith('convert ') or message.content.lower().startswith('conv '):
        await handle_conversion(message, full_response=False)

    # Handle 'convertfull' or variations like 'Convertfull' and 'convf' (full response)
    elif message.content.lower().startswith('convertfull') or message.content.lower().startswith('convf'):
        await handle_conversion(message, full_response=True)

    elif message.content.lower().startswith('whelp'):
        embed = get_weather_help_embed()  # Get the weather help embed
        await message.channel.send(embed=embed)
    
    # Handle 'chelp' for showing syntax and examples
    elif message.content.lower().startswith('chelp'):
        embed = get_currency_help_embed()  # Get the currency help embed
        await message.channel.send(embed=embed)

# Adding this to the on_message handler to handle the `time` command
    elif message.content.lower().startswith('time '):
        await handle_time_command(message)

    # Handle 'clist' for listing supported currencies
    elif message.content.lower().startswith('clist'):
        embed = get_currency_list_embed(SUPPORTED_CURRENCIES, CURRENCY_NAMES)  # Get the currency list embed
        await message.channel.send(embed=embed)


    # Handle 'thelp' for listing supported timezones
    elif message.content.lower().startswith('thelp'):
        embed = get_time_help_embed()  # Get the time help embed
        await message.channel.send(embed=embed)
    
    # Handle 'tlist' command
    elif message.content.lower().startswith('tlist'):
        embed = get_timezone_list_embed(timezones_dict, COUNTRY_ABBREVIATIONS)
        await message.channel.send(embed=embed)


# Handle 'time' command
    elif message.content.lower().startswith('time '):
        location_name = message.content[5:].strip()
        times = get_current_time(location_name)
        if times:
            # Capitalize only the first letter of each word in the country name
            formatted_times = [
                time.replace(location_name.upper(), location_name.title()) for time in times
            ]
            await message.channel.send("\n".join(formatted_times))
        else:
            await message.channel.send(
                "Timezone(s) unsupported - type 'tlist' for supported timezones and cities."
            )
    
# Handle 'timec' command
    elif message.content.lower().startswith('timec ') or message.content.lower().startswith('timeconvert'):
        await handle_timec_command(message)

# function to fetch time for a specific user from user_timezone_mapping
async def handle_time_command(message):
    mentioned_users = message.mentions  # Get mentioned users

    if mentioned_users:
        responses = []

        for user in mentioned_users:
            user_data = USER_TIMEZONE_MAPPING.get(user.id)

            if not user_data:
                responses.append(f"No timezone information found for **{user.name}**.")
                continue

            username, city_abbreviation = user_data

            # Find the city, timezone, and GMT offset
            for country, cities in timezones_dict.items():
                for city, abbreviation, timezone, gmt_offset in cities:
                    if city_abbreviation == abbreviation:
                        tz = pytz.timezone(timezone)
                        city_time = datetime.now(tz)
                        formatted_time = city_time.strftime('%I:%M %p')
                        responses.append(
                            f"It's **{formatted_time}** for **{username}**, in {city.title()}, {country.title()}, {gmt_offset}."
                        )
                        break
                else:
                    continue
                break
            else:
                responses.append(f"City abbreviation `{city_abbreviation}` for **{username}** not found in timezones.")

        await message.channel.send("\n".join(responses))

    else:
        location_name = message.content[5:].strip()
        times = get_current_time(location_name)
        if times:
            formatted_times = [
                time.replace(location_name.upper(), location_name.title()) for time in times
            ]
            await message.channel.send("\n".join(formatted_times))
        else:
            await message.channel.send(
                "Timezone(s) unsupported - type 'tlist' for supported timezones and cities."
            )

# allows converting user - user time 
# fixer-upper with ye olde AI to support parsing for 24 hour format with ":"
async def handle_timec_command(message):
    parts = message.content[6:].split(' to ')
    if len(parts) == 2:
        try:
            time_str, origin_location = parts[0].rsplit(' ', 1)
            destination_location = parts[1].strip()

            mentioned_users = message.mentions
            if mentioned_users:
                if len(mentioned_users) == 2:
                    from_user, to_user = mentioned_users

                    from_user_data = USER_TIMEZONE_MAPPING.get(from_user.id)
                    to_user_data = USER_TIMEZONE_MAPPING.get(to_user.id)

                    if not from_user_data or not to_user_data:
                        await message.channel.send("Timezone information for one or both users is missing.")
                        return

                    from_username, from_city_abbreviation = from_user_data
                    to_username, to_city_abbreviation = to_user_data

                    converted_times = convert_time(time_str, from_city_abbreviation, to_city_abbreviation)

                    if converted_times:
                        # Retrieve full city names for both users
                        from_city_name = next(
                            (city.title() for country, cities in timezones_dict.items() for city, abbreviation, _, _ in cities if abbreviation == from_city_abbreviation),
                            from_city_abbreviation.upper()
                        )
                        to_city_name = next(
                            (city.title() for country, cities in timezones_dict.items() for city, abbreviation, _, _ in cities if abbreviation == to_city_abbreviation),
                            to_city_abbreviation.upper()
                        )

                        # Correct response formatting (no city repeated)
                        response = f"{time_str} for **{from_username}** in {from_city_name}, is "
                        response += f"{converted_times[0].split(' is ')[1]} for **{to_username}**."
                        await message.channel.send(response)
                        return

                    else:
                        await message.channel.send("Could not convert time between the mentioned users.")
                        return

            # If no mentions, use the location-based conversion
            converted_times = convert_time(time_str, origin_location, destination_location)

            if converted_times:
                # Send the regular conversion response
                await message.channel.send("\n".join(converted_times))
            else:
                await message.channel.send(
                    "Timezone(s) unsupported - type 'tlist' for supported timezones and cities."
                )
        except ValueError:
            await message.channel.send(
                "Invalid syntax. Use `timec Xam/pm <origin location> to <destination location>` or `timec <time> @user1 to @user2`."
            )
    else:
        await message.channel.send(
            "Invalid syntax. Use `timec <time> <origin location> to <destination location>` or `timec <time> @user1 to @user2`."
        )

# actual conversion happens here (hopefully)
async def handle_conversion(message, full_response):
    try:
        parts = message.content.split()
        
        # Ensure correct number of elements
        if len(parts) < 5:
            await message.channel.send("Invalid syntax. Use `conv [amount] [from_currency] to [target_currency]`.")
            return

        amount = parts[1]
        from_currency = parts[2].upper()
        to_currency = parts[4].upper()

        # Validate currencies before processing
        if from_currency not in SUPPORTED_CURRENCIES or to_currency not in SUPPORTED_CURRENCIES:
            supported_currencies = "\n".join(
                f"{i+1}. {CURRENCY_NAMES[c][1]} ({c})" for i, c in enumerate(SUPPORTED_CURRENCIES)
            )
            await message.channel.send(
                f"**Unsupported currency. Supported currencies are:**\n{supported_currencies}\n\n"
                "**To use the currency converter, type:**\n`conv [amount] [from_currency] to [target_currency]`\n"
                "`convf [amount] [from_currency] to [target_currency]` will return more information with source."
            )
            return

        # Convert amount to float
        amount = float(amount)
        
        rate, high_30, low_30, average_30, change_30, url = get_exchange_rate(from_currency, to_currency)

        if rate:
            converted_amount = amount * rate

            from_currency_singular, from_currency_plural = CURRENCY_NAMES[from_currency]
            to_currency_singular, to_currency_plural = CURRENCY_NAMES[to_currency]

            from_currency_name = from_currency_singular if amount == 1 else from_currency_plural
            to_currency_name = to_currency_singular if round(converted_amount, 2) == 1.00 else to_currency_plural

            if full_response:
                await message.channel.send(
                    f"**{amount} {from_currency_name}** is approximately **{converted_amount:.2f} {to_currency_name}** at an exchange rate of **{rate:.4f}**.\n"
                    f"In the past 30 days, the **high** was {high_30}, the **low** was {low_30}, with an **average** of {average_30} and a **change** of {change_30}%.\n"
                    f"Click here for additional info: [source]({url})"
                )
            else:
                await message.channel.send(
                    f"**{amount} {from_currency_name}** is approximately **{converted_amount:.2f} {to_currency_name}** at an exchange rate of **{rate:.4f}**."
                )
        else:
            await send_error("Exchange rate or historical data not found.", message)
    except Exception as e:
        await send_error(f"Error: {str(e)}", message)

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

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

client.run(DISCORD_TOKEN)
