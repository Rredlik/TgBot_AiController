from asyncpg import UniqueViolationError

from database.main import db
from database.schemas.company import Company
from database.schemas.user import User


async def add_user(telegram_id: str, telegram_username):
    try:
        user = User(telegram_id=telegram_id, telegram_username=telegram_username)
        await user.create()
    except UniqueViolationError:
        print("Пользователь не добавлен")


async def add_company(company_id: str, company_name):
    try:
        company = Company(company_id=str(company_id), company_name=company_name)
        await company.create()
    except UniqueViolationError:
        print("Компания не добавлена")


async def select_all_users():
    users = await User.query.gino.all()
    return users


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
    print(f'update_user_connect_bot: {user}')
    await user.update(telegram_id=str(telegram_id), telegram_username=new_username, have_bot=True).apply()


async def select_company(company_id: str):
    company = await Company.query.where(Company.company_id == str(company_id)).gino.first()
    return company


## registration
async def check_args(company_id):
    if company_id == '':
        company = '0'
    elif not company_id.isnumeric():
        company = await select_company(company_id)
        if company is None:
            company = '0'
        else:
            company = company
    else:
        company = '0'
    return company
