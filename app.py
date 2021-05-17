import telebot
from config import keys, TOKEN
from extensions import ConversionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_message(message: telebot.types.Message):
    text = "To work with the bot input currencies as:" \
           " \n<from>  <to>  <how much>\n" \
           "For example: \n" \
           "Ethereum Dollar 1 \n" \
           "(lower case is also possible)\n" \
           "To see available currencies type /values \n" \
           "To see this message again type /start or /help"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "List of currencies:"
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConversionException('Unexpected element amount (should be 3).')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f"APIException:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Couldn't process command:\n{e}")
    else:
        text = f' Price for {amount} {quote} in {base} - {total_base * float(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling()
