import paho.mqtt.client
import sys
import json
import time
import numpy as np
import datetime

def on_connect(client, userdata, flags, rc):
    print("Se ha conectado el Publicador de Tanque Nivel con el código de resultado: "+str(rc))

def main():
    cliente = paho.mqtt.client.Client("PublicadorTabque", False) #Para guardar la sesión
    cliente.qos = 0 #0: Mandar mensajes constantemente (sin importar si se escuchan o no) / 1: Manda mensajes y espera el acuse de recibo, si no recibe vuelve a enviar sucesivamente (puede llegar a enviar la misma info repetidas veces) / 2: Como el 1 pero se asegura que lo envíe una sola vez
    cliente.connect(host='localhost')
    minutoBase= datetime.datetime.now().replace(microsecond=0, second=0)
    TanqueAgua = 100
    desviacionSalida = 0.05 * TanqueAgua
    mediaSalida = 0.1 * TanqueAgua
    desviacionEntrada = 0.05 * TanqueAgua
    mediaEntrada = 0.2 * TanqueAgua
    Cont = 0
    
    while (True):
        Cont += 1
        SalidaAgua = np.random.normal(mediaSalida, desviacionSalida)
        TanqueAgua -= SalidaAgua
        if TanqueAgua < 0:
             TanqueAgua = 0
        payload = {
		    "Minuto": str(minutoBase),
		    "AguaEnTanque": str(TanqueAgua)
		}

        if Cont == 3:
            EntradaAgua = np.random.normal(mediaEntrada, desviacionEntrada)
            TanqueAgua += EntradaAgua
            print("Le sume agua en el momento ", str(minutoBase))
            if TanqueAgua > 100:
                TanqueAgua = 100
            payload = {
                "Minuto": str(minutoBase),
		        "AguaEnTanque": str(TanqueAgua)
		    }
            Cont = 0		

        if TanqueAgua == 0: 
            mensajeTvacio = { 
				"Minuto": str(minutoBase),
                "Mensajito": ("El Tanque se quedó vacío :(")
			}
            cliente.publish('Casa/Baño/nivel_tanque',json.dumps(mensajeTvacio),qos=0)
            print(mensajeTvacio)

        if TanqueAgua > 0 and TanqueAgua <= 50:
            mensaje = { 
                "Minuto": str(minutoBase),
				"Mensajito": ("El Tanque tiene la mitad o menos de su capacidad en agua")
			}
            cliente.publish('Casa/Baño/nivel_tanque',json.dumps(mensaje),qos=0)
            print(mensaje)

        
        print(payload)
        cliente.publish('Casa/Baño/nivel_tanque',json.dumps(payload),qos=0)
        
        minutoBase += datetime.timedelta(minutes=10)
        time.sleep(1) 

if __name__ == '__main__':
    main()
    sys.exit(0)

  

