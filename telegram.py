import os
import logging
import pyrogram
from dotenv import load_dotenv
from pyrogram import idle
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.errors import MediaCaptionTooLong
from pyrogram.types import InputMediaPhoto

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

@bot.on_message()
def on_message(_, message):

    bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    session_id = None  # TODO ricerca in sqlite3

    agent_response, agent_text = call_agent(text=message.text, session_id=session_id)

    try:
        agent_text = agent_response.content.message
    except AttributeError:
        print(f"ERROR content non valido: {agent_response.content}")

    else:
        if images := agent_response.content.images:
            if len(images) == 1:
                bot.send_photo(chat_id=message.chat.id, caption=agent_text, photo=images[0])
            else:
                media = [
                    InputMediaPhoto(media=m, caption=agent_text if i == 0 else None) for i, m in enumerate(images)
                ]
                try:
                    bot.send_media_group(chat_id=message.chat.id, media=media)
                except MediaCaptionTooLong:
                    media = [InputMediaPhoto(media=m) for m in images]
                    bot.send_media_group(chat_id=message.chat.id, media=media)
                    bot.send_message(chat_id=message.chat.id, text=agent_text)
        else:
            bot.send_message(chat_id=message.chat.id, text=agent_text)


if __name__ == "__main__":
    bot.start()
    idle()
