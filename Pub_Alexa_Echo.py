import paho.mqtt.client
import sys
import json
import time
import numpy as np
import datetime
import requests

def on_connect(client, userdata, flags, rc):
    print("Se ha conectado el Publicador de la Alexa EchoDot con el código de resultado: "+str(rc))


def main():
    cliente = paho.mqtt.client.Client("PublicadorTemperaturaCaracas", False) #Para guardar la sesión
    minutoBase = datetime.datetime.now().replace(second=0, microsecond=0)
    cliente.qos = 0 #0: Mandar mensajes constantemente (sin importar si se escuchan o no) / 1: Manda mensajes y espera el acuse de recibo, si no recibe vuelve a enviar sucesivamente (puede llegar a enviar la misma info repetidas veces) / 2: Como el 1 pero se asegura que lo envíe una sola vez
    cliente.connect(host='localhost')
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Caracas&APPID=e4aacb507ab6036d28b1254cd2a63745')
    respuesta = r.json()
    TemperaturaBase = float((respuesta['main']['temp']))

    while(True):

        CambioTemperatura = float(np.random.uniform(-0.5, 0.5)) #Para que varíe segun indicación del profe
        payload = {
                "Minuto": str(minutoBase),
                "TemperaturaCaracas": round(TemperaturaBase + CambioTemperatura, 2)
            }    
        print(payload)
        cliente.publish('Casa/Sala/alexa_echo',json.dumps(payload),qos=0)
        
        minutoBase += datetime.timedelta(minutes=1)
        time.sleep(5) 

if __name__ == '__main__':
    main()
    sys.exit(0)