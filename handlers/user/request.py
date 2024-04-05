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
cancel_btn = KeyboardButton('Назад')


async def __create_new_dialog_waitName(msg: Message, state: FSMContext):
    await state.reset_state()
    await state.set_state(Request.CreateDialog)
    markup = (ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
              .add(cancel_btn))
    await bot.send_message(chat_id=msg.from_user.id,
                           text=f'Введите название запроса',
                           reply_markup=markup)


async def __dialog_created_setName(msg: Message, state: FSMContext):
    await state.set_state(Request.MakeRequest)
    '''
    TO DO: Создание диалога в БД, возвращая его ID
    dialog_id = await create_new_dialog(dialog.name = msg.text)
    await state.update_data(dialog_id=dialog_id)
    '''
    await state.update_data(dialog_id=msg.text)
    markup = (ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
              .add(cancel_btn))
    await bot.send_message(chat_id=msg.from_user.id,
                           text=f'Создан диалог {msg.text}\n\n'
                                f'Введите ваш запрос',
                           reply_markup=markup)


async def __create_new_request(msg: Message, state: FSMContext):
    await state.set_state(Request.MakeRequest)
    data = await state.get_data()
    print()
    print(data['dialog_id'])
    '''
    TO DO: Создание запроса в БД, возвращая его ID
    data = await state.get_data()
    await state.update_data(request_id=request_id)
    request_id = await create_new_request(dialog_id=data['dialog_id'], prompt=msg.text)
    await state.update_data(request_id=request_id)
    '''
    markup = (ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
              .add(cancel_btn))
    sended_msg = await bot.send_message(chat_id=msg.from_user.id,
                                        text=f'Запрос отправлен, ответ генерируется, подождите пожалуйста...')
    '''
    API: отправить запрос к ИИ получив ответ
    answer = api_chatgpt()
    if len(answer) > 200: # доработать
        answer = answer.split('.', maxsplit=1)
    '''

    answer = ['Сгенерированный ответ.', 'Продолжение ответа.']
    answer.append(f'\n\nНапишите следующий запрос или нажмите кнопку "{cancel_btn.text}"')
    for message in answer:
        await bot.edit_message_text(chat_id=msg.from_user.id,
                                    text=f'Ответ:\n'
                                         f'{message}',
                                    message_id=sended_msg.message_id)
    await bot.edit_message_reply_markup(chat_id=msg.from_user.id,
                                        message_id=sended_msg.message_id,
                                        reply_markup=markup)


#############################
#############################


def register_request_handlers(dp: Dispatcher) -> None:
    # region EVENT

    ## create event
    dp.register_message_handler(__create_new_dialog_waitName,
                                Text(equals=kb.btn_new_request), state='*')

    dp.register_message_handler(__dialog_created_setName,
                                content_types=[ContentType.TEXT], state=Request.CreateDialog)

    dp.register_message_handler(__create_new_request,
                                content_types=[ContentType.TEXT], state=Request.MakeRequest)
