import paho.mqtt.client
import sys
import json
import time
import numpy as np
import datetime


def on_connect(client, userdata, flags, rc):
    print("Se ha conectado el Publicador de Temperatura Olla con el código de resultado: "+str(rc))


def main():
	cliente = paho.mqtt.client.Client("PublicadorOlla", False) #Para guardar la sesión
	cliente.qos = 0 #0: Mandar mensajes constantemente (sin importar si se escuchan o no) / 1: Manda mensajes y espera el acuse de recibo, si no recibe vuelve a enviar sucesivamente (puede llegar a enviar la misma info repetidas veces) / 2: Como el 1 pero se asegura que lo envíe una sola vez
	cliente.connect(host='localhost')
	segundoBase= datetime.datetime.now().replace(microsecond=0)
	
	while(True):

		temperatura = int(np.random.uniform(0, 150))
		
		payload = {
			"Segundo": str(segundoBase),
			"TemperaturaOlla": str(temperatura)
		}
		print(payload)
		if temperatura >= 100: 
			mensaje = { 
				"Segundo": str(segundoBase),
				"Mensajito": ("El agua ya hirvio")
			}
			cliente.publish('Casa/Cocina/temperatura_olla',json.dumps(mensaje),qos=0)
			print(mensaje)
		cliente.publish('Casa/Cocina/temperatura_olla',json.dumps(payload),qos=0)				
		segundoBase += datetime.timedelta(seconds=1)
		time.sleep(1)

if __name__ == '__main__':
	main()
	sys.exit(0)


