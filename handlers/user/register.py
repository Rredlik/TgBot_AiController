from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentType
from aiogram.utils.deep_linking import get_start_link
from loguru import logger

# from database.main import connectToDB
# from database.methods.db_user import update_user_data
from database import quick_commands as commands
from database.quick_commands import select_company, select_user_by_telegram_id
from handlers.keyboards import *
from handlers.keyboards import kb_main_menu
from loader import bot
from utils.states import Register, Request


async def __start(message: Message, state: FSMContext):
    print('произошел старт')
    args = message.get_args()
    print(args)
    user_id = message.from_user.id
    if args == '':
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
        user = await commands.select_user_by_website_id(user_website_id)
        # print(user)
        company = await commands.check_args(user.company_id)
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


        # if company == '0':
        #     msg_txt = ("Приветствую вас! Это бот для использования сервиса AI Control.\n"
        #                "Чтобы получить к нему доступ, пожалуйста зарегистрируйтесь на сайте:\n"
        #                "https://ai-control-service.bubbleapps.io/version-test/\n"
        #                "Сгенерируйте ссылку для доступа через сайт")
        #     await bot.send_message(chat_id=user_id, text=msg_txt, reply_markup=await kb_main_menu(user_id))
        #
        # elif user.company == company.company_id and not user.have_bot:
        #     await commands.update_user_connect_bot(user.website_id, message.from_user.username)
        #     msg_txt = ("Добро пожаловать в бота сервиса AI Control!\n"
        #                "Ваш аккаунт связан с учетной записью на сайте успешно.\n"
        #                f"Ваша организация: {company.company_name}")
        #     await bot.send_message(chat_id=user_id, text=msg_txt, reply_markup=await kb_main_menu(user_id))
        #
        # elif user.company != company.company_id and user.have_bot:
        #     msg_txt = ("Вы уже привязаны к другой организации, уверены что хотите ее сменить?\n"
        #                f"Ваша организация: {(await select_company(user.company)).company_name}\n"
        #                f"Новая организация: {company.company_name}")
        #     await bot.send_message(chat_id=user_id, text=msg_txt, reply_markup=await kb_main_menu(user_id))
        #
        # else:
        #     msg_txt = "Отправил вам клавиатуру. Используйте кнопки, чтобы пользоваться ботом"
        #     await bot.send_message(chat_id=user_id, text=msg_txt, reply_markup=await kb_main_menu(user_id))

    except Exception as e:
        # await commands.add_user(user_id, message.from_user.username)
        print(e)
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
async def user_main_menu(msg: Message, state: FSMContext):
    await state.reset_state()
    user = await select_user_by_telegram_id(msg.from_user.id)
    await bot.send_message(chat_id=msg.from_user.id,
                           text=f'Главное меню\n\n'
                                f'Пользователь: {user.first_name}\n'
                                f'Почта: {user.email}\n',
                           reply_markup=await kb_main_menu(user.telegram_id))


async def __ref(message: Message, state: FSMContext):
    ref_link = await get_start_link(payload='351931465-1711620726794x118791242414806770')
    await message.answer(f'Привет {message.from_user.first_name}\n'
                         f'Твоя ссылка: {ref_link}')



# async def __getName(message: Message, state: FSMContext):
#     await state.reset_state()
#     user_id = message.from_user.id
#     user_login = message.text
#     '''
#     TO DO:
#     Добавить проверку правильности ввода логина (без лишних символов и пробелов)
#     '''
#     # await update_user_data(user_id, 'user_login', user_login)
#     msg_txt = ('Спасибо за регистрацию.\n'
#                'Используйте кнопки, чтобы пользоваться ботом')
#     await bot.send_message(chat_id=user_id, text=msg_txt, reply_markup=await kb_main_menu(user_id))


# async def __mainMenu(msg: Message, state: FSMContext) -> None:
#     await state.reset_state()
#     user_id = msg.from_user.id
#     msg_text = 'Используй кнопки, чтобы пользоваться ботом'
#     await bot.send_message(chat_id=user_id,
#                            text=msg_text,
#                            reply_markup=await kb_main_menu(user_id))


###########################################################################################################
###########################################################################################################

# async def is_registered(user_id=None, message: Message = None):
#     if message is not None:
#         user_id = message.from_user.id
#     async with connectToDB() as db:
#         try:
#             command = await db.execute(
#                 """SELECT * FROM 'users' WHERE telegram_id = :user_id""",
#                 {'user_id': user_id}
#             )
#             await db.commit()
#             values = await command.fetchone()
#
#             if values is None:
#                 await create_new_user(user_id, message)
#                 return False
#             else:
#                 return True
#         except Exception as er:
#             logger.error(f"{er}")
#         finally:
#             await db.commit()


# async def create_new_user(user_id=None, message: Message = None):
#     username = 'admin'
#     if message is not None:
#         user_id = str(message.from_user.id)
#         username = message.from_user.username.lower()
#     async with connectToDB() as db:
#         try:
#             await db.execute(
#                 "INSERT INTO 'users' (telegram_id, user_name, reg_date) VALUES (?, ?, ?)",
#                 (user_id, username, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#             )
#             logger.info(f"New user registered: {user_id}")
#             await db.commit()
#         except Exception as er:
#             logger.error(f"{er}")
#         finally:
#             await db.commit()


def _register_register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__start, commands=["start"], state='*')

    dp.register_message_handler(__ref, commands=["ref"], state='*')

    dp.register_message_handler(user_main_menu,
                                Text(equals=cancel_btn), state=Request.MakeRequest)
    # dp.register_message_handler(__getName, content_types=[ContentType.TEXT], state=Register.WaitLogin)
    # dp.register_callback_query_handler(attention_to_sub, lambda c: c.data == 'check_sub_status', state='*')



