from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, Filters, MessageHandler
# from dotenv import load_dotenv
import os
from Bot import Bot


# load_dotenv()
TOKEN = "2145063102:AAGvc8R9Q7ifSHBhd2OIMPQ0jIN1u78wmy8"

def cancel(update, context):
    return ConversationHandler.END

def main():
    # Establece la conexión entre nuestro programa y el Bot de Telegram.
    updater = Updater(TOKEN, use_context=True) # Ingresar el TOKEN de nuestro bot.
    dp = updater.dispatcher # Despachador de solicitudes.

    # Instanciamos nuestro objeto bot
    bot = Bot()

    # Establecer los comandos que escuchará el bot.
    dp.add_handler(CommandHandler("start", bot.start))
    dp.add_handler(CommandHandler("ayuda", bot.ayuda))
    # Manejar los Callback de menú de ayudas.
    f1_conversation_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(bot.f1_input, pattern="op1")],
        states={
            0: [MessageHandler(Filters.text & ~Filters.command, bot.f1)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(f1_conversation_handler)

    f2_conversation_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(bot.f2_input_RR, pattern="op2")],
        states={
            0: [MessageHandler(Filters.text & ~Filters.command, bot.f2_input_a)],
            1: [MessageHandler(Filters.text & ~Filters.command, bot.f2_input_i0)],
            2: [MessageHandler(Filters.text & ~Filters.command, bot.f2_result)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(f2_conversation_handler)
    # dp.add_handler(CallbackQueryHandler(bot.menu_opciones, pattern="op1"))
    # dp.add_handler(CallbackQueryHandler(bot.menu_opciones, pattern="op2"))
    dp.add_handler(CallbackQueryHandler(bot.menu_opciones, pattern="op3"))
    dp.add_handler(CallbackQueryHandler(bot.menu_opciones, pattern="op4"))
    # Inicir el bot, escuchando las peticiones del servidor.
    updater.start_polling()
    # Mantener el bot ejecutándose hasta que ocurra alguna interrupción.
    updater.idle()


if __name__ == '__main__':
    main()