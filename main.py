import asyncio
import os
import httplib2
import apiclient.discovery
import emoji
import time
import threading
import json

from datetime import date
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from aiogram import Bot, F, Dispatcher, html
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command, BaseFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

#Ключи доступа и остальное
TOKEN = ('6775216943:AAHDuxzBAhv5vkeKCoRTk2pfg3TgDxxbX0c')
CHANNEL_ID = 6775216943
CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1qqlqA6mYHLHcglrr_4SWWFeyqAJz0Nev732XJBpgnM0'

#Подключение медиа
all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_media')
photo_file = os.path.join(all_media_dir, 'photo.jpg')

#Инициализация бота
bot = Bot(token=TOKEN)

class Register(StatesGroup):
    pers = State()

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

# DateTimeRenderOption ='FORMATTED_STRING'
# Пример чтения файла

#Парсинг выполнения работы из Google Таблицы
async def get_data(pers):
    if pers == 'temir':
        val_temir = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='C4:N4',
            majorDimension='ROWS',
        ).execute()
        return val_temir['values']

    elif pers == 'lentik':
        val_len = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='C5:N5',
            majorDimension='ROWS'
        ).execute()
        return val_len['values']

    elif pers == 'niyaz':
        val_niyaz = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='C6:N6',
            majorDimension='ROWS'
        ).execute()
        return val_niyaz['values']

    elif pers == 'pahan':
        val_pahan = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='C7:N7',
            majorDimension='ROWS'
        ).execute()
        return val_pahan['values']
    else:
        print('Error pers')

#Парсинг даты из Google Таблицы
async def get_date():
    dates = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='C3:N3',
            majorDimension='ROWS'
        ).execute()
    return dates['values']

dp = Dispatcher()

#Клавиатура выбора пользователя
main_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Байкенов Т.С.', callback_data='temir')],
                                                [InlineKeyboardButton(text='Ганиев Л.Р.', callback_data='lentik')],
                                                [InlineKeyboardButton(text='Махьянов Н.', callback_data='niyaz')],
                                                [InlineKeyboardButton(text='Набиуллин Д.', callback_data='pahan')]
])

#Клавиатура меню
menu_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Начать проверку')]],                                                
                                                resize_keyboard=True,
                                                input_field_placeholder='')

#Приветствие
@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    photo_file = FSInputFile(path=os.path.join(all_media_dir, 'photo.jpg'))
    await message.answer_photo(photo=photo_file)
    await message.answer(f"Вечер в хату, <b>{html.quote('Арестант')}</b> ! ", parse_mode=ParseMode.HTML)
    await message.answer('Ну здравствуй. Кем будешь?', reply_markup=main_kb)
    
#Нажатие на Байкенов Т.С.
@dp.callback_query(F.data == 'temir')
async def temir(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer(emoji.emojize('Ха, казахов у нас тут ещё не было!:морда_лошади:',
                                                 language= 'ru'), reply_markup=menu_kb)
    await callback.message.edit_reply_markup(
        reply_markup=None
    )
    pers = 'temir'
    while True:
        check_done = await update(pers)
        if  check_done == True:
            await callback.message.answer(emoji.emojize('Метнулся драить хату:колокольчик:',
                                                     language= 'ru'), reply_markup=menu_kb)
    
#Нажатие на Ганиев Л.Р.
@dp.callback_query(F.data == 'lentik')
async def temir(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer(emoji.emojize('Твоё место у параши, опущенный!:петух:',
                                                 language= 'ru'), reply_markup=menu_kb)
    await callback.message.edit_reply_markup(
        reply_markup=None
    )
    pers = 'lentik'
    while True:
        check_done = await update(pers)
        if  check_done == True:
            await callback.message.answer(emoji.emojize('Метнулся драить хату:колокольчик:',
                                                     language= 'ru'), reply_markup=menu_kb)

#Нажатие на Махьянов Н.
@dp.callback_query(F.data == 'niyaz')
async def temir(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer(emoji.emojize('Клуб на этаж ниже, коЖевник:влюбленная_пара:',
                                                 language= 'ru'), reply_markup=menu_kb)
    await callback.message.edit_reply_markup(
        reply_markup=None
    ) 
    pers = 'niyaz'
    while True:
        check_done = await update(pers)
        if  check_done == True:
            await callback.message.answer(emoji.emojize('Метнулся драить хату:колокольчик:',
                                                     language= 'ru'), reply_markup=menu_kb)

#Нажатие на Набиуллин Д.
@dp.callback_query(F.data == 'pahan')
async def temir(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer(emoji.emojize('Ты первоход что ли?..Ой извини, пахан, не признали, молодого!:воинское_приветствие:',
          language= 'ru'), reply_markup=menu_kb)
    await callback.message.edit_reply_markup(
        reply_markup=None
    )
    pers = 'pahan'
    while True:
        check_done = await update(pers)
        if  check_done == False:
            print(check_done)
            await callback.message.answer(emoji.emojize('Метнулся драить хату:колокольчик:', language= 'ru'))
        else:
            print(check_done)

#Проверка выполнения работы
async def update(pers):
    while True:
        current_date = date.today().strftime('%d-%m')
        dates = await get_date()
        date_1 = dates[0][2]
        date_2 = dates[0][3]
        date_3 = dates[0][4]
        date_4 = dates[0][5]
        date_5 = dates[0][6]
        date_6 = dates[0][7]
        date_7 = dates[0][8]
        date_8 = dates[0][9]
        date_9 = dates[0][10]
        data_done = await get_data(pers)
        time.sleep(2.0)        
        if (current_date.count(date_1[:2], 0, 2) == 1 and current_date.count(date_1[3:], 2) == 1):
            if data_done[0][2] == True:
                done = True
                return done
            else:
                done = False
                return done
        elif (current_date.count(date_2[:2], 0, 2) == 1 and current_date.count(date_2[3:], 2) == 1):
            if data_done[0][3] == True:
                done = True
                return done
            else:
                done = False
                return done 
        elif(current_date.count(date_3[:2], 0, 2) == 1 and current_date.count(date_3[3:], 2) == 1):
            if data_done[0][4] == True:
                done = True
                return done
            else:
                done = False
                return done
        elif(current_date.count(date_4[:2], 0, 2) == 1 and current_date.count(date_4[3:], 2) == 1):
            if data_done[0][5] == True:
                done = True
                return done
            else:
                done = False
                return done
        elif(current_date.count(date_5[:2], 0, 2) == 1 and current_date.count(date_5[3:], 2) == 1):
            if data_done[0][6] == True:
                done = True
                return done
            else:
                done = False
                return done
        elif(current_date.count(date_6[:2], 0, 2) == 1 and current_date.count(date_6[3:], 2) == 1):
            if data_done[0][7] == True:
                done = True
                return done
            else:
                done = False
                return done
        elif(current_date.count(date_7[:2], 0, 2) == 1 and current_date.count(date_7[3:], 2) == 1):
            if data_done[0][8] == True:
                done = True
                return done
            else:
                done = False
                return done
        elif(current_date.count(date_8[:2], 0, 2) == 1 and current_date.count(date_8[3:], 2) == 1):
            if data_done[0][9] == True:
                done = True
                return done
            else:
                done = False
                return done 
        elif(current_date.count(date_9[:2], 0, 2) == 1 and current_date.count(date_9[3:], 2) == 1):
            if data_done[0][10] == True:
                done = True
                return done
            else:
                done = False
                return done
        else:
            
        
        
#Запуск бота
async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')