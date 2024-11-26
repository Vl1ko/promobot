
from main import dp
from aiogram import types
from aiogram import types, F

from aiogram.filters import Command
from aiogram.types import  WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.methods.send_message import SendMessage

from database.db import Database

import sys
import pathlib
import requests
import json
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

ADMIN = int((os.getenv('ADMIN')))



script_dir = pathlib.Path(sys.argv[0]).parent
db_file = script_dir / 'database/db.sqlite3'

db = Database(db_file=db_file)


@dp.message(Command('add_promo'))
async def add_promo(message: types.Message):
  if message.from_user.id == ADMIN:
    amount = message.text.split(' ')[1].split('\n')[0]
    promo = message.text.split('\n')[1:]

    db.add_product(amount=amount, number=promo)
    await message.answer(f"Промокод на сумму {amount} звезд с номером {promo} добавлен успешно")

@dp.message(Command('del_promo'))
async def add_promo(message: types.Message):
  if message.from_user.id == ADMIN:
    promo = message.text.split(' ')[1]
    db.del_product(number=promo)
    await message.answer(f"Промокод с номером {promo} успешно удален")

@dp.message(Command('hide_7'))
async def hide(message: types.Message):
  if message.from_user.id == ADMIN:
    await message.answer("Промокоды на 7 дней скрыты")
    db.hide_gifts(7)

@dp.message(Command('hide_14'))
async def hide(message: types.Message):
  if message.from_user.id == ADMIN:
    await message.answer("Промокоды на 14 дней скрыты")
    db.hide_gifts(14)

@dp.message(Command('hide_30'))
async def hide(message: types.Message):
  if message.from_user.id == ADMIN:
    await message.answer("Промокоды на 30 дней скрыты")
    db.hide_gifts(30)

@dp.message(Command('hide_60'))
async def hide(message: types.Message):
  if message.from_user.id == ADMIN:
    await message.answer("Промокоды на 60 дней скрыты")
    db.hide_gifts(60)

@dp.message(Command('show_7'))
async def show(message: types.Message):
  if message.from_user.id == ADMIN:
    await message.answer("Промокоды на 7 дней отображены")
    db.show_gifts(7)

@dp.message(Command('show_14'))
async def show(message: types.Message):
  if message.from_user.id == ADMIN:
    await message.answer("Промокоды на 14 дней отображены")
    db.show_gifts(14)

@dp.message(Command('show_30'))
async def show(message: types.Message):
  if message.from_user.id == ADMIN:
    await message.answer("Промокоды на 30 дней отображены")
    db.show_gifts(30)

@dp.message(Command('show_60'))
async def show(message: types.Message):
  if message.from_user.id == ADMIN:
    await message.answer("Промокоды на 60 дней отображены")
    db.show_gifts(60)