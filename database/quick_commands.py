from asyncpg import UniqueViolationError
from loguru import logger

from database.main import db
from database.schemas.company import Company
from database.schemas.request import Dialogs, Requests
from database.schemas.user import User


async def add_user(telegram_id: str, telegram_username):
    try:
        user = User(telegram_id=str(telegram_id), telegram_username=telegram_username)
        await user.create()
    except UniqueViolationError as er:
        logger.error(f"Пользователь не добавлен: {er}")


async def add_tester_user(telegram_id: str, telegram_username=''):
    try:
        user = User(website_id=f'{telegram_id}', first_name='Тестер', last_name='Тестовый', telegram_id=str(telegram_id),
                    telegram_username=telegram_username)
        await user.create()
    except UniqueViolationError as er:
        logger.error(f"Пользователь не добавлен: {er}")


async def add_company(company_id: str, company_name):
    try:
        company = Company(company_id=str(company_id), company_name=company_name)
        await company.create()
    except UniqueViolationError as er:
        logger.error(f"Компания не добавлена: {er}")


async def add_dialog(dialog_name: str, telegram_id):
    try:
        user = await select_user_by_telegram_id(telegram_id)
        dialog = Dialogs(name=dialog_name, user_id=user.user_id)
        data = await dialog.create()
        return data.dialog_id
    except UniqueViolationError as er:
        logger.error(f"Диалог не создан: {er}")


async def add_request_to_dialog(dialog_id: str, prompt):
    try:
        request = Requests(dialog_id=dialog_id, prompt=prompt)
        '''
        TODO: Добавлять контекст в диалог Dialog.context += prompt
        '''
        data = await request.create()
        return data.request_id
    except UniqueViolationError as er:
        logger.error(f"Запрос не создан: {er}")


async def add_answer_to_request(request_id: str, answer, usage_completion_tokens, usage_prompt_tokens,
                                usage_total_tokens):
    request = await Requests.query.where(Requests.request_id == request_id).gino.first()
    await request.update(answer=answer, usage_completion_tokens=usage_completion_tokens,
                         usage_prompt_tokens=usage_prompt_tokens, usage_total_tokens=usage_total_tokens).apply()


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_all_active_user_dialogs(telegram_id):
    user = await select_user_by_telegram_id(telegram_id)
    dialogs = await Dialogs.query.where(Dialogs.user_id == user.user_id and Dialogs.is_deleted is False).gino.all()
    return dialogs


async def select_requests_of_user_dialog(dialog_id):
    dialogs = await Requests.query.where(Requests.dialog_id == int(dialog_id)).gino.all()
    return dialogs


async def count_users():
    # count = await User.query.gino.count()
    count = await db.func.count(User.user_id).gino.scalar()
    return count


async def select_user_by_telegram_id(telegram_id):
    user = await User.query.where(User.telegram_id == str(telegram_id)).gino.first()
    return user


async def select_user_by_website_id(website_id: str):
    user = await User.query.where(User.website_id == str(website_id)).gino.first()
    return user


async def update_user_name_bot(telegram_id: str, new_username):
    user = await select_user_by_telegram_id(str(telegram_id))
    await user.update(telegram_username=new_username).apply()


async def update_user_connect_bot(telegram_id: str, website_id: str, new_username):
    user = await select_user_by_website_id(str(website_id))
    # print(f'update_user_connect_bot: {user}')
    logger.info(f"{user}")
    await user.update(telegram_id=str(telegram_id), telegram_username=new_username, have_bot=True).apply()


async def select_company(company_id: str):
    company = await Company.query.where(Company.company_id == company_id).gino.first()
    return company


## registration
async def check_args(user_website_id):
    if user_website_id == '':
        company = '0'
    elif not user_website_id.isnumeric():
        # company = await select_company(user_website_id)
        # if company is None:
        #     company = '0'
        # else:
        #     company = company
        print(True)
    else:
        company = '0'
    return company
