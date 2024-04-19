# spotify-downloader 🎵

# Telegram Music Bot

This is a Telegram bot that allows users to download music from Spotify and YouTube. It supports downloading tracks,
albums, playlists, and artist information.
DISCLAIMER : THIS SCRIPTS ARE FOR EDUCATION PURPOSES ONLY AND ARE NOT INTENDED TO PROMOTE ANY ILLEGAL ACTIVITIES. THE
AUTHOR WILL NOT BE HELD RESPONSIBLE FOR ANY MISUSE OF THE INFORMATION PROVIDED

## Features

- Download tracks, albums, playlists, and artist information from Spotify.
- Search for music by song name, album name, or artist name.
- Retrieve top tracks and albums of an artist.
- Download music from YouTube.

## Installation

1. Clone the repository:

```
git clone https://github.com/nimiology/spotify_downloader_telegram__bot.git
cd spotify_downloader_telegram__bot
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Set up your .env file with sample.env:
    - `BOT_TOKEN`: Telegram bot token - You can obtain this by creating a new bot on Telegram using the BotFather bot. BotFather will provide you with a token for your bot.
    - `SPOTIFY_CLIENT_ID`: Spotify client ID - These are obtained by registering your application on the Spotify Developer Dashboard. After registration, you'll receive both the client ID and client secret.
    - `SPOTIFY_CLIENT_SECRET`: Spotify client secret - These are obtained by registering your application on the Spotify Developer Dashboard. After registration, you'll receive both the client ID and client secret.
    - `TELEGRAM_API_ID`: Telegram api ID - You can get these by creating an application on the Telegram API website (https://my.telegram.org). After creating the application, you'll receive the API ID and API hash
    - `TELEGRAM_API_HASH`: Telegram api hash - You can get these by creating an application on the Telegram API website (https://my.telegram.org). After creating the application, you'll receive the API ID and API hash
    - `GENIUS_ACCESS_TOKEN`: Genius API access token - You can obtain this by registering your application on the Genius Developer website (https://genius.com/api-clients). After registering, you'll receive an access token for using the Genius API.
    - `BOT_ID`: Telegram bot username - This is the username of your Telegram bot, which you set when creating the bot on the BotFather. You can use this variable as song caption too.
    - `DB_CHANNEL_ID`: Telegram channel ID - This is the chat ID of the channel you want to use for your database. You can obtain this by adding your bot to the channel and using a tool like https://t.me/JsonDumpBot bot in the Telegram to find out the ID of the channel.

4. Run the bot:

```
 python main.py
 ```

## Usage

1. Start the bot by sending `/start` command.
2. Send a Spotify or song name to download music.
3. Search for music by sending song, album, or artist names.

## Contributing

Contributions are welcome! If you want to contribute to this project, feel free to open an issue or submit a pull
request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.




