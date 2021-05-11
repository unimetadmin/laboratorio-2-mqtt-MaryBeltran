import paho.mqtt.client
import ssl
import sys
import json
import random
import time
import numpy as np
import datetime

def on_connect(client, userdata, flags, rc):
    print("Se ha conectado el Publicador de Contador de Personas (que pasan por la Sala) con el código de resultado: "+str(rc))

def main():
	cliente = paho.mqtt.client.Client("PublicadorPersonasSala", False) #Para guardar la sesión
	cliente.qos = 0 #0: Mandar mensajes constantemente (sin importar si se escuchan o no) / 1: Manda mensajes y espera el acuse de recibo, si no recibe vuelve a enviar sucesivamente (puede llegar a enviar la misma info repetidas veces) / 2: Como el 1 pero se asegura que lo envíe una sola vez
	cliente.connect(host='localhost')
	minutoBase = datetime.datetime.now().replace(second=0, microsecond=0)

	while(True):

		persona = int(np.random.uniform(0, 10))
		payload = {
			"Minuto": str(minutoBase),
			"Personas en la Sala": str(persona)
		}
		print(payload)
		if persona > 5: 
			mensaje = { 
				"Minuto": str(minutoBase),				
				"Mensajito": ("COVID-19 ALERT: No pueden estar mas de 5 personas reunidas en la sala")
			}
			cliente.publish('Casa/Sala/contar_personas',json.dumps(mensaje),qos=0)
			print(mensaje)
		cliente.publish('Casa/Sala/contar_personas',json.dumps(payload),qos=0)				

		minutoBase += datetime.timedelta(minutes=1)
		time.sleep(1)

if __name__ == '__main__':
	main()
	sys.exit(0)