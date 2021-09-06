import os
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
import configparser as cfg
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
import qrcode


INPUT_TEXT = 0



def start(update, context):

    # update.message.reply_text('Hola, bienvenido, qué deseas hacer? \n\nUsa /qr para generar un código qr')

    btnAbrirBilo = InlineKeyboardButton(
        text='Abrir Bilo',
        url='http://bilo.morales.local/'
    )


    btnAbrirWhatsapp = InlineKeyboardButton(
        text='Abrir Whatsapp',
        url='https://web.whatsapp.com'
    )

    btnGenerarFicheros = InlineKeyboardButton(
        text='Generar ficheros Overlink',
        callback_data='qr'
    )



    update.message.reply_text(
        text = 'Haz click en un botón',
        reply_markup=InlineKeyboardMarkup([
            [btnAbrirBilo, btnAbrirWhatsapp],
            [btnGenerarFicheros]
        ])
    )



    return INPUT_TEXT

def retry(update, context):
    update.message.reply_text('No conozco a ese hombre')


def qr_command_handler(update, context):
    update.message.reply_text('Envíame un texto para convertirlo en QR')

    return INPUT_TEXT



def generaFicheros_callback_handler(update, context):
    
    query = update.callback_query

    # Da la respuesta al BOT como que está contestando a la petición del usuario
    query.answer()

    # Modifica el valor del último mensaje y lo cambia por un texto básico
    query.edit_message_text(
        text= 'Envíame un texto para convertirlo en QR'
    )

    return INPUT_TEXT







def input_text(update, context):

    texto = update.message.text
    print(texto)
 
    filename = generate_qr(texto)

    print(filename)

    chat = update.message.chat

    send_qr(filename, chat)

    return ConversationHandler.END

def generate_qr(texto):

    filename = texto + '.jpg'

    img = qrcode.make(texto)
    img.save(filename)

    return filename

def send_qr(filename, chat):

    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )

    chat.send_photo(
        photo=open(filename, 'rb')
    )

    os.unlink(filename)














# Esto quiere decir que el sistema va a empezar a ejecutarse por aquí
if __name__ == '__main__':

    print('Iniciando Bot')


    # Busca ruta donde esta alojado el token
    parser = cfg.ConfigParser()
    parser.read('\\\\192.168.1.159\\ficheros\\ADMINISTRACION\\Privado\\tokens\\telegram\\ItBot.cfg')
    token = parser.get('creds', 'token')


    updater = Updater(token=token, use_context=True)

    # Es el encargado de enviar las acciones
    # Cuando entra un comando, pasa por el dispacher para saber lo que tiene que hacer
    dp = updater.dispatcher

    # Aquí se define lo que tiene que hacer el bot cuando recibe "start"
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('Pablo', retry))    


    # Handler para generar QR con botones en el chat
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('qr', qr_command_handler),
            CallbackQueryHandler(pattern='qr', callback=generaFicheros_callback_handler)
        ],

        states={
            INPUT_TEXT: [
                MessageHandler(Filters.text, input_text)
            ]
        },

        fallbacks=[]
    ))


    # Handler para generar ficheros de Overlink
    dp.add_handler(ConversationHandler(
        entry_points=[],

        states={[]},

        fallbacks=[]
    ))



    # Con esto el bot se queda en un ciclo infito para revisar si un usuario envia un mensaje
    updater.start_polling()    
    updater.idle()