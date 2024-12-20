import discord

sections = [
    {
        "title": "Worldwise Bot Help",
        "description": "This guide covers all the **features** of the Worldwise Bot.\n"
                       "This is the result of an over-engineered project for the *mild convenience* of not having to switch tabs.\n\n"
                       "All commands are case-*in*sensitive.\n\n"
                       "**Use the selector below to navigate to what you need help with.**",
        "inline": False,
        "color": discord.Color.dark_teal(),
        "fields": []
    },
    {
        "title": "💰 Currency Conversion Help",
        "description": "Use the currency conversion features to convert between different currencies with ease. Here's how you can use them:",
        "color": discord.Color.dark_teal(),
        "fields": [
            {
                "name": "1. Basic Currency Conversion (conv or convert)",
                "value": "`conv [amount] [from_currency] to [target_currency]`\n"
                          "Example 1: `conv 100 USD to CAD`\n"
                          "Example 2: `convert 50 EUR to USD`\n\n"
                          "This command provides a short response with the conversion rate.\n\n",
                "inline": False
            },
            {
                "name": "2. Detailed Currency Conversion (convf or convertfull)",
                "value": "`convf [amount] [from_currency] to [target_currency]`\n"
                          "Example 1: `convf 100 USD to CAD`\n"
                          "Example 2: `convertfull 50 EUR to USD`\n\n"
                          "This command gives you detailed information, including:\n"
                          "- Conversion rate\n"
                          "- 30-day high, low, average, and change\n"
                          "- Source link for the data\n\n",
                "inline": False
            },
            {
                "name": "3. Currency List (clist)",
                "value": "Type `clist` to view all supported currencies.\n"
                          "The list shows full names and abbreviations, so you can use either.",
                "inline": False
            },
        ]
    },
    {
        "title": "🕰️ Timezone Help",
        "description": "Use the time-related features to check the current time or convert time between different locations.",
        "color": discord.Color.dark_teal(),
        "fields": [
            {
                "name": "1. Current Time (time)",
                "value": "`time <location>` - Provides the current time for the specified location.\n"
                          "Examples:\n"
                          "- `time MY` (Malaysia)\n"
                          "- `time yyz` (Toronto)\n"
                          "- `time newzealand`\n"
                          "- `time Malaysia`\n\n"
                          "If the country name is *two words*, like United States, _delete the space in-between_ to use it. i.e. unitedstates or newzealand.\n"
                          "You can use full city and country names or abbreviations from all the supported regions found in `tlist`.",
                "inline": False
            },
            {
                "name": "2. User Time (time @username)",
                "value": "`time @username` - Shows the current time for the mentioned user, based on their configured city.\n"
                          "Example: `time @Zer0`.\n\n"
                          "This works when you directly @mention the user.\n"
                          "Ask <@340485392434200576> to change/add your region.",
                "inline": False
            },
            {
                "name": "3. Time Zone Conversion (timec or timeconvert)",
                "value": "`timec [time] [from_location] to [to_location]`\n"
                          "Example 1: `timec 5pm yyz to US`\n"
                          "Example 2: `timec 1:23am dac to plu`\n"
                          "Example 3: `timec 16:00 Hamilton to AU`\n\n"
                          "You can use both full location names or abbreviations.\n\n"
                          "If a country has multiple time zones, all timezones will be listed.\n\n"
                          "**Supported time formats:**\n"
                          "- 12-hour format: `4:00pm`, `4pm`\n"
                          "- 24-hour format: `16:00`, `1600`\n"
                          "- Military time: `1600`\n",
                "inline": False
            },
            {
                "name": "4. User-to-User Time Conversion (timec)",
                "value": "`timec [time] @from_user to @to_user`\n"
                          "Example: `timec 2pm @Zer0 to @strangyyy`\n\n"
                          "This command converts time from one user's region to another's based on their allocated region.",
                "inline": False
            },
            {
                "name": "5. Supported Timezones (tlist)",
                "value": "Type `tlist` to view all supported regions and cities with their corresponding timezone codes.\n"
                          "The list shows both full city names and abbreviations.\n\n"
                          "The abbreviations in this list will work accurately with all time-related commands.\n",
                "inline": False
            },
        ]
    },
    {
        "title": "🌩️ Weather Help",
        "description": "Fetching weather information for any location worldwide using OpenWeather.",
        "color": discord.Color.dark_teal(),
        "fields": [
            {
                "name": "1. Weather today",
                "value": "`weather <city>,<country_abbreviation>` - Provides weather information for the specified location.\n"
                          "Examples:\n"
                          "- `weather Hamilton, NZ` (New Zealand)\n"
                          "- `weather Malaysia`\n"
                          "Best to specify city followed by country abbreviation for accurate results.",
                "inline": False
            },
            {
                "name": "2. Weather @user",
                "value":  "`weather <@username>` - Provides weather information for the mentioned user, based on their allocated region.\n"
                          "- Example: `weather @strangyyy`\n",
                "inline": False
            },
        ]
    },
    {
        "title": "🔤 Translate Help",
        "description": "`translate <text>` - Translates the provided text to English.",
        "color": discord.Color.dark_teal(),
        "fields": []
    },
    {
        "title": "💻 Server Info",
        "description": "Type `svinfo` or `serverinfo` for information about the server.\n"
                       "This includes:\n"
                       "- Server ID\n"
                       "- Owner\n"
                       "- Member count\n"
                       "- Boost count\n"
                       "- Text channels\n"
                       "- Voice channels\n"
                       "- Server creation date",
        "color": discord.Color.dark_teal(),
        "fields": []
    },
    {
        "title": "🌍 Server List",
        "description": "Type `ww -guilds` or `worldwise -guilds` to see **all the servers** the bot is in (including number of users in listed servers).\n"
                       "**Admin only.**",
        "color": discord.Color.dark_teal(),
        "fields": []
    },
    {
        "title": "👥 Members List",
        "description": "Type `mlist` to see all **members** and **when they joined the server.**",
        "color": discord.Color.dark_teal(),
        "fields": []
    },
    {
        "title": "👥 Account Creation Dates",
        "description": "Type `jdlist` to see all **members** in the server and their **account creation dates.**",
        "color": discord.Color.dark_teal(),
        "fields": []
    },
    {
        "title": "📜 All Commands",
        "description": "Here is a summary of all available commands:",
        "color": discord.Color.dark_teal(),
        "fields": [
            {
                "name": "Currency Conversion Commands",
                "value": "`conv [amount] [currency] to [target_currency]` - Convert currency.\n"
                         "`convf [amount] [currency] to [target_currency]` - Detailed conversion.\n"
                         "`clist` - List all supported currencies.",
                "inline": False
            },
            {
                "name": "Timezone Commands",
                "value": "`time <location>` - Get current time for a location.\n"
                         "`time @username` - Get current time for the mentioned user.\n"
                         "`timec [time] [origin] to [destination]` - Convert time between locations.\n"
                         "`tlist` - List all supported timezones.",
                "inline": False
            },
            {
                "name": "Weather Commands",
                "value": "`weather <city>,<country_abbreviation>` - Get weather for a location.\n"
                         "`weather <@username>` - Get weather for the mentioned user.",
                "inline": False
            },
            {
                "name": "Translation Command",
                "value": "`translate <text>` - Translate the provided text to English.",
                "inline": False
            },
            {
                "name": "Server Info Commands",
                "value": "`svinfo` or `serverinfo` - Get server information.\n"
                         "`ww -guilds` or `worldwise -guilds` - List all servers the bot is in **(Admin only)**.\n"
                         "`mlist` - List all members and their join dates.\n"
                         "`jdlist` - List all members and their account creation dates.",
                "inline": False
            },
            {
                "name": "For Help or Additions",
                "value": "Ping <@340485392434200576> for further assistance or suggestions.",
                "inline": False
            },
        ],
    }
]       


# Function to create an embed from a section
def create_embed(section):
    embed = discord.Embed(
        title=section["title"],
        description=section["description"],
        color=section["color"]
    )
    for field in section["fields"]:
        embed.add_field(name=field["name"], value=field["value"], inline=field["inline"])
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
