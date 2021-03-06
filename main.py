from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, Filters, MessageHandler
import os
from Bot import Bot


# load_dotenv()
TOKEN = "Token"

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
    f1_btn_conversation_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(bot.f1_input_RR_btn, pattern="op1")],
        states={
            0: [MessageHandler(Filters.text & ~Filters.command, bot.f1_input_a)],
            1: [MessageHandler(Filters.text & ~Filters.command, bot.f1)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(f1_btn_conversation_handler)

    f1_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("f1", bot.f1_input_RR)],
        states={
            0: [MessageHandler(Filters.text & ~Filters.command, bot.f1_input_a)],
            1: [MessageHandler(Filters.text & ~Filters.command, bot.f1)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(f1_conversation_handler)

    f2_btn_conversation_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(bot.f2_input_RR_btn, pattern="op2")],
        states={
            0: [MessageHandler(Filters.text & ~Filters.command, bot.f2_input_a)],
            1: [MessageHandler(Filters.text & ~Filters.command, bot.f2_input_i0)],
            2: [MessageHandler(Filters.text & ~Filters.command, bot.f2_result)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(f2_btn_conversation_handler)

    f2_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("f2", bot.f2_input_RR)],
        states={
            0: [MessageHandler(Filters.text & ~Filters.command, bot.f2_input_a)],
            1: [MessageHandler(Filters.text & ~Filters.command, bot.f2_input_i0)],
            2: [MessageHandler(Filters.text & ~Filters.command, bot.f2_result)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(f2_conversation_handler)
    
    f3_btn_conversation_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(bot.f3_input_btn, pattern="op3")],
        states={
            0: [MessageHandler(Filters.text & ~Filters.command, bot.f3)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(f3_btn_conversation_handler)

    f3_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("f3", bot.f3_input)],
        states={
            0: [MessageHandler(Filters.text & ~Filters.command, bot.f3)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(f3_conversation_handler)

    f4_btn_conversation_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(bot.f4_input_V_btn, pattern="op4")],
        states={
            0: [MessageHandler(Filters.text & ~Filters.command, bot.f4_input_E)],
            1: [MessageHandler(Filters.text & ~Filters.command, bot.f4_input_K)],
            2: [MessageHandler(Filters.text & ~Filters.command, bot.f4)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(f4_btn_conversation_handler)

    f4_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("f4", bot.f4_input_V)],
        states={
            0: [MessageHandler(Filters.text & ~Filters.command, bot.f4_input_E)],
            1: [MessageHandler(Filters.text & ~Filters.command, bot.f4_input_K)],
            2: [MessageHandler(Filters.text & ~Filters.command, bot.f4)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(f4_conversation_handler)

    # Inicir el bot, escuchando las peticiones del servidor.
    updater.start_polling()
    # Mantener el bot ejecutándose hasta que ocurra alguna interrupción.
    updater.idle()


if __name__ == '__main__':
    main()
