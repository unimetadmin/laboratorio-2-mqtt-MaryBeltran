import sys
import paho.mqtt.client
import json
import psycopg2

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='Casa/Sala/#', qos=2)

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

        # Query SQL para crear una Nueva Tabla para SensorContadorPersonas
        if PayloadOriginal.get("Personas en la Sala"):
            cursor.execute ('''CREATE TABLE IF NOT EXISTS Cant_Personas_Sala
                            (ID SERIAL PRIMARY KEY NOT NULL,
                            Personas REAL NOT NULL,
                            Tiempo TIMESTAMP NOT NULL); ''')
            connection.commit()
            #print("La Tabla de Contador Personas se ha creado satisfactoriamente en PostgreSQL ")

            cursor.execute(''' INSERT INTO Cant_Personas_Sala (Tiempo, Personas)
                            VALUES (%(Tiempito)s, %(Personas)s);''',{'Tiempito': PayloadOriginal["Minuto"], 'Personas': PayloadOriginal["Personas en la Sala"] })
            connection.commit()


        if PayloadOriginal.get("Mensajito"):
            cursor.execute ('''CREATE TABLE IF NOT EXISTS Mensaje_AlertaCOVID
                            (ID SERIAL PRIMARY KEY NOT NULL,
                            Tiempo TIMESTAMP NOT NULL,
                            Mensajito TEXT NOT NULL); ''')
            connection.commit()
            #print("La Tabla Mensaje Alerta se ha creado satisfactoriamente en PostgreSQL ")

            cursor.execute(''' INSERT INTO Mensaje_AlertaCOVID (Tiempo, Mensajito)
                            VALUES (%(Tiempito)s, %(Mensajito)s);''',{'Tiempito': PayloadOriginal["Minuto"], 'Mensajito': PayloadOriginal["Mensajito"] })
            connection.commit()

        # Query SQL para crear una Nueva Tabla para AMAZON ALEXA
        if PayloadOriginal.get("TemperaturaCaracas"):
            cursor.execute ('''CREATE TABLE IF NOT EXISTS Temperatura_Ccs_AmazonAlexa
                            (ID SERIAL PRIMARY KEY NOT NULL,
                            TemperaturaCCS REAL NOT NULL,
                            Tiempo TIMESTAMP NOT NULL); ''')
            connection.commit()
            #print("La Tabla de TempCcsALEXA se ha creado satisfactoriamente en PostgreSQL ")

            cursor.execute(''' INSERT INTO Temperatura_Ccs_AmazonAlexa (Tiempo, TemperaturaCCS)
                            VALUES (%(Tiempito)s, %(TemperaturaCCS)s);''',{'Tiempito': PayloadOriginal["Minuto"], 'TemperaturaCCS': PayloadOriginal["TemperaturaCaracas"] })
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
	client = paho.mqtt.client.Client(client_id='MaryBeltran-SuscriptorSala', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='127.0.0.1', port=1883)
	client.loop_forever()
    

if __name__ == '__main__':
	main()

sys.exit(0)