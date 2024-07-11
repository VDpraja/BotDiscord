# YouTube Notification Discord Bot

This is a Discord bot that monitors a specified YouTube channel and sends a notification to a Discord channel whenever a new video is uploaded. The bot uses YouTube API v3 to check for new uploads and Discord.py to interact with Discord.

## Features

- Monitor a specified YouTube channel for new uploads.
- Send a notification with an embedded message to a Discord channel when a new video is uploaded.
- Only server owner and bot owner can set or list the monitored YouTube channel.
- Stores YouTube channel settings in SQLite database.

## Requirements

- Python 3.7+
- Discord.py
- YouTube Data API v3
- SQLite

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repository.git
    cd your-repository
    ```
2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up your environment variables. Create a `.env` file in the project root directory and add your Discord bot token, YouTube API key, and your Discord user ID:
    ```env
    DISCORD_TOKEN=your_discord_token_here
    YOUTUBE_API_KEY=your_youtube_api_key_here
    OWNER_ID=your_discord_id_here
    ```
5. Run the bot:
    ```bash
    python bot.py
    ```

## Usage

### Commands

- `/setchannel <channel_id> <notify_channel>`: Set the YouTube channel to monitor and the Discord channel to send notifications. Only the server owner and bot owner can use this command.
- `/listchannel`: Get the current YouTube channel being monitored and the Discord channel for notifications.

### Example

1. Set the YouTube channel to monitor and the Discord channel for notifications:
    ```
    /setchannel <ID_CHANNEL> #general
    ```
2. List the current YouTube channel being monitored:
    ```
    /listchannel
    ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
