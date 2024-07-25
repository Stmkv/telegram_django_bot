import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from dotenv import load_dotenv





def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton('процедуры', callback_data='процедуры')],
        [InlineKeyboardButton('салоны', callback_data='салон')],
        [InlineKeyboardButton('мастера', callback_data='мастер')],
        [InlineKeyboardButton('о нас', callback_data='хотите узнать о нас '),
         InlineKeyboardButton('связь с менеджером', callback_data='контакты менеджера')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите опцию:', 
                              reply_markup=reply_markup)


def pay(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    title = "Тестовая оплата"
    description = "Оплата услуг салона Beauty-City"
    payload = "Стрижка машинкой"
    currency = "RUB"
    prices = [LabeledPrice("Тестовая оплата", 10000)]

    provide_token = context.bot_data['provide_token']# Цена в копейках

    context.bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token=provide_token,
        currency=currency,
        prices=prices,
        start_parameter="test-payment",
        need_name=True,
        need_phone_number=True,
    )


def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f'Вы выбрали: {query.data}')


def main():
    load_dotenv()
    provide_token = os.environ['PAYMENT_PROVIDER_TOKEN']
    telegram_token = os.environ['BOT_TOKEN']
    updater = Updater(telegram_token, use_context=True)

    updater.dispatcher.bot_data['provide_token'] = provide_token
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('pay', pay))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()