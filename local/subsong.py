#####################################################
# Step 0 : Import the libraries
####################################################
import paho.mqtt.client as mqtt
from playsound import playsound

# variables
start_engine = False
accelerate = False
nb_start = 0
# MQTT broker
BROKER = "192.168.0.109"
# create a client
CLIENT = mqtt.Client("Pc ilyes")
# connect to the broker
CLIENT.connect(BROKER)

# variables to contol the sound playing
start_engine = True
accelerate = True
missile = True
# playsound("acceleration.mp3")

CLIENT.subscribe("play_sound")
CLIENT.loop_start()

def on_message(client, userdata, message):
    global start_engine, accelerate, missile
    print("received message: " ,str(message.payload.decode("utf-8")))
    msg = str(message.payload.decode("utf-8"))
    if msg == "start_engine":
        playsound("start_engine.mp3")
    elif msg == "accelerate":
        playsound("acceleration.mp3")
    elif msg == "missile":
        playsound("missile.mp3")
    elif msg == "sui":
        playsound("sui.mp3")
    elif msg == "disco":
        playsound("disco.mp3")
    else:
        # reset the variables
        start_engine = False
        accelerate = False
        missile = False


while True:
    CLIENT.on_message = on_message
