from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentType, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, \
    ReplyKeyboardMarkup, CallbackQuery

from database.quick_commands import add_dialog, add_request_to_dialog, select_all_active_user_dialogs, \
    select_requests_of_user_dialog, add_answer_to_request
from handlers import keyboards as kb
from handlers.user.register import user_main_menu
from loader import bot
from utils.api_sber import send_requests
from utils.states import Request, ViewDialogs

#############################
#############################
cancel_btn = KeyboardButton('Назад 🔙')


async def _cancel_action_msg(msg: Message, state: FSMContext):
    await state.reset_state()
    await user_main_menu(msg, state)


async def _cancel_action_query(query: CallbackQuery, state: FSMContext):
    await state.reset_state()
    # print("чоо")
    await user_main_menu(query, state)
#############################
#############################


async def __create_new_dialog_waitName(msg: Message, state: FSMContext):
    await state.reset_state()
    await state.set_state(Request.CreateDialog)
    markup = (ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
              .add(cancel_btn))
    await bot.send_message(chat_id=msg.from_user.id,
                           text=f'Введите ваш запрос',
                           reply_markup=markup)


async def __dialog_created_setName(msg: Message, state: FSMContext):
    await state.set_state(Request.MakeRequest)
    '''
    Создание диалога в БД, возвращая его ID
    '''
    dialog_id = await add_dialog(msg.text, msg.from_user.id)
    await state.update_data(dialog_id=dialog_id)

    # await state.update_data(dialog_id=msg.text)
    markup = (ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
              .add(cancel_btn))

    await bot.send_message(chat_id=msg.from_user.id,
                           text=f'Создан диалог с названием "{msg.text}"\n\n',
                           reply_markup=markup)
    await __create_new_request(msg, state)


async def __create_new_request(msg: Message, state: FSMContext):
    # await state.set_state(Request.MakeRequest)
    # print(msg.text)
    # if msg.text == cancel_btn:
    #     await user_main_menu(msg, state)
    #     print(msg.text)
    #     return

    data = await state.get_data()
    # print()
    # print(data['dialog_id'])
    '''
    TO DO: Создание запроса в БД, возвращая его ID
    data = await state.get_data()
    await state.update_data(request_id=request_id)
    request_id = await create_new_request(dialog_id=data['dialog_id'], prompt=msg.text)
    await state.update_data(request_id=request_id)
    '''

    request_id = await add_request_to_dialog(data['dialog_id'], msg.text)
    markup = (ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
              .add(cancel_btn))
    sended_msg = await bot.send_message(chat_id=msg.from_user.id,
                                        text=f'Запрос отправлен, ответ генерируется, подождите пожалуйста...')

    answer_data = await send_requests(msg.text)
    completion_tokens = answer_data['usage']['completion_tokens']
    prompt_tokens = answer_data['usage']['prompt_tokens']
    total_tokens = answer_data['usage']['total_tokens']
    answer = [answer_data['choices'][0]['message']['content']]
    answer_text = "".join(answer)
    await add_answer_to_request(request_id, answer_text, completion_tokens, prompt_tokens, total_tokens)
    '''
        API: отправить запрос к ИИ получив ответ
        answer = api_chatgpt()
        if len(answer) > 200: # доработать
            answer = answer.split('.', maxsplit=1)
    '''
    answer.append(f'\n\nНапишите следующий запрос или нажмите кнопку "{cancel_btn.text}"')
    # for message in answer:
    await bot.edit_message_text(chat_id=msg.from_user.id,
                                text=f'<b>Вопрос:</b> {msg.text}\n\n'
                                     f'<b>Ответ:</b> {"".join(answer)}',
                                message_id=sended_msg.message_id)


#############################
#############################

async def __view_all_user_dialogs(msg: Message, state: FSMContext):
    await state.reset_state()
    await state.set_state(ViewDialogs.ShowAll)

    dialogs = await select_all_active_user_dialogs(msg.from_user.id)
    # markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup = InlineKeyboardMarkup()
    for dialog in dialogs:
        markup.add(InlineKeyboardButton(f'{dialog.name}', callback_data=f'openDialog_{dialog.dialog_id}'))

    markup.add(InlineKeyboardButton('Назад', callback_data="cancel_act"))
    await bot.send_message(chat_id=msg.from_user.id,
                           text=f'Ваши сохраненные запросы',
                           reply_markup=markup)


async def __view_selected_dialog(query: CallbackQuery, state: FSMContext):
    # print('bebra')
    await state.set_state(ViewDialogs.ShowSelected)
    dialog_id = query.data.split('_')[1]

    requests = await select_requests_of_user_dialog(dialog_id)
    # markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    msg_text = 'Последний запрос:\n\n'
    # markup = InlineKeyboardMarkup()
    # for dialog in dialogs:
    #     markup.add(InlineKeyboardButton(f'{dialog.name}', callback_data=f'open_dialog_{dialog.dialog_id}'))
    msg_text += (f'Вопрос: {requests[-1].prompt}\n'
                 f'Ответ: {requests[-1].answer}')

    markup = (ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
              .add(cancel_btn))
    await bot.send_message(chat_id=query.from_user.id,
                           text=f'{msg_text}',
                           reply_markup=markup)

#############################
#############################

def register_request_handlers(dp: Dispatcher) -> None:
    # region EVENT

    dp.register_message_handler(_cancel_action_msg,
                                Text(equals=cancel_btn.text), state='*')
    dp.register_callback_query_handler(_cancel_action_query, lambda c: c.data == "cancel_act", state='*')

    #############################
    ## create dialog
    dp.register_message_handler(__create_new_dialog_waitName,
                                Text(equals=kb.btn_new_request), state='*')

    dp.register_message_handler(__dialog_created_setName,
                                content_types=[ContentType.TEXT], state=Request.CreateDialog)

    dp.register_message_handler(__create_new_request,
                                content_types=[ContentType.TEXT], state=Request.MakeRequest)

    #############################
    ## view dialogs
    dp.register_message_handler(__view_all_user_dialogs,
                                Text(equals=kb.btn_my_requests), state='*')
    dp.register_callback_query_handler(__view_selected_dialog,
                                       lambda c: c.data and c.data.startswith('openDialog_'),
                                       state=ViewDialogs.ShowAll)
