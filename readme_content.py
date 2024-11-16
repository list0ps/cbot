import discord

def get_readme_embed():
    embed = discord.Embed(
        title="Worldwise Bot Full Readme",
        description="Welcome to the full readme! This is your go-to guide for understanding and using all the features of the Worldwise Bot.\n"
                    "This is the result of over-engineering currency and time conversions for the mild convenience of not having to switch tabs.\n\n"
                    "All commands are case-*in*sensitive.",
        color=discord.Color.dark_teal()  # Set color to whatever eh
    )

    # Currency Conversion Help
    embed.add_field(
        name="💰 Currency Conversion Help",
        value="Use the currency conversion features to convert between different currencies with ease. "
              "Here's how you can use them:",
        inline=False
    )

    embed.add_field(
        name="1. Basic Currency Conversion (conv or convert)",
        value="`conv [amount] [from_currency] to [target_currency]`\n"
              "Example 1: `conv 100 USD to CAD`\n"
              "Example 2: `convert 50 EUR to USD`\n\n"
              "This command provides a short response with the conversion rate.\n\n",
        inline=False
    )

    embed.add_field(
        name="2. Detailed Currency Conversion (convf or convertfull)",
        value="`convf [amount] [from_currency] to [target_currency]`\n"
              "Example 1: `convf 100 USD to CAD`\n"
              "Example 2: `convertfull 50 EUR to USD`\n\n"
              "This command gives you detailed information, including:\n"
              "- Conversion rate\n"
              "- 30-day high, low, average, and change\n"
              "- Source link for the data\n\n",
        inline=False
    )

    embed.add_field(
        name="3. Currency List (clist)",
        value="Type `clist` to view all supported currencies.\n"
              "The list shows full names and abbreviations, so you can use either.",
        inline=False
    )

    # Timezone Help
    embed.add_field(
        name="🕰️ Timezone Help",
        value="Use the time-related features to check the current time or convert time between different locations.",
        inline=False
    )

    embed.add_field(
        name="1. Current Time (time)",
        value="`time <location>` - Provides the current time for the specified location.\n"
              "Examples:\n"
              "- `time KL` (Kuala Lumpur)\n"
              "- `time MY` (Malaysia)\n"
              "- `time yyz` (Toronto)\n"
              "- `time newzealand`\n"
              "- `time Malaysia`\n\n"
              "If the country name is two words, like United States, delete the space in-between to use it. i.e. unitedstates or newzealand.\n"
              "You can use full city and country names or abbreviations from all the supported regions found in `tlist`.",
        inline=False
    )

    embed.add_field(
        name="2. User Time (time @username)",
        value="`time @username` - Shows the current time for the mentioned user, based on their configured city.\n"
              "Example: `time @Zer0`.\n\n"
              "This works when you directly mention or @ping the user. If a user has their city allocated to them, the bot will show the time accordingly.\n"
              "Currently, users can't configure their own locations with a command. Ask <@340485392434200576> to change/add your region for support.",
        inline=False
    )

    embed.add_field(
        name="3. Time Zone Conversion (timec or timeconvert)",
        value="`timec [time] [from_location] to [to_location]`\n"
              "Example 1: `timec 6pm KL to Australia`\n"
              "Example 2: `timec 5pm yyz to US`\n"
              "Example 3: `timec 1am dac to plu`\n"
              "Example 4: `timec 2am Hamilton to AU`\n\n"
              "You can use either full location names or abbreviations. The bot will show you the time converted to the destination time zone.\n\n"
              "If a country has multiple time zones, all of them will be listed for that country.\n\n"
              "**Supported time formats:**\n"
              "- 12-hour format: `4:00pm`, `4pm`\n"
              "- 24-hour format: `16:00`, `1600`\n"
              "- Military time: `1600`\n"
              "- Both minutes and hour are supported: `4:23pm` or `1623`",
        inline=False
    )

    embed.add_field(
        name="4. User-to-User Time Conversion (timec)",
        value="`timec [time] @from_user to @to_user`\n"
              "Example: `timec 2pm @Zer0 to @strangyyy`\n\n"
              "This command converts time from one user's region to another's based on their allocated region.",
        inline=False
    )

    embed.add_field(
        name="5. Supported Timezones (tlist)",
        value="Type `tlist` to view all supported regions and cities with their corresponding timezone codes.\n"
              "The list shows both full city names and abbreviations.\n\n"
              "The abbreviations in this list will work accurately with all time-related commands.\n",
        inline=False
    )

    # Weather Help
    embed.add_field(
        name="🌩️ Weather Help",
        value="Fetching weather information for any location worldwide using OpenWeather.",
        inline=False
    )
    embed.add_field(
        name="1. Weather today (weather)",
        value="`weather <city>,<country_abbreviation>` - Provides weather information for the specified location.\n"
              "Examples:\n"
              "- `weather Hamilton, NZ` (New Zealand)\n"
              "- `weather Malaysia` \n"
              "Abbreviation and region codes work too such as `weather NZ` but returns highly inaccurate responses. \n"
              "Best to specify city followed by country abbreviation.",
        inline=False
    )

    # Server Info
    embed.add_field(
        name="💻 Server Info (svinfo or serverinfo)",
        value="Type `svinfo` or `serverinfo` to get information about the server where the bot is active.\n"
              "This includes:\n"
              "- Server ID\n"
              "- Owner\n"
              "- Member count\n"
              "- Boost count\n"
              "- Text channels\n"
              "- Voice channels\n"
              "- Server creation date",
        inline=False
    )

    # Worldwise Bot Guilds Info
    embed.add_field(
        name="🌍 Server List (ww -guilds or worldwise -guilds)",
        value="Type `ww -guilds` or `worldwise -guilds` to see all the servers the bot is in (including number of users in listed servers).\n"
              "**Admin only.**\n",
        inline=False
    )

    # Members List
    embed.add_field(
        name="👥 Members List (mlist)",
        value="Type `mlist` to see all the members and when they joined the server.\n",
        inline=False
    )

    # Account Creation Dates
    embed.add_field(
        name="👥 Account Creation Dates (jdlist)",
        value="Type `jdlist` to see all the members in the server and their account creation dates.\n",
        inline=False
    )

    # Final Notes and Contact Info
    embed.add_field(
        name="For Help or Additions",
        value="If you need further assistance or would like to suggest an addition to the bot, feel free to mention me: <@340485392434200576>.\n"
              "You can also check the full source code and more info at: [Worldwise Bot GitHub](https://github.com/list0ps/Worldwise).",
        inline=False
    )

    return embed 

def get_weather_help_embed():
    embed = discord.Embed(
        title="Weather Information Help",
        description="Learn how to use the weather command.",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Usage",
        value="`weather [city_name],[country_abbreviation]`\n"
              "Example: `weather Hamilton, NZ`\n"
              "Displays current weather, temperatures, and conditions.",
        inline=False
    )
    embed.add_field(
        name="Note",
        value="You can use this command in both server channels and private messages!",
        inline=False
    )
    return embed

def get_currency_help_embed():
    embed = discord.Embed(
        title="Currency Conversion Help",
        description="Learn how to use the currency conversion commands effectively.",
        color=discord.Color.dark_green()
    )
    embed.add_field(
        name="1. Basic Conversion",
        value="`conv [amount] [from_currency] to [target_currency]`\n"
              "Example: `conv 100 USD to CAD`\n"
              "Provides a short response with the conversion rate.",
        inline=False
    )
    embed.add_field(
        name="2. Full Conversion with Details",
        value="`convf [amount] [from_currency] to [target_currency]`\n"
              "Example: `convf 100 USD to CAD`\n"
              "Provides a detailed response including 30-day high, low, average, change, and source link.",
        inline=False
    )
    embed.add_field(
        name="Additional Commands",
        value="Type `clist` to view all supported currencies."
              "You can make these conversions __privately__ too! **Slide into my DMs ;)**",
        inline=False
    )
    return embed

def get_time_help_embed():
    embed = discord.Embed(
        title="Time Zone Help",
        description="Only works with supported regions!",
        color=discord.Color.dark_blue()
    )
    embed.add_field(
        name="1. Current Time",
        value="`time <location>` - Tells you the current time for the region.\n"
              "Example: `time KL`, `time MY`, or `time Malaysia`.\n",
        inline=False
    )
    embed.add_field(
        name="2. User Time",
        value="`time @username` - Tells you what time it is for the user you mention.\n"
              "Example: `time @Zer0`.",
        inline=False
    )
    embed.add_field(
        name="3. Time Zone Conversion",
        value="`timec` - Converts time from one region to another.\n"
              "Example: `timec 6pm KL to Australia`, or `timec 2pm Hamilton to AU`.\n"
              "If a country has multiple time zones, all zones will be listed.\n",
        inline=False
    )
    embed.add_field(
        name="4. User-to-User Time Conversion",
        value="`timec` - Converts time from one user's region to another's.\n"
              "Example: `timec 2pm @Zer0 to @strangyyy`.",
        inline=False
    )
    embed.add_field(
        name="What's supported?",
        value="Type `tlist` to view all supported regions with codes for easy typing.\n"
              "You can make these conversions __privately__ too! **Slide into my DMs ;)**",
        inline=False
    )
    return embed

def get_currency_list_embed(supported_currencies, currency_names):
    embed = discord.Embed(
        title="Supported Currencies",
        description="A complete list of supported currencies for the converter.",
        color=discord.Color.dark_green()
    )
    currency_list = "\n".join(
        f"{i + 1}. {currency_names[c][1]} ({c})" for i, c in enumerate(supported_currencies)
    )
    embed.add_field(
        name="Currency List",
        value=currency_list,
        inline=False
    )
    embed.add_field(
        name="How to Use",
        value="`conv [amount] [from_currency] to [target_currency]`\n"
              "Example: `conv 100 USD to CAD`\n\n"
              "`convf` returns more information with source.\n",
        inline=False
    )
    embed.add_field(
        name="Want to Add a Currency?",
        value="Contact <@340485392434200576>.",
        inline=False
    )
    return embed


def get_timezone_list_embed(timezones_dict, country_abbreviations):
    embed = discord.Embed(
        title="Supported Timezones",
        description="A list of countries and their cities you can convert between. Yes you can use abbreviations.",
        color=discord.Color.dark_blue()
    )

    country_number = 1
    processed_countries = set()  # Keep track of processed countries

    # List of countries to include
    countries_to_include = [
        'newzealand', 'australia', 'bangladesh', 'malaysia', 'mauritius',
        'canada', 'unitedstates', 'england', 'germany', 'france',
        'italy', 'netherlands', 'denmark', 'finland', 'switzerland',
        'luxembourg', 'philippines', 'singapore', 'japan'
    ]

    for country in countries_to_include:
        # Check if the country exists in the timezones_dict
        if country in timezones_dict:
            cities = timezones_dict[country]
            # Get the full country name and abbreviation
            full_country_name = country.title()  # Capitalize the country name
            abbreviation = country_abbreviations.get(country, "").upper()  # Get abbreviation

            # Create the country heading with number and abbreviation
            country_heading = f"{country_number}. {full_country_name} ({abbreviation})"

            # Create the cities list
            cities_list = ", ".join([f"{city.title()} ({code.upper()})" for city, code, _, _ in sorted(cities)])

            # Add the field to the embed
            embed.add_field(name=country_heading, value=cities_list, inline=False)
            country_number += 1

            # Check if we have reached the limit of 25 fields
            if country_number > 25:
                break  # Stop adding fields if we exceed the limit

    # Add the contact information
    embed.add_field(
        name="Want to Add a City?",
        value="Contact <@340485392434200576>.",
        inline=False
    )

    return embed
