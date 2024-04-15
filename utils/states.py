from typing import Final
from aiogram.dispatcher.filters.state import StatesGroup, State


class Register(StatesGroup):
    WaitLogin: Final = State()
    SucceedSub: Final = State()


class Request(StatesGroup):
    CreateDialog: Final = State()
    SetNameDialog: Final = State()
    MakeRequest: Final = State()


class ViewDialogs(StatesGroup):
    ShowAll: Final = State()
    ShowSelected: Final = State()


class ADPosting(StatesGroup):
    WriteText: Final = State()
    CheckPost: Final = State()
    SendPost: Final = State()


class AddAdmin(StatesGroup):
    TakeUserId: Final = State()

