from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from config import ADMIN_LINK
from filters.main import IsSubscriber
from handlers.user.request import register_request_handlers
from handlers.user.register import _register_register_handlers
from handlers.user.user_settings import register_settings_handlers
from loader import bot


async def __askTp(msg: Message):
    await bot.send_message(chat_id=msg.from_user.id,
                           text=f'Если у вас возникли вопросы или что-то не работает пишите: {ADMIN_LINK}')


def register_users_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__askTp, Text(equals='👩🏼‍💻 Тех. поддержка'), IsSubscriber(), state='*')

    # dp.chat_join_request_handler(__channel_member)
    # dp.register_errors_handler(function_name, exception=exceptions.)

    _register_register_handlers(dp)
    register_request_handlers(dp)
    register_settings_handlers(dp)
    # register_transaction_handlers(dp)
    # register_calculation_handlers(dp)
    # register_members_handlers(dp)
    # register_dialog_handlers(dp)
