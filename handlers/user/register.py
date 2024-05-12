from datetime import datetime

import loguru
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.utils.deep_linking import get_start_link
from loguru import logger

# from database.main import connectToDB
# from database.methods.db_user import update_user_data
from database import quick_commands as commands
from database.quick_commands import select_company, select_user_by_telegram_id, add_tester_user
from database.schemas.user import User
from handlers.keyboards import *
from handlers.keyboards import kb_main_menu
from loader import bot
from utils.states import Register, Request


async def __start(message: Message, state: FSMContext):
    # print('произошел старт')
    args = message.get_args()
    # print(args)
    user_id = message.from_user.id
    user = await select_user_by_telegram_id(user_id)
    # print(user)
    # print(user)
    if args == 'tester' and user is None:
        await add_tester_user(user_id, telegram_username=message.from_user.username)
        msg_txt = ("Добро пожаловать в бота сервиса AI Control!\n"
                   "Это у вас тестовый аккаунт с ограниченным функционалом")
        await bot.send_message(chat_id=user_id, text=msg_txt, reply_markup=await kb_main_menu(user_id))
        return

    if user is not None:
        await state.reset_state()
        msg_txt = "Отправил вам клавиатуру. Используйте кнопки, чтобы пользоваться ботом"
        await bot.send_message(chat_id=user_id, text=msg_txt, reply_markup=await kb_main_menu(user_id))
        return

    # args = args.split('-')
    # if len(args) == 2:
    user_website_id = args
    # user_website_id, company_id = args
    # print(user_website_id, company_id)
    await state.reset_state()

    try:
        # user_website_id = await commands.check_args(user_website_id)
        user: User = await commands.select_user_by_website_id(user_website_id)
        # print(user)
        company = await commands.select_company(user.company_id)
        # print(company)
        if user is not None and not user.have_bot:
            await commands.update_user_connect_bot(user_id, user.website_id, message.from_user.username)
            msg_txt = ("Добро пожаловать в бота сервиса AI Control!\n"
                       "Ваш аккаунт связан с учетной записью на сайте успешно.\n"
                       f"Ваша организация: {company.company_name}")
            await bot.send_message(chat_id=user_id, text=msg_txt, reply_markup=await kb_main_menu(user_id))

        elif user is not None and user.have_bot:
            msg_txt = "Отправил вам клавиатуру. Используйте кнопки, чтобы пользоваться ботом"
            await bot.send_message(chat_id=user_id, text=msg_txt, reply_markup=await kb_main_menu(user_id))

        else:
            msg_txt = ("Приветствую вас! Это бот для использования сервиса AI Control.\n"
                       "Чтобы получить к нему доступ, пожалуйста зарегистрируйтесь на сайте:\n"
                       "https://ai-control-service.bubbleapps.io/version-test/\n"
                       "Сгенерируйте ссылку для доступа через сайт")
            await bot.send_message(chat_id=user_id, text=msg_txt)

    except Exception as er:
        logger.error(f"{er}")
        msg_txt = ("Приветствую вас! Это бот для использования сервиса AI Control.\n"
                   "Чтобы получить к нему доступ, пожалуйста зарегистрируйтесь на сайте\n"
                   "https://ai-control-service.bubbleapps.io/version-test/")
        await bot.send_message(chat_id=user_id, text=msg_txt)
    # else:
    #     msg_txt = ("Приветствую вас! Это бот для использования сервиса AI Control.\n"
    #                "Чтобы получить к нему доступ, пожалуйста зарегистрируйтесь на сайте и получите ссылку доступа\n"
    #                "https://ai-control-service.bubbleapps.io/version-test/")
    #     await bot.send_message(chat_id=user_id, text=msg_txt)


cancel_btn = KeyboardButton('Назад 🔙')


async def user_main_menu(call: Message or CallbackQuery, state: FSMContext):
    await state.reset_state()
    user_tg_id = call.from_user.id
    user = await select_user_by_telegram_id(user_tg_id)
    await bot.send_message(chat_id=user_tg_id,
                           text=f'Главное меню\n\n'
                                f'Пользователь: {user.first_name}\n'
                                f'Почта: {user.email}\n',
                           reply_markup=await kb_main_menu(user.telegram_id))


async def __ref(message: Message, state: FSMContext):
    ref_link = await get_start_link(payload='tester')
    await message.answer(f'Привет {message.from_user.first_name}\n'
                         f'Твоя ссылка: {ref_link}')


def _register_register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__start, commands=["start"], state='*')

    dp.register_message_handler(__ref, commands=["ref"], state='*')

    dp.register_message_handler(user_main_menu,
                                Text(equals=cancel_btn), state=Request.MakeRequest)
    # dp.register_message_handler(__getName, content_types=[ContentType.TEXT], state=Register.WaitLogin)
    # dp.register_callback_query_handler(attention_to_sub, lambda c: c.data == 'check_sub_status', state='*')
