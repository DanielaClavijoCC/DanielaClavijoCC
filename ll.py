import network, time, urequests
from dht import DHT11
from machine import Pin, I2C, ADC
from utime import sleep

led_verde=Pin( 15,Pin.OUT)
led_rojo=Pin ( 2,Pin.OUT)
sensorG = ADC(Pin(39))


def conectaWifi(red, password):
     global miRed
     miRed = network.WLAN(network.STA_IF)     
     if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect('iPhone de Daniela', 'eeizviuh520s1')         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
     return True

if conectaWifi("iPhone de Daniela", "eeizviuh520s1"):
    print("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    
    url = "https://maker.ifttt.com/trigger/sensor_de_gas/with/key/ncflUg8bDGV7L1tgEBgSXvSCJsELPbftbzpwneKGqQC?"
 
while True:
    
    
    sleep(0.5)
    lectura = sensorG.read_u16()
    print( "Nivel de gas = {:02}".format(lectura))
   
    
    if lectura > 32000:
        respuesta = urequests.get(url+"&valor="+str(lectura))
        print (respuesta.status_code)
        respuesta.close ()
        led_verde.value(0)
        led_rojo.value(1)
    else:
        led_verde.value(1)
        led_rojo.value(0)
         
    
    print("Nivel de gas: ",lectura)
    sleep(0.25)