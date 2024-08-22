import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher


from models.schemas import Event, Invitation

load_dotenv()
bot = Bot(token=os.getenv("TOKEN_TG"))
dp = Dispatcher()


async def send_message_tg(tg_id, inviter: str, event: Event, invitation: Invitation):
    message = (f"<b>{invitation.name}</b>\n"
               f"{inviter} invited you to an event - {event.name}")
    link = f"https://{os.getenv('HOST')}/events/{event.id}"
    full_message = (f"{message}\n\n"
                    f"You can read more about the event here <a href='{link}'>link</a>")

    await bot.send_message(tg_id, full_message, parse_mode='HTML')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
