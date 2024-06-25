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

cancel_btn = KeyboardButton('Назад 🔙')


async def _cancel_action_msg(msg: Message, state: FSMContext):
    await state.reset_state()
    await user_main_menu(msg, state)


async def _cancel_action_query(query: CallbackQuery, state: FSMContext):
    await state.reset_state()
    # print("чоо")
    await user_main_menu(query, state)



async def __view_other_payed_models(msg: Message, state: FSMContext):
    await state.reset_state()
    await state.set_state(ViewDialogs.ShowAll)

    # dialogs = await select_all_active_user_dialogs(msg.from_user.id)
    # markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup = InlineKeyboardMarkup()
    # for dialog in dialogs:
    #     markup.add(InlineKeyboardButton(f'{dialog.name}', callback_data=f'openDialog_{dialog.dialog_id}'))

    markup.add(InlineKeyboardButton('GigaChat', callback_data="selectOtherModel_GigaChat"))
    markup.add(InlineKeyboardButton('ChatGPT', callback_data="selectOtherModel_ChatGPT"))
    markup.add(InlineKeyboardButton('Назад', callback_data="cancel_act"))
    await bot.send_message(chat_id=msg.from_user.id,
                           text=f'Выберите модель, которая будет исползоваться при запросах',
                           reply_markup=markup)


async def __select_other_model(query: CallbackQuery, state: FSMContext):
    # print('bebra')
    # await state.set_state(ViewDialogs.ShowSelected)
    model = query.data.split('_')[1]

    # requests = await select_requests_of_user_dialog(dialog_id)
    # markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    msg_text = f'Выбрана новая модель для запросов: {model}'
    # markup = InlineKeyboardMarkup()
    # for dialog in dialogs:
    #     markup.add(InlineKeyboardButton(f'{dialog.name}', callback_data=f'open_dialog_{dialog.dialog_id}'))
    # msg_text += (f'Вопрос: {requests[-1].prompt}\n'
    #              f'Ответ: {requests[-1].answer}')

    # markup = (ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    #           .add(cancel_btn))
    await bot.send_message(chat_id=query.from_user.id,
                           text=f'{msg_text}')
    await user_main_menu(query, state)

def register_settings_handlers(dp: Dispatcher) -> None:
    # region EVENT

    dp.register_message_handler(_cancel_action_msg,
                                Text(equals=cancel_btn.text), state='*')
    dp.register_callback_query_handler(_cancel_action_query, lambda c: c.data == "cancel_act", state='*')

    #############################
    ## create dialog
    dp.register_message_handler(__view_other_payed_models,
                                Text(equals=kb.btn_profile), state='*')

    dp.register_callback_query_handler(__select_other_model,
                                       lambda c: c.data and c.data.startswith('selectOtherModel_'),
                                       state='*')
