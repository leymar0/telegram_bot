from morales import query, converter

from datetime import datetime,timedelta
from decimal import Decimal
import random
import os
from subprocess import Popen

import pdfkit as pdf

import requests as rq






def genFicherosOverlink(update, agente=None):

    print(update)
    print(f'Chat: {update.message.chat}')

    sql = f"select permiso from Usuarios where chatid = '{update.message.chat.id}'"
    print(sql)
    datos = query.mariaDB(sql, 'BiloDB')
    print(datos)
    permiso = datos[0]['permiso']
    print(f'El permiso es {permiso}')
    # update.message.reply_text(f'{update.message.fisrt_name} el permiso es: {permiso} y el chat es {update.message.chat}')


    try:
        if permiso == 1:

            if agente is None:
                proceso = Popen("python \\\\192.168.1.163\\Morales\\bin\\python\\mantenimiento\\overlink\\generarArchivosOverlink\\index.py", shell=True)
            else:
                proceso = Popen(f"python \\\\192.168.1.163\\Morales\\bin\\python\\mantenimiento\\overlink\\generarArchivosOverlink\\index.py {agente}", shell=True)
                
            return proceso.pid
        else:
            return False
    except Exception as e:
        print(e)
        return False