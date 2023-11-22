import telebot
from config import TOKEN, currencies
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\nСписок всех доступных валют: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def handle_values(message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        text += '\n' + key
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def handle_convert(message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неправильное количество параметров.')

        base, quote, amount = values
        total_price = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} — {total_price}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)




