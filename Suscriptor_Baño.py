import sys
import paho.mqtt.client
import json
import psycopg2

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='Casa/Baño/nivel_tanque', qos=2)

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
        
        # Query SQL para crear una Nueva Tabla
        if PayloadOriginal.get("AguaEnTanque"):
            cursor.execute ('''CREATE TABLE IF NOT EXISTS Cantidad_Agua_Tanque
                            (ID SERIAL PRIMARY KEY NOT NULL,
                            Agua REAL NOT NULL,
                            Tiempo TIMESTAMP NOT NULL); ''')
            connection.commit()
            #print("La Tabla se ha creado satisfactoriamente en PostgreSQL ")

            cursor.execute(''' INSERT INTO Cantidad_Agua_Tanque (Tiempo, Agua)
                            VALUES (%(Tiempito)s, %(Aguita)s);''',{'Tiempito': PayloadOriginal["Minuto"], 'Aguita': PayloadOriginal["AguaEnTanque"] })
            connection.commit()


        if PayloadOriginal.get("Mensajito"):
            cursor.execute ('''CREATE TABLE IF NOT EXISTS Mensaje_Agua_Tanque
                            (ID SERIAL PRIMARY KEY NOT NULL,
                            Tiempo TIMESTAMP NOT NULL,
                            Mensajito TEXT NOT NULL); ''')
            connection.commit()
            #print("La Tabla Mensajes se ha creado satisfactoriamente en PostgreSQL ")

            cursor.execute(''' INSERT INTO Mensaje_Agua_Tanque (Tiempo, Mensajito)
                            VALUES (%(Tiempito)s, %(Mensajes)s);''',{'Tiempito': PayloadOriginal["Minuto"], 'Mensajes': PayloadOriginal["Mensajito"] })
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
	client = paho.mqtt.client.Client(client_id='MaryBeltran-SuscriptorBano', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='127.0.0.1', port=1883)
	client.loop_forever()
    

if __name__ == '__main__':
	main()

sys.exit(0)