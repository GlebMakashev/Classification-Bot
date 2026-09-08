#
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = '8780014826:aahbfdxonw9pf5ry3qhnszzbgd3rkapujfw'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
                               InlineKeyboardButton("No", callback_data="cb_no"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if not message.photo:
        return bot.reply_to(message, "Пожалуйста, отправьте фотографию.")
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    class_name, confidence_score = get_class(file_name)
    bot.reply_to(message, f"На фото '{class_name}' с вероятностью {confidence_score:.2f}%")



bot.polling()