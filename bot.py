from telegram.ext import Updater, CommandHandler


def start(update, context):
    update.message.reply_text('Hola, humano!')




# Esto quiere decir que el sistema va a empezar a ejecutarse por aquí
if __name__ == '__main__':

    updater = Updater(token='YOUR_TOKEN', use_context=True)

    # Es el encargado de enviar las acciones
    # Cuando entra un comando, pasa por el dispacher para saber lo que tiene que hacer
    dp = updater.dispatcher

    # Aquí se define lo que tiene que hacer el bot cuando recibe "start"
    dp.add_handler(CommandHandler('start', start))


    # Con esto el bot se queda en un ciclo infito para revisar si un usuario envia un mensaje
    updater.start_polling()    
    updater.idle()

