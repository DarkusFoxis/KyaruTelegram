import logging
from aiogram import Bot, Dispatcher, types
import g4f
from aiogram.utils import executor

# Включите логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token="6050360696:AAGc2Y7ShpZmEUyS3lOz48BZIXsLXYDAWQg")
dp = Dispatcher(bot)

# Словарь для хранения истории разговоров
conversation_history = {}

# Функция для обрезки истории разговора
def trim_history(history, max_length=16384):
    current_length = sum(len(message["content"]) for message in history)
    while history and current_length > max_length:
        removed_message = history.pop(0)
        current_length -= len(removed_message["content"])
    return history


@dp.message_handler(commands=['clear'])
async def process_clear_command(message: types.Message):
    user_id = message.from_user.id
    conversation_history[user_id] = []
    await message.reply("История диалога очищена.")
    print(f"{message.from_user.full_name}({user_id}) очистил диалог.")

@dp.message_handler(commands=['start'])
async def starting_command(message: types.Message):
    user_id = message.from_user.id
    conversation_history[user_id] = []
    await message.answer("Привет! Начинаем новую историю со мной!")
    print(f"{message.from_user.full_name}({user_id}) начинает новый диалог.")

# Обработчик для каждого нового сообщения
@dp.message_handler()
async def send_welcome(message: types.Message):
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
        print(f"{g4f.Provider.GeekGpt.__name__}:", e)
        chat_gpt_response = "Извините, произошла ошибка."

    conversation_history[user_id].append({"role": "assistant", "content": chat_gpt_response})
    print(conversation_history)
    length = sum(len(message["content"]) for message in conversation_history[user_id])
    print(length)
    await message.answer(chat_gpt_response)


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)