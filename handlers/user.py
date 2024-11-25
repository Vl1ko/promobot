
from database import db
from main import dp, bot
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

ADMIN = int(os.getenv('ADMIN'))

script_dir = pathlib.Path(sys.argv[0]).parent
db_file = script_dir / 'database/db.sqlite3'

db = Database(db_file=db_file)

@dp.message(F.text)
async def admin_menu(message: types.Message):
  builder = InlineKeyboardBuilder()

  builder.row(types.InlineKeyboardButton(
      text="Купить промокод 7 дней (220р)",
      callback_data="buy_7"
  ), types.InlineKeyboardButton(
      text="Купить промокод 14 дней (380р)",
      callback_data="buy_14"
  ), types.InlineKeyboardButton(
      text="Купить промокод 30 дней (760р)",
      callback_data="buy_30"
  ), types.InlineKeyboardButton(
      text="Купить промокод 60 дней (1300р)",
      callback_data="buy_60"
  ), width=1)
  await message.answer("Выберите промокод, который желаете купить", reply_markup=builder.as_markup())
  
@dp.callback_query(F.data == "buy_7")
async def buy_7(callback_query: types.CallbackQuery):
  await callback_query.message.reply_invoice(
      title="Промокод на 7 дней",
      description="Промокод на 7 дней (220р)",
      currency="XTR",
      payload="test_payload",
      prices=[
          types.LabeledPrice(label="Промокод на 7 дней", amount=100)
      ]
  )


@dp.callback_query(F.data == "buy_14")
async def buy_14(callback_query: types.CallbackQuery):
  await callback_query.message.reply_invoice(
      title="Промокод на 14 дней",
      description="Промокод на 14 дней (380р)",
      currency="XTR",
      payload="test_payload",
      prices=[
          types.LabeledPrice(label="Промокод на 14 дней", amount=200)
      ]
  )

@dp.callback_query(F.data == "buy_30")
async def buy_30(callback_query: types.CallbackQuery):
  await callback_query.message.reply_invoice(
      title="Промокод на 30 дней",
      description="Промокод на 30 дней (760р)",
      currency="XTR",
      payload="test_payload",
      prices=[
          types.LabeledPrice(label="Промокод на 30 дней", amount=400)
      ]
  )

@dp.callback_query(F.data == "buy_60")
async def buy_60(callback_query: types.CallbackQuery):
  await callback_query.message.reply_invoice(
      title="Промокод на 60 дней",
      description="Промокод на 60 дней (1300р)",
      currency="XTR",
      payload="test_payload",
      prices=[
          types.LabeledPrice(label="Промокод на 60 дней", amount=700)
      ] 
  )

@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
  if db.check_promo():
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
  
  else: 
    await pre_checkout_query.answer(
        ok=False,
        error_message="Товара нет в наличии, попробуйте позже"
    )

    await bot.send_message(chat_id=ADMIN, text=f"Промокды стоимостью {pre_checkout_query.total_amount} звезд закончились!")

@dp.message(F.successful_payment)
async def successful_payment(message: types.Message):
  await message.answer("Платеж прошел успешно")
  await message.answer(f"Ваш промокод - {str(db.new_buy(amount=message.successful_payment.total_amount))}")
  if db.check_remain(amount=message.successful_payment.total_amount) <= 5:
    await bot.send_message(chat_id=ADMIN, text=f"Осталось {db.check_remain(amount=message.successful_payment.total_amount)} промокода(ов) стоимостью {message.successful_payment.total_amount} звезд!")