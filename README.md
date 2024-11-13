# Time & Currency Conversion Discord Bot

This is a Discord bot designed to provide time zone conversions, currency conversions, and periodic messages to prevent dyno sleeping on Heroku. The bot supports various commands for users to get the current time for a given location, convert times between time zones, and convert currencies with detailed information.

## Features
- **Time Zone Conversion:** Convert time from one location to another, including support for multiple time zones within a country.
- **Time Lookup:** Simply gives you the time of a supported location you ask for.
- **Currency Conversion:** Convert amounts between various currencies and get additional information like historical data and exchange rates.
- **Periodic Messages:** Prevent Heroku dynos from going to sleep by sending periodic messages.
- **User-Friendly Commands:** easy-to-use commands for conversion and time retrieval.



## Command List
**not case sensitive**
| Command                                                              | Description                                                                 | Example                                      |
|----------------------------------------------------------------------|-----------------------------------------------------------------------------|----------------------------------------------|
| `time <location>`                                                     | Returns the current time for the specified city or country. Case-insensitive. | `time Kuala Lumpur`, `time MY`, `time Malaysia` |
| `convt <time> <origin location> to <destination location>`             | Converts time from one location to another. Supports multiple time zones in the same country. | `convt 6pm Malaysia to Australia`, `convt 9am NYC to London` |
| `conv <amount> <from_currency> to <target_currency>`                   | Converts a given amount from one currency to another. | `conv 100 USD to CAD`, `conv 100 EUR to GBP` |
| `convf <amount> <from_currency> to <target_currency>`                  | Converts a given amount from one currency to another and returns additional info (high, low, average, change). | `convf 100 USD to CAD`, `convf 100 EUR to GBP` |
| `cthelp`                                                              | Provides help on time-related commands.                                      | `cthelp`                                    |
| `clist`                                                               | Lists all supported currencies and their codes.                              | `clist`                                     |
| `ctlist`                                                              | Lists all supported cities and countries for time-related commands.         | `ctlist`                                    |


