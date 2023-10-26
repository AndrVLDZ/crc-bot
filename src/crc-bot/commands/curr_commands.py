from typing import Callable, Union

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from common.currencies import CURRENCIES
from common.checks import check_user, get_id
from db import get_currency_pair, get_from, get_to, set_currency_pair, set_from, set_to
from menu import main_menu

router = Router()


async def set_curr(
    user_id: str, curr: str, get_func: Callable, set_func: Callable, pair: bool
) -> Union[str, bool]:
    db_curr = await get_func(user_id)

    if curr == db_curr.split()[0]:
        if pair:
            return False
        curr_from, curr_to = await get_currency_pair(user_id)
        return f"**{curr_from}** >> **{curr_to}**"

    if curr in CURRENCIES.keys():
        flag = CURRENCIES[curr]
        await set_func(user_id, f"{curr} {flag}")
        if pair:
            return True
        curr_from, curr_to = await get_currency_pair(user_id)
        return f"**{curr_from}** >> **{curr_to}**"

    return f"No such currency **{curr}**"


@router.message(Command(commands=["from"]))
async def cmd_set_from(message: Message, command: Command) -> None:
    if await check_user(message):
        user_id = await get_id(message)
        if command.args:
            curr_from = str((command.args.split())[0]).upper()
            response_text = await set_curr(
                user_id, curr_from, get_from, set_from, pair=False
            )
            menu = await main_menu(user_id)
            await message.answer(
                text=response_text,
                parse_mode="Markdown",
                reply_markup=menu,
            )
        else:
            menu = await main_menu(user_id)
            await message.answer("Specify currency", reply_markup=menu)


@router.message(Command(commands=["to"]))
async def cmd_set_to(message: Message, command: Command) -> None:
    if await check_user(message):
        user_id = await get_id(message)
        if command.args:
            curr_to = str((command.args.split())[0]).upper()
            response_text = await set_curr(user_id, curr_to, get_to, set_to, pair=False)
            menu = await main_menu(user_id)
            await message.answer(
                text=response_text,
                parse_mode="Markdown",
                reply_markup=menu,
            )
        else:
            menu = await main_menu(user_id)
            await message.answer("Specify currency", reply_markup=menu)


@router.message(Command(commands=["pair"]))
async def cmd_set_pair(message: Message, command: Command) -> None:
    user_id = await get_id(message)
    if await check_user(message):
        if command.args and len((command.args.split())) == 2:
            args = command.args.split()
            curr_from = str(args[0]).upper()
            curr_to = str(args[1]).upper()

            res_to = await set_curr(user_id, curr_to, get_to, set_to, pair=True)
            res_from = await set_curr(user_id, curr_from, get_from, set_from, pair=True)
            menu = await main_menu(user_id)

            if type(res_to) == str:
                await message.answer(
                    text=res_to, parse_mode="Markdown", reply_markup=menu
                )

            if type(res_from) == str:
                await message.answer(
                    text=res_from, parse_mode="Markdown", reply_markup=menu
                )

            if (
                (not res_to and not res_from)
                or (res_to and not res_from)
                or (res_to and res_from)
            ):
                curr_from, curr_to = await get_currency_pair(user_id)
                await message.answer(
                    text=f"**{curr_from}** >> **{curr_to}**",
                    parse_mode="Markdown",
                    reply_markup=menu,
                )

        else:
            menu = await main_menu(user_id)
            await message.answer("Specify currency pair", reply_markup=menu)


@router.message(Command(commands=["swap"]))
async def cmd_swap(message: Message) -> None:
    if await check_user(message):
        user_id = await get_id(message)
        curr_from, curr_to = await get_currency_pair(user_id)
        await set_currency_pair(user_id, curr_to, curr_from)
        menu = await main_menu(user_id)
        await message.answer(
            text=f"**{curr_to}** >> **{curr_from}**",
            parse_mode="Markdown",
            reply_markup=menu,
        )
