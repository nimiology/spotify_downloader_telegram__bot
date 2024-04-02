from telethon import events, Button
from telethon.tl import types

from consts import NOT_FOUND_STICKER
from spotify.utils import search_single


async def handle_search_message(event: events.NewMessage.Event):
    msg = event.message.message
    song_items = search_single(msg)

    # Create inline keyboard buttons
    # Create buttons for each song item
    buttons = []
    for song_item in song_items:
        # Create a new row for each button
        button = [Button.inline(f'{song_item.track_name} - {song_item.artist}', data=f"song:{song_item.id}")]
        buttons.append(button)

    # Create the reply message with buttons
    reply_message = "No results found."
    if buttons:
        reply_message = "🔎Here are the search results:"

        # Send the message with buttons as a reply to the original message
        await event.reply(reply_message, buttons=buttons)
    else:
        await event.respond('❌')
        await event.reply(reply_message, )
