import paho.mqtt.client
import sys
import json
import time
import numpy as np
import datetime

def on_connect(client, userdata, flags, rc):
    print("Se ha conectado el Publicador de Temperatura Nevera con el código de resultado: "+str(rc))

def main():
	
    cliente = paho.mqtt.client.Client("PublicadorNevera", False) #Para guardar la sesión
	
    cliente.qos = 0 #0: Mandar mensajes constantemente (sin importar si se escuchan o no) / 1: Manda mensajes y espera el acuse de recibo, si no recibe vuelve a enviar sucesivamente (puede llegar a enviar la misma info repetidas veces) / 2: Como el 1 pero se asegura que lo envíe una sola vez
    cliente.connect(host='localhost')
    minutoBase= datetime.datetime.now().replace(microsecond=0, second=0)
    desviacion = 2
    media = 10
    Cont = 0
    
    
    while (True):
        Cont += 1
        temperatura = np.random.normal(media, desviacion)
        payload = {
		    "Minuto": str(minutoBase),
		    "TemperaturaNevera": str(temperatura)
		}
        
        print(payload)
	    
        cliente.publish('Casa/Cocina/temperatura_nevera',json.dumps(payload),qos=0)				
		
        if Cont == 2:
            hielo = int(np.random.uniform(0, 10))
            hielito = {
                "Minuto": str(minutoBase),
                "Hielo": str(hielo)
		}
            Cont = 0
            print(hielito)
            cliente.publish('Casa/Cocina/temperatura_nevera',json.dumps(hielito),qos=0)
        
        minutoBase += datetime.timedelta(minutes=5)
        time.sleep(1) 

if __name__ == '__main__':  
    
    main()
    sys.exit(0)

