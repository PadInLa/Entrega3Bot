from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv
import os
from Bot import Bot


load_dotenv()
TOKEN = "2145063102:AAGvc8R9Q7ifSHBhd2OIMPQ0jIN1u78wmy8"


def main():
    # Establece la conexión entre nuestro programa y el Bot de Telegram.
    updater = Updater(TOKEN, use_context=True) # Ingresar el TOKEN de nuestro bot.
    dp = updater.dispatcher # Despachador de solicitudes.

    # Instanciamos nuestro objeto bot
    bot = Bot()

    # Establecer los comandos que escuchará el bot.
    dp.add_handler(CommandHandler("start", bot.start))
    dp.add_handler(CommandHandler("ayuda", bot.ayuda))
    dp.add_handler(CommandHandler("f1", bot.f1))
    dp.add_handler(CommandHandler("f2", bot.f2))
    dp.add_handler(CommandHandler("f3", bot.f3))
    dp.add_handler(CommandHandler("f4", bot.f4))
    # Manejar los Callback de menú de ayudas.
    dp.add_handler(CallbackQueryHandler(bot.menu_opciones, pattern="op1"))
    dp.add_handler(CallbackQueryHandler(bot.menu_opciones, pattern="op2"))
    dp.add_handler(CallbackQueryHandler(bot.menu_opciones, pattern="op3"))
    dp.add_handler(CallbackQueryHandler(bot.menu_opciones, pattern="op4"))
    # Inicir el bot, escuchando las peticiones del servidor.
    updater.start_polling()
    # Mantener el bot ejecutándose hasta que ocurra alguna interrupción.
    updater.idle()


if __name__ == '__main__':
    main()