import logging

import g4f
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
from fuzzywuzzy import fuzz
import sqlite3 as sql
from chat import conversation_history, trim_history, clear_command

logging.basicConfig(level=logging.INFO)

bot = Bot(token="6050360696:AAGc2Y7ShpZmEUyS3lOz48BZIXsLXYDAWQg")

dp = Dispatcher(bot)

con = sql.connect('bd.db')

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    print(f"Start event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Подписаться!", url="https://t.me/song_of_the_abyss")
    keyboard.add(url_button)
    await message.reply(f"Меня звать Кяру. Приятно познакомиться, {message.from_user.first_name}! \nПожалуйста, если ты планируешь изучить меня от и до, то помоги моему создателю, подписавший по кнопочке на канал создателя. Тут много интересного, я обещаю тебе^^", reply_markup=keyboard)

@dp.message_handler(commands=['rand'])
async def cmd_rand(message: types.Message):
    print(f"Rand event\nAuthor message: {message.from_user.full_name}({message.from_user.username})")
    from random import randint
    await message.reply(f"Число сгенерированно! Это число: {randint(0, 100)}")

@dp.message_handler(commands=['info'])
async def cmd_info(message: types.Message):
    print(f"Info event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
    await message.answer(f"{message.from_user.first_name}, информация: \nСоздатель: @DarkusFoxis \nВерсия бота: 0.2.1 alfa")

@dp.message_handler(commands=['create'])
async def cmd_create(message: types.Message):
    cur = con.cursor()
    if cur.execute(f"SELECT userid FROM users WHERE userid = {message.from_user.id}").fetchone() is not None:
        print(f"Create guard event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
        await message.reply("Вы уже зарегистрированны!")
    else:
        print(f"Warning! Create event \nAuthor message: {message.from_user.full_name}")
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text ="Да", callback_data="yes"))
        keyboard.add(types.InlineKeyboardButton(text ="Нет", callback_data="no"))
        await message.answer("После подтверждения создания вашего профиля, он не будет подлежать удалению, вы уверенны?", reply_markup=keyboard)

@dp.callback_query_handler(text="yes")
async def create_bd(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    await call.message.answer("Ваш профиль создан! Добро пожаловать в бездну.")
    print(f"Warning! Create profile \nAuthor message: {call.from_user.full_name}({call.from_user.username})")
    await call.answer()
    with con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
        userid INT PRIMARY KEY,
        name TEXT,
        money INT,
        smol INT,
        strike INT);
        """)
        con.commit()

        cur.execute(f"""INSERT INTO users (userid, name, money, smol, strike)
        VALUES('{call.from_user.id}', '{call.from_user.first_name}', '10', '0', '0')""")

@dp.callback_query_handler(text="no")
async def create_bd(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    await call.message.answer("Создание профиля отменено.")
    await call.answer()

@dp.message_handler(commands=["work"])
async def bonus(message: types.Message):
    cur = con.cursor()
    if cur.execute(f"SELECT userid FROM users WHERE userid = {message.from_user.id}").fetchone() is None:
        print(f"Work guard event \nAuthor message: {message.from_user.full_name}")
        await message.reply("Вы не зарегистрированны! Пожалуйста, используйте /create, для регистрации в боте!")
    else:
        print(f"Warning! Work event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
        from random import randint
        znk = {1: "+", 2: "-", 3: "*"}
        z_id = randint(1, 3)
        num1 = randint(-100, 900)
        num2 = randint(-100, 900)
        quest = f"{num1} {znk[z_id]} {num2}"
        veryfi = 0
        match z_id:
            case 1:
                veryfi = num1 + num2
            case 2:
                veryfi = num1 - num2
            case 3:
                veryfi = num1 * num2
        print(veryfi)
        qu1 = veryfi + 4 + (veryfi % 7)
        qu2 = veryfi + 11 - (veryfi // 5)
        qu3 = veryfi // 3 + (veryfi // 5)
        qu4 = veryfi - (veryfi % 11)
        v1 = "n"
        v2 = "n"
        v3 = "n"
        v4 = "n"
        ver_id = randint(1, 4)
        match ver_id:
            case 1:
                qu1 = veryfi
                v1 = "y"
            case 2:
                qu2 = veryfi
                v2 = "y"
            case 3:
                qu3 = veryfi
                v3 = "y"
            case 4:
                qu4 = veryfi
                v4 = "y"
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text=f"{qu1} ", callback_data=f"{v1}"))
        keyboard.add(types.InlineKeyboardButton(text=f"{qu2}", callback_data=f"{v2}"))
        keyboard.add(types.InlineKeyboardButton(text=f"{qu3}", callback_data=f"{v3}"))
        keyboard.add(types.InlineKeyboardButton(text=f"{qu4}", callback_data=f"{v4}"))
        await message.reply(f"Решите пример: {quest}", reply_markup=keyboard)

@dp.callback_query_handler(text="n")
async def work(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    await call.message.answer("Неверно.")
    await call.answer()
    with con:
        cur = con.cursor()
        cur.execute(f"""UPDATE users SET strike = 0 WHERE userid = {call.from_user.id}""")
        con.commit()

@dp.callback_query_handler(text="y")
async def work(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    from random import randint
    coin = randint(1, 6)
    coins = f"{coin} монетки"
    match coin:
        case 1:         coins = f"{coin} монетка"
        case [5, 6]:    coins = f"{coin} монет"
    await call.message.answer(f"Правильно! Вам начисленно: {coins}.")
    await call.answer()
    with con:
        cur = con.cursor()
        cur.execute(f"""UPDATE users SET money = money + {coin} WHERE userid = {call.from_user.id}""")
        cur.execute(f"""UPDATE users SET strike = strike + 1 WHERE userid = {call.from_user.id}""")
        cur.execute(f"""SELECT strike FROM users WHERE userid = {call.from_user.id}""")
        pr = cur.fetchone()
        if pr[0] >= 3:
            gk = f"Ты ответил {pr[0]} раз подряд!"
            match pr[0]:
                case [3, 4]:
                    gk = f"Ты ответил {pr[0]} раза подряд!"
            await call.message.answer(f"{gk} В награду, ты получишь {pr[0] - 1} смолы ")
            cur.execute(f"""UPDATE users SET smol = smol + {pr[0] - 1} WHERE userid = {call.from_user.id}""")
        con.commit()

@dp.message_handler(commands=["profile", "prof"])
async def profile(message: types.Message):
    cur = con.cursor()
    if cur.execute(f"SELECT userid FROM users WHERE userid = {message.from_user.id}").fetchone() is None:
        print(f"Profile guard event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
        await message.reply("Вы не зарегистрированны! Пожалуйста, используйте /create, для регистрации в боте!")
    else:
        with con:
            print(f"Warning! Profile event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
            cur = con.cursor()
            if cur.execute(f"SELECT grup FROM prof WHERE userid = {message.from_user.id}").fetchone() is None:
                cur.execute(f"""SELECT * FROM users WHERE userid = {message.from_user.id}""")
                pr = cur.fetchone()
                await message.reply(f"Beta profile! \nВаш профиль: \nИмя: {pr[1]}\nМонет: {pr[2]}\nСмола времени: {pr[3]}\nКол-во ответ подряд: {pr[4]}")
            else:
                cur.execute(f"""SELECT * FROM users WHERE userid = {message.from_user.id}""")
                pr = cur.fetchone()
                cur.execute(f"""SELECT * FROM users WHERE userid = {message.from_user.id}""")
                cur.execute(f"""SELECT grup, gpt FROM prof WHERE userid = {message.from_user.id}""")
                p = cur.fetchone()
                await message.reply(f"Beta profile! \nВаш профиль: \nИмя: {pr[1]}\nГруппа: {p[0]}\nМонет: {pr[2]}\nСмола времени: {pr[3]}\nКол-во ответ подряд: {pr[4]}\nДоступ к gpt: {p[1]}")

num = 0
@dp.message_handler(commands=["random"])
async def random(message: types.Message):
    cur = con.cursor()
    if cur.execute(f"SELECT userid FROM users WHERE userid = {message.from_user.id}").fetchone() is None:
        print(f"Random guard event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
        await message.reply("Вы не зарегистрированны! Пожалуйста, используйте /create, для регистрации в боте!")
    else:
        print(f"Warning! Random event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
        from random import randint
        global num
        num = randint(1, 6)
        print(num)
        v1 = "-"
        v2 = "-"
        v3 = "-"
        v4 = "-"
        v5 = "-"
        v6 = "-"
        match num:
            case 1:
                v1 = "+"
            case 2:
                v2 = "+"
            case 3:
                v3 = "+"
            case 4:
                v4 = "+"
            case 5:
                v5 = "+"
            case 6:
                v6 = "+"
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="1", callback_data=f"{v1}"))
        keyboard.add(types.InlineKeyboardButton(text="2", callback_data=f"{v2}"))
        keyboard.add(types.InlineKeyboardButton(text="3", callback_data=f"{v3}"))
        keyboard.add(types.InlineKeyboardButton(text="4", callback_data=f"{v4}"))
        keyboard.add(types.InlineKeyboardButton(text="5", callback_data=f"{v5}"))
        keyboard.add(types.InlineKeyboardButton(text="6", callback_data=f"{v6}"))
        await message.reply("Отгадай число от 1 до 6-ти.", reply_markup=keyboard)

@dp.callback_query_handler(text="-")
async def random(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    global num
    await call.message.answer(f"Неверное число! Правильно число: {num}")
    await call.answer()
    with con:
        cur = con.cursor()
        cur.execute(f"""UPDATE users SET strike = 0 WHERE userid = {call.from_user.id}""")
        con.commit()

@dp.callback_query_handler(text="+")
async def random(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    from random import randint
    coin = randint(5, 20)
    coins = f"{coin} монеток"
    global num
    await call.message.answer(f"Правильно! Загаданное число: {num} Вам начисленно: {coins}.")
    await call.answer()
    with con:
        cur = con.cursor()
        cur.execute(f"""UPDATE users SET money = money + {coin} WHERE userid = {call.from_user.id}""")
        cur.execute(f"""UPDATE users SET strike = strike + 1 WHERE userid = {call.from_user.id}""")
        cur.execute(f"""SELECT strike FROM users WHERE userid = {call.from_user.id}""")
        pr = cur.fetchone()
        if pr[0] >= 3:
            gk = f"Ты ответил {pr[0]} раз подряд!"
            match pr[0]:
                case [3, 4]:
                    gk = f"Ты ответил {pr[0]} раза подряд!"
            await call.message.answer(f"{gk} В награду, ты получишь {pr[0] * 2} смолы ")
            cur.execute(f"""UPDATE users SET smol = smol + {pr[0] * 2} WHERE userid = {call.from_user.id}""")
        con.commit()

@dp.message_handler(commands=["shop"])
async def shop(message: types.Message):
    cur = con.cursor()
    if cur.execute(f"SELECT userid FROM users WHERE userid = {message.from_user.id}").fetchone() is None:
        print(f"Shop guard event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
        await message.reply("Вы не зарегистрированны! Пожалуйста, используйте /create, для регистрации в боте!")
    else:
        print(f"Shop event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
        await message.reply('Магазин: \nЧай [1] - 50 монет;\nКофе [2] - 50 монет;\nД... Даркус? [3] - 999999 смолы;\nОчень нужная фигня [4] - 1000 cмолы;\nДоступ к GPT4 в боте[5] - 50 смолы или 1000 монет (приоритет оплаты: смола).')

@dp.message_handler(commands=["buy"])
async def buy(message: types.Message):
    cur = con.cursor()
    if cur.execute(f"SELECT userid FROM users WHERE userid = {message.from_user.id}").fetchone() is None:
        print(f"Buy guard event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
        await message.reply("Вы не зарегистрированны! Пожалуйста, используйте /create, для регистрации в боте!")
    else:
        print(f"Buy event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
        memory = message.get_args()
        result = memory.split(" ")
        if result[0] == '1':
            await message.answer("Я тоже люблю чай, но к сожалению пока не могу тебе его налить. Пока держи такой чай: 🍵")
        elif result[0] == '2':
            await message.answer("Я тоже хотела бы кофе, но он где-то застрял опять!")
        elif result[0] == '3':
            await message.answer("Ну... Допустим, что у тебя столько смолы ЕСТЬ... Вопрос: а откуда ты её достал?")
        elif result[0] == '4':
            cur = con.cursor()
            cur.execute(f"""SELECT smol FROM users WHERE userid = {message.from_user.id}""")
            pr = cur.fetchone()
            if pr[0] < 1000:
                await message.answer("У вас нет мани. Спасибо.")
            else:
                media = InputFile(r"media\morhu.gif")
                await message.answer("Спасибо за покупку! Вы купили настоящее нихуя, и призвали моржу, который спиздил у вас всю смолу!")
                await bot.send_document(message.from_user.id, media)
                print(f"Warning! Buy 4 \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
                with con:
                    cur = con.cursor()
                    cur.execute(f"""UPDATE users SET smol = 0 WHERE userid = {message.from_user.id}""")
                    con.commit()
        elif result[0] == '5':
            cur = con.cursor()
            result1 = cur.execute(f"SELECT userid FROM prof WHERE userid = {message.from_user.id}").fetchone()
            result2 = cur.execute(f"SELECT gpt FROM prof WHERE userid = {message.from_user.id}").fetchone()
            pr = cur.execute(f"""SELECT smol, money FROM users WHERE userid = {message.from_user.id}""").fetchone()
            print(result1, result2, pr)
            if (pr[0] < 50 and pr[1] < 1000) or result1[0] is None or result2[0] == 1:
                await message.answer("У вас недостаточно смолы и монет, и/или вы не верифицированны, или у вас уже есть доступ.")
            else:
                if pr[0] < 50:
                    await message.answer("Спасибо за покупку! С вашего счёта были списанны монеты. Доступ к GPT открыт! Просто напиши сообщение любое сообщение.")
                    print(f"Warning! Buy 5 \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
                    with con:
                        cur = con.cursor()
                        cur.execute(f"""UPDATE users SET money = money - 1000 WHERE userid = {message.from_user.id}""")
                        cur.execute(f"UPDATE prof SET gpt = 1 WHERE userid = {message.from_user.id}")
                        con.commit()
                else:
                    await message.answer("Спасибо за покупку! С вашего счёта была списанна смола. Доступ к GPT открыт! Просто напиши сообщение любое сообщение.")
                    print(f"Warning! Buy 5 \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
                    with con:
                        cur = con.cursor()
                        cur.execute(f"""UPDATE users SET smol = smol - 50 WHERE userid = {message.from_user.id}""")
                        cur.execute(f"UPDATE prof SET gpt = 1 WHERE userid = {message.from_user.id}")
                        con.commit()
        else:
            await message.answer("Как использовать команду: \nКоманда пишется: /buy номер_товара_из_shop")

@dp.message_handler(commands=['feedback'])
async def cmd_feedback(message: types.Message):
    print(f"Feedback event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
    chatID = "942025817"
    if message.text == "/feedback":
        await message.reply("Чтобы написать сообщение создателю, напиши команду, и к ней текст. Пример команды: \n/feedback Приветик, как дела?")
    else:
        await message.answer("Сообщение отправлено!")
        await bot.forward_message(chatID, message.chat.id, message.message_id)

@dp.message_handler(commands=['verify'])
async def cmd_verify(message: types.Message):
    cur = con.cursor()
    if cur.execute(f"SELECT userid FROM prof WHERE userid = {message.from_user.id}").fetchone() is not None:
        print(f"Verefy prof event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
        await message.reply("Вы уже верифицированны!")
    elif cur.execute(f"SELECT userid FROM users WHERE userid = {message.from_user.id}").fetchone() is None:
        print(f"Verefy prof guard event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
        await message.reply("Вы не зарегистрированны! Пожалуйста, используйте /create, для регистрации в боте!")
    else:
        print(f"Warning! Verefy event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Да", callback_data="t"))
        keyboard.add(types.InlineKeyboardButton(text="Нет", callback_data="f"))
        await message.answer("Верификация профиля - ключ к открытию большинства возможностей бота! Но она стоит денег, а именно 500 монет. Готов ли ты верифицироваться?", reply_markup=keyboard)

@dp.callback_query_handler(text="t")
async def veryfi_bd(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    cur = con.cursor()
    cur.execute(f"""SELECT money FROM users WHERE userid = {call.from_user.id}""")
    pr = cur.fetchone()
    if pr[0] < 500:
        await call.message.answer("У вас недостаточно монет, для совершения верификации профиля!")
        await call.answer()
    else:
        await call.message.answer("Ваша верификация завершена!")
        print(f"Warning! Verify profile \nAuthor message: {call.from_user.full_name}({call.from_user.username})")
        await call.answer()
        with con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS prof(
            userid INT PRIMARY KEY,
            grup TEXT,
            gpt INT)""")
            cur.execute(f"""UPDATE users SET money = money - 500 WHERE userid = {call.from_user.id}""")
            con.commit()

            cur.execute(f"""INSERT INTO prof (userid, grup, gpt)
            VALUES('{call.from_user.id}', "BETATESTER", 0)""")

@dp.callback_query_handler(text="f")
async def verify_bd(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    await call.message.answer("Верификация отменена.")
    await call.answer()

@dp.message_handler(commands=["admin_panel"])
async def admin_panel(message: types.Message):
    cur = con.cursor()
    if cur.execute(f"SELECT userid FROM prof WHERE userid = {message.from_user.id}").fetchone() is None:
        print(f"admin_panel stop event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
        await message.reply("Вы не верифицированны! Используйте /veryfi , для верификации!")
    else:
        print(f"admin_panel event \nAuthor message: {message.from_user.full_name}({message.from_user.username})")
        cur.execute(f"""SELECT grup FROM prof WHERE userid = {message.from_user.id}""")
        p = cur.fetchone()
        media = InputFile(r"media\big_brain.mp4")
        await message.answer(f"Обычные люди: Спокойно работают, и зарабатывают. \nМегамозг: вызывают админ панель, имея группу: {p[0]}.")
        await bot.send_video(message.from_user.id, media)

@dp.message_handler(commands=['clear'])
async def process_clear_command(message: types.Message):
    cur = con.cursor()
    if cur.execute(f"SELECT userid FROM prof WHERE userid = {message.from_user.id}").fetchone() is None or cur.execute(f"SELECT gpt FROM prof WHERE userid = {message.from_user.id}").fetchone() == 0:
        await message.answer("Вы не верифицированны, или у вас нет доступа к gpt. Получить доступ можно купив в магазине.")
    else:
        user_id = message.from_user.id
        user_name = message.from_user.full_name
        await message.reply(clear_command(user_id, user_name))

@dp.message_handler(content_types=['text'])
async def get_text_messages(message: types.Message):
    cur = con.cursor()
    cur.execute(f"""SELECT gpt FROM prof WHERE userid = {message.from_user.id}""")
    p = cur.fetchone()
    if cur.execute(f"SELECT userid FROM prof WHERE userid = {message.from_user.id}").fetchone() is not None and p[0] == 1:
        print(f'GPT4 event. Text message: {message.text} \nAuthor message: {message.from_user.full_name}({message.from_user.username})')
        user_id = message.from_user.id
        user_input = message.text

        if user_id not in conversation_history:
            conversation_history[user_id] = []

        conversation_history[user_id].append({"role": "user", "content": user_input})
        conversation_history[user_id] = trim_history(conversation_history[user_id])

        chat_history = conversation_history[user_id]

        try:
            response = await g4f.ChatCompletion.create_async(
                model=g4f.models.default,
                messages=chat_history,
                provider=g4f.Provider.Liaobots,
            )
            chat_gpt_response = response
        except Exception as e:
            print(f"{g4f.Provider.Liaobots.__name__}:", e)
            chat_gpt_response = "Извините, произошла ошибка. Сообщение об инциденте отправленно."

        conversation_history[user_id].append({"role": "assistant", "content": chat_gpt_response})
        print(conversation_history)
        length = sum(len(message["content"]) for message in conversation_history[user_id])
        print(length)
        await message.answer(chat_gpt_response)
    else:
        print(f'Message event. Text message: {message.text} \nAuthor message: {message.from_user.full_name}({message.from_user.username})')
        messg = {1: "а", 2: "чем занимаешься?", 3: "ты девочка?", 4: "привет", 5: "хорошо", 6: "плохо", 7: "нормально", 8: "отлично", 9: "дай рыбку", 10: "ало", 11: "ку-ку", 12: "хай", 13: "как дела?", 14: "спокойной ночи", 15: "я люблю тебя"}
        aut = {1: "Я не вижу на тебе жабров и плавников... Ты не Гавр Гура!", 2: "Как и всегда, ловлю рыбку.", 3: "Да, я великолепнейшая кошка Кяру! Бойся, и уважай меня!", 4: "Приветик! Чем порадуешь? Надеюсь вкусной рыбкой.", 5: "Хорошо, это хорошо, но явно не предел!", 6: "Выше нос! Даже у меня бывают плохие дни, когда опять надо питаться жуками...", 7: "Как то сухо... А может рыбки?", 8: "Отличное настроение, залог успешного дня!", 9: "Моя рыбка! И вообще, мне самой мало!", 10: "Я тебе не абонент! У меня нет телефона! И вообще... Пришли мне фото рыбки... А лучше дай живой!", 11: "Я не кукушка! Хоть и знаю, что ты так приветствуешь меня, но можно и более вежливей!", 12: "Я должна ответить на английском? Ну хорошо, こんにちは、魚", 13: "Дела прекрасны! А у тебя?", 14: "Ага, спокойной ночи, но учти! Будешь храпеть, столкну с кровати", 15: "Ч... Чего?! Т... Ты точно путаешь!"}
        for i in range(1, 16):
            print(fuzz.WRatio(messg[i], message.text.lower()))
            if fuzz.WRatio(messg[i], message.text.lower()) >= 88:
                await message.reply(aut[i])
                break
            elif i == 15:
                await message.reply("Я не умею распознавать все тексты...")

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)