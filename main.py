import os
import logging
import pyrogram
from dotenv import load_dotenv
from pyrogram import idle
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.errors import MediaCaptionTooLong
from pyrogram.types import InputMediaPhoto
from db import DatabaseManager
import time
from agent import agent

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_SESSION = os.getenv("BOT_SESSION")

bot = pyrogram.client.Client(name="PersonalTrainerBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN, in_memory=True, session_string=BOT_SESSION)


def call_agent(text: str, attemps: int = 3, session_id: str = None) -> tuple:
    for _ in range(0, attemps):
        agent_response = agent.run(text, session_id=session_id)
        try:
            return agent_response, agent_response.content.message
        except AttributeError:
            print(f"ERROR content non valido: {agent_response.content}")
    raise AttributeError(f"L'agente ha restituito un agent_response.content non valido per {attemps} volte di seguito.")


def send_images(user_id: int | str, image_paths: list) -> None:
    """
    Support function for sending more images. With Telegram API you can send up to 10 pics per request.
    In case the agent "want" to send more than 10 we must split it in more requests, with a little timeout
    for avoiding flood wait from Telegram.
    """

    # Number of requests needed for sending all pictures
    requests_needed: int = len(image_paths) // 10 + (1 if len(image_paths) % 10 else 0)
    for i in range(0, requests_needed):
        media_group_paths = image_paths[i:i + 10]

        if len(media_group_paths) == 1:
            bot.send_photo(chat_id=user_id, photo=media_group_paths[0])
        else:
            media = [
                InputMediaPhoto(media=m) for m in media_group_paths
            ]
            bot.send_media_group(chat_id=user_id, media=media)

            # Timeout for avoiding flood wait from Telegram API
            time.sleep(.2)


@bot.on_message()
def on_request(_, message):
    user_id = message.chat.id

    # Send "typing..." action to user while agent "thinks"
    bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)

    # Call agent passing session id if user already used the agent
    if db.user_session_exists(user_id=user_id):
        session_id = db.get_user_session(user_id=user_id)
        agent_response, agent_text = call_agent(text=message.text, session_id=session_id)

    # Save session id if it is a new user
    else:
        agent_response, agent_text = call_agent(text=message.text)
        session_id = agent_response.session_id
        db.add_user_session(user_id=user_id, session_id=session_id)

    if images := agent_response.content.images:
        # If there is only one picture, use send_photo passing its path
        if len(images) == 1:
            bot.send_photo(chat_id=user_id, caption=agent_text, photo=images[0])

        else:
            send_images(user_id=user_id, image_paths=images)

            # Timeout for avoiding flood wait from Telegram API
            time.sleep(.2)

            # Send text in a separate message
            bot.send_message(chat_id=user_id, text=agent_text)

    # If there aren't images, send only text
    else:
        bot.send_message(chat_id=user_id, text=agent_text)


if __name__ == "__main__":
    db = DatabaseManager("storage/users.db")
    bot.start()
    idle()
