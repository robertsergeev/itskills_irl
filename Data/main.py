import telebot
import matplotlib.pyplot as plt
from io import BytesIO

token = 'token'
bot = telebot.TeleBot(token)

user_data = {}

@bot.message_handler(commands=['start'])
def ask_for_info(message):
    start_message = ('Привет, я бот, который поможет тебе следить за количеством выпитой воды в день!\n\n'
                     'Для начала, надо посчитать сколько воды тебе надо пить в день, для этого пришли свой рост и вес в таком формате:\n\n'
                     'вес, рост')
    bot.send_message(message.chat.id, start_message)
    bot.register_next_step_handler(message, get_user_info)

def get_user_info(message):
    try:
        weight, height = map(float, message.text.split(','))
        daily_water_intake = (weight * 30 / 1000) + (height * 0.4 / 100)
        user_data[message.chat.id] = {
            'weight': weight,
            'height': height,
            'daily_water_intake': daily_water_intake,
            'today_intake': []
        }
        response_message = f'Тебе нужно пить примерно {daily_water_intake:.2f} литров воды в день.'
    except ValueError:
        response_message = 'Пожалуйста, введите данные в правильном формате: вес, рост (например, 70, 175).'
        bot.register_next_step_handler(message, get_user_info)
    
    bot.send_message(message.chat.id, response_message)

@bot.message_handler(commands=['add'])
def ask_for_water_amount(message):
    if message.chat.id in user_data:
        bot.send_message(message.chat.id, 'Пришли количество воды, которое ты выпил в миллилитрах!')
        bot.register_next_step_handler(message, count_water)
    else:
        bot.send_message(message.chat.id, 'Сначала отправьте свои данные с помощью команды /start.')

def count_water(message):
    try:
        water_count = int(message.text)
        user_data[message.chat.id]['today_intake'].append(water_count)
        total_intake = sum(user_data[message.chat.id]['today_intake'])
        daily_intake = user_data[message.chat.id]['daily_water_intake'] * 1000  
        response_message = f'Данные были добавлены, ты выпил {total_intake} мл из {daily_intake} мл.'
    except ValueError:
        response_message = 'Пожалуйста, введите данные в миллилитрах (например, 250).'
        bot.register_next_step_handler(message, count_water)
    
    bot.send_message(message.chat.id, response_message)

@bot.message_handler(commands=['check'])
def send_progress(message):
    if message.chat.id in user_data:
        user_info = user_data[message.chat.id]
        total_intake = sum(user_info['today_intake'])
        daily_intake = user_info['daily_water_intake'] * 1000  
        image = create_progress_image(total_intake, daily_intake)
        bot.send_photo(message.chat.id, image)
    else:
        bot.send_message(message.chat.id, 'Сначала отправьте свои данные с помощью команды /start.')

def create_progress_image(current_intake, daily_intake):
    fig, ax = plt.subplots(figsize=(6, 4))

    if current_intake <= daily_intake:
        ax.barh(['Прогресс'], [current_intake], color='blue', label='Выпито')
    else:
        ax.barh(['Прогресс'], [daily_intake], color='blue', label='Цель')
        ax.barh(['Прогресс'], [current_intake - daily_intake], left=[daily_intake], color='red', label='Избыток')

    ax.set_xlim(0, max(current_intake, daily_intake) * 1.1)
    ax.set_xlabel('Миллилитры')
    ax.set_title('Прогресс выпитой воды за день')
    ax.legend()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return buf

bot.polling()
