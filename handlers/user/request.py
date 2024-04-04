from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentType, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, \
    ReplyKeyboardMarkup

from handlers import keyboards as kb
from loader import bot
from utils.states import Request

#############################
#############################
cancel_btn = KeyboardButton('Отмена')


async def __create_new_request_setName(msg: Message, state: FSMContext):
    await state.reset_state()
    await state.set_state(Request.CreateRequest)
    markup = (ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
              .add(cancel_btn))
    await bot.send_message(chat_id=msg.from_user.id,
                           text=f'Введите название запроса',
                           reply_markup=markup)


async def __request_created_waitQuestion(msg: Message, state: FSMContext):
    await state.set_state(Request.Dialog)

    # Создание диалога в БД



#############################
#############################


def register_request_handlers(dp: Dispatcher) -> None:
    # region EVENT

    ## create event
    dp.register_message_handler(__create_new_request_setName,
                                Text(equals=kb.btn_new_request), state='*')

    dp.register_message_handler(__request_created_waitQuestion,
                                content_types=[ContentType.TEXT], state=Request.CreateRequest)
