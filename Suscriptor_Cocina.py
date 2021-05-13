import sys
import paho.mqtt.client
import json
import psycopg2

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='Casa/Cocina/#', qos=2)

def on_message(client, userdata, message):
    try:
    # Para conectarlo a mi BD  
        connection = psycopg2.connect(user="jwfzmnbf",
                                  password="iNootd8guPlSWTXSz2otlXx9EGxeCiGr",
                                  host="kashin.db.elephantsql.com",
                                  database="jwfzmnbf")
    
        cursor = connection.cursor()
        PayloadOriginal = json.loads(message.payload)
        print('------------------------------')
        print('payload: %s' % message.payload)

        # Query SQL para crear una Nueva Tabla para NEVERA
        if PayloadOriginal.get("TemperaturaNevera"):
            cursor.execute ('''CREATE TABLE IF NOT EXISTS Temperatura_Nevera
                            (ID SERIAL PRIMARY KEY NOT NULL,
                            Temperatura REAL NOT NULL,
                            Tiempo TIMESTAMP NOT NULL); ''')
            connection.commit()
            #print("La Tabla se ha creado satisfactoriamente en PostgreSQL ")

            cursor.execute(''' INSERT INTO Temperatura_Nevera (Tiempo, Temperatura)
                            VALUES (%(Tiempito)s, %(Temper)s);''',{'Tiempito': PayloadOriginal["Minuto"], 'Temper': PayloadOriginal["TemperaturaNevera"] })
            connection.commit()


        if PayloadOriginal.get("Hielo"):
            cursor.execute ('''CREATE TABLE IF NOT EXISTS Hielo_Nevera
                            (ID SERIAL PRIMARY KEY NOT NULL,
                            Tiempo TIMESTAMP NOT NULL,
                            Hielo REAL NOT NULL); ''')
            connection.commit()
            #print("La Tabla Hielo se ha creado satisfactoriamente en PostgreSQL ")
            cursor.execute(''' INSERT INTO Hielo_Nevera (Tiempo, Hielo)
                            VALUES (%(Tiempito)s, %(Hielos)s);''',{'Tiempito': PayloadOriginal["Minuto"], 'Hielos': PayloadOriginal["Hielo"] })
            connection.commit()

        # Query SQL para crear una Nueva Tabla para OLLA
        if PayloadOriginal.get("TemperaturaOlla"):
            cursor.execute ('''CREATE TABLE IF NOT EXISTS Temperatura_Olla
                            (ID SERIAL PRIMARY KEY NOT NULL,
                            Temperatura REAL NOT NULL,
                            Tiempo TIMESTAMP NOT NULL); ''')
            connection.commit()
            #print("La Tabla se ha creado satisfactoriamente en PostgreSQL ")

            cursor.execute(''' INSERT INTO Temperatura_Olla (Tiempo, Temperatura)
                            VALUES (%(Tiempito)s, %(Temper)s);''',{'Tiempito': PayloadOriginal["Segundo"], 'Temper': PayloadOriginal["TemperaturaOlla"] })
            connection.commit()


        if PayloadOriginal.get("Mensajito"):
            cursor.execute ('''CREATE TABLE IF NOT EXISTS Mensaje_Olla
                            (ID SERIAL PRIMARY KEY NOT NULL,
                            Tiempo TIMESTAMP NOT NULL,
                            Mensajito TEXT NOT NULL); ''')
            connection.commit()
            #print("La Tabla Mensaje se ha creado satisfactoriamente en PostgreSQL ")

            cursor.execute(''' INSERT INTO Mensaje_Olla (Tiempo, Mensajito)
                            VALUES (%(Tiempito)s, %(Mensajito)s);''',{'Tiempito': PayloadOriginal["Segundo"], 'Mensajito': PayloadOriginal["Mensajito"] })
            connection.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error mientras se recuperaba la data desde PostgreSQL", error)

    finally:
        # Cerrando la conexión con la BD
        if connection:
            cursor.close()
            connection.close()
            print("Fue cerrada la conexión con PostgreSQL")

def main():
	client = paho.mqtt.client.Client(client_id='MaryBeltran-SuscriptorCocina', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='127.0.0.1', port=1883)
	client.loop_forever()
    

if __name__ == '__main__':
	main()

sys.exit(0)