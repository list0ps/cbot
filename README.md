
# Worldwise Discord Bot

This bot was designed to be used in my personal discord server with an exceedingly international group of friends. It's built entirely using python and the discord.py library, with a tinge of web scraping and API integration (also some json architecture).

Though most of the bot's functionality is easily attainable through a quick google search, it served the purpose of my hyperfixiative means of stress relief over a week long project. 



## Commands Overview

### Functional Commands

| Command                          | Description                                                                                     |
|----------------------------------|-------------------------------------------------------------------------------------------------|
| `conv [amount] [from_currency] to [target_currency]` | Converts a specified amount from one currency to another.                                      |
| `convf [amount] [from_currency] to [target_currency]`| Provides detailed currency conversion information, including rates and historical data.        |
| `time <location>`               | Displays the current time for the specified location.                                          |
| `time @username`                | Shows the current time for the mentioned user based on their configured city.                 |
| `timec [time] [from_location] to [to_location]`     | Converts time from one location to another.                                                   |
| `timec [time] @from_user to @to_user`               | Converts time from one user's region to another's based on their allocated region.            |
| `weather <city>,<country_abbreviation>`              | Provides current weather information for the specified location.                               |
| `weather @username`             | Fetches weather information for the mentioned user based on their allocated region.           |
| `translate <text>`              | Translates the provided text to English.                                                      |

### Help and Server Commands

| Command                          | Description                                                                                     |
|----------------------------------|-------------------------------------------------------------------------------------------------|
| `svinfo` or `serverinfo`       | Displays information about the server where the bot is active.                                |
| `ww -guilds` or `worldwise -guilds` | Lists all servers the bot is in, including the number of users (Admin only).                |
| `mlist`                          | Shows all members in the server and when they joined.                                        |
| `jdlist`                         | Lists all members in the server along with their account creation dates.                      |
| `tlist`                          | Lists all supported time zones and cities with their corresponding codes.                     |
| `clist`                          | Lists all supported currencies along with their full names and abbreviations.                 |

## How the Worldwise Bot Works

The Worldwise Bot operates by integrating various APIs and data sources to provide real-time information on currency conversion, time zones, and weather conditions. Here's a brief overview of how each function is achieved:

### Currency Conversion
The bot utilizes web scraping techniques to fetch the latest exchange rates from reliable financial websites. When a user requests a currency conversion, the bot retrieves the current rate and performs the necessary calculations to provide accurate conversion results. Additionally, it offers detailed information such as historical data, high and low rates over the past 30 days, and links to the source of the data.

### Time Zone Management
To manage time zones effectively, the bot maintains a comprehensive mapping of cities, countries, and their corresponding time zones. When a user queries the current time for a specific location or requests a time conversion between two locations, the bot uses this mapping to calculate and return the correct time, taking into account any differences in time zones.

### Weather Information
For weather updates, the bot leverages the OpenWeather API to fetch current weather data based on user-provided locations. Users can inquire about the weather for specific cities or even for other users based on their registered locations. The bot processes the API response to extract relevant weather details, such as temperature, conditions, and forecasts, and presents this information in a user-friendly format.

### Translation Services
The translation functionality is implemented using web scraping techniques to access Google Translate. When a user issues the `translate <text>` command, the bot constructs a URL for the translation request and sends an HTTP GET request with appropriate headers to mimic a browser request. The response is parsed to extract the translated text, which is then sent back to the user. This process is encapsulated in a try-except block to handle potential errors gracefully, ensuring that users receive accurate translations.
