import asyncio

from config import Env
from database.main import db
import quick_commands as commands
from database.schemas.request import Requests
from database.schemas.solution import Solution


async def db_test():
    await db.set_bind(Env.POSTGRES_URI)
    # await db.gino.drop_all()
    await db.gino.create_all()

    await Requests.create(prompt='test request 2')
    await Solution.create(name='ChatGPT')
    # await commands.add_user('111111', 'test')
    # await commands.add_user('351931465', 'skidikis')
    # await commands.add_user('222222222', 'test2')
    # await commands.add_user('33333333', 'test4')
    # await commands.add_company('1711620726794x118791242414806770', 'Oko')
    #
    # users = await commands.select_all_users()
    # print(users)
    #
    # count = await commands.count_users()
    # print(count)
    #
    # user = await commands.select_user_by_telegram_id(111111)
    # print(user.telegram_username)
    #
    # await commands.update_user_name_bot(111111, 'tester')
    #
    # user = await commands.select_user_by_telegram_id(111111)
    # print(user.telegram_username)

loop = asyncio.get_event_loop()
loop.run_until_complete(db_test())
