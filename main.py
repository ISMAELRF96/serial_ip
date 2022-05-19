import socket

import psycopg2
import binascii
import time
import serial

def leer_sonda():
    echoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    # echoSocket.connect(("179.133.125.164", 5001));
    echoSocket.connect(("localhost", 7777));

    while 1:
        # mandar comando para obtener medidas de sonda U_52
        echoSocket.send("#RD@XX\r\n".encode('utf-8'));
        # se usa site name para identificar la sonda cuando hay varias
        msg = echoSocket.recv(1024);
        print(msg)
        medidas=parametros5(msg.decode(),id=0)
        # return msg
    # Print lista de medidas
    # print(to_table(medidas))
    # print(medidas);
# leer datos de la sonda a traves de IP


def parametros5(cadena,id):
    param=[]
    param.append(cadena)
    param.append(id)
    x=31
    for i in range(13):
        param.append(cadena[x:x+5])
        x=x+8
    param.remove('-----')
    param.remove('-----')
    return param
# funcion para extraer las medidas de la trama que envia la sonda


def to_table(lista):
    dict_tmp = [{'Temp': lista[0], 'PH': lista[1], 'PHmv': lista[2], 'ORP': lista[3], 'Conductividad': lista[4],
                 'Turb': lista[5], 'DissOx': lista[6], 'TDS': lista[7], 'Salinity': lista[8], 'SeawaterSG': lista[9],
                  'OD%': lista[11]}]
    print(dict_tmp)
    return dict_tmp
# para poder ver los datos leidos de la sonda con etiquetas


def subir (lista):
    try:
        conn = psycopg2.connect(dbname='sonda', user='postgres', host='localhost', password='Mass2077')
    except:
        print("I am unable to connect to the database")

    cursor = conn.cursor()
    print(str(conn.get_dsn_parameters()) + "/n")
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected into the - " + str(record))

    if lista.len()<13:#usar espacios en la lista ispace()
        cursor.execute(
            """INSERT INTO medidas_raw(raw_input,id) VALUES (%s,%s)""",lista[0],lista[1])
    else:
        #query = "INSERT INTO medidas_raw(temperatura,Ph,Phmv,ORP,Cond,Turb,DissOx,TDS,Salinity,SWSG,DissOxpercent) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(
            """INSERT INTO medidas_raw(raw_input,id,temperatura,Ph,Phmv,ORP,Cond,Turb,DissOx,TDS,Salinity,SWSG,DissOxpercent) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            lista)

    conn.commit()
    cursor.close()
    conn.close()
# funcion para subir los datos a postgres


leer_sonda()






