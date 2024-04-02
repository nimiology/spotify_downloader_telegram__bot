from telegram import BOT_TOKEN, song_callback_query, new_message, CLIENT


if __name__ == '__main__':
    print('[BOT] Starting...')
    CLIENT.start(bot_token=BOT_TOKEN)
    CLIENT.run_until_disconnected()
