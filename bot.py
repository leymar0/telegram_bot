import os
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
import configparser as cfg
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
import qrcode
from ficherosOverlink import genFicherosOverlink


INPUT_TEXT = 0
INPUT_AGENTE = 0



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

    btnQR = InlineKeyboardButton(
        text='Generar código QR',
        callback_data='qr'
    )


    btnGenerarFicheros = InlineKeyboardButton(
        text='Generar ficheros Overlink',
        callback_data='generaFicheros'
    )

    update.message.reply_text(
        text = 'Haz click en un botón',
        reply_markup=InlineKeyboardMarkup([
            [btnAbrirBilo, btnAbrirWhatsapp],
            # [btnQR],
            [btnGenerarFicheros]
        ])
    )

    return INPUT_TEXT




def retry(update, context):
    update.message.reply_text('No conozco a ese hombre')


def qr_command_handler(update, context):
    update.message.reply_text('Envíame un texto para convertirlo en QR')

    return INPUT_TEXT









def input_generaFicheros(update, context):

    # Recoge las variables necesarias
    text = update.message.text
    chat = update.message.chat
    agente = ""
    msg = ""

    # Simula que escribe
    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
    )
    
    print('Para que me haga el commit')

    # Prepara ficheros dependiendo de quién pasa los datos

    if text == '/todos':
        agente = None
        msg = 'Generando ficheros para todos los comerciales\nEste proceso puede tardar más de una hora.'
    else:
        agente = text
        msg = f'Generando ficheros para el agente {text}'
    
    pid = genFicherosOverlink(update, agente)
    update.message.reply_text(f'{msg}\nPID del proceso: {pid}')

    return ConversationHandler.END

def generaFicheros_callback_handler(update, context):
    
    query = update.callback_query
    query.answer()

    # Modifica el valor del último mensaje y lo cambia por un texto básico
    query.edit_message_text(
        text= 'Indique el agente para generar datos\nEscriba /todos para una generación masiva'
    )

    return INPUT_TEXT



def generaAllFiles(update, context):

    update.message.reply_text('Generando ficheros para todos los comerciales\nEste proceso puede tardar más de una hora.')
    # r = genFicherosOverlink(chat_id, agente)









def qr_callback_handler(update, context):
    
    query = update.callback_query
    query.answer()

    # Modifica el valor del último mensaje y lo cambia por un texto básico
    query.edit_message_text(
        text= 'Envíame un texto para convertirlo en QR'
    )

    return INPUT_TEXT


def input_text(update, context):

    texto = update.message.text
 
    filename = generate_qr(texto)

    chat = update.message.chat

    print(f'Codigo QR generado por {update.message.chat.username}')

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

    # Se migra la lectura del token a una variable de sistema
    token = os.environ.get('TOKEN_TELEGRAM_IT', 'Debe crear una variable de sistema con el token correcto')

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
            # CommandHandler('gagagas', qr_command_handler),
            CallbackQueryHandler(pattern='qr', callback=qr_callback_handler)
            # CallbackQueryHandler(pattern='generaFicheros', callback=generaFicheros_callback_handler)
        ],
        states={
            INPUT_TEXT: [
                MessageHandler(Filters.text, input_text)
            ]
        },

        fallbacks=[]
    ))


    dp.add_handler(ConversationHandler(
        entry_points=[
            # CommandHandler('todos', generaAllFiles_command_handler),
            CallbackQueryHandler(pattern='generaFicheros', callback=generaFicheros_callback_handler)
        ],
        states={
            INPUT_TEXT: [
                MessageHandler(Filters.text, input_generaFicheros)
            ]
        },

        fallbacks=[]
    ))

    # Con esto el bot se queda en un ciclo infito para revisar si un usuario envia un mensaje
    updater.start_polling()    
    updater.idle()