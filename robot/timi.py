#####################################################
# Step 0 : Import the libraries
####################################################
import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
import uuid
import RPi.GPIO as GPIO
import move
import LED
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import os
# lancer la manette de ps
from pydualsense import pydualsense
import move
from tqdm import tqdm
import InfraLib

IR_RECEIVER = 22

shot_topic = "tanks/"+ str(uuid.getnode()) +"/shots"
shot_in_topic = shot_topic + "/in"
shot_out_topic = shot_topic + "/out"

def get_shooting(x):
    CLIENT.publish(shot_in_topic, "SHOT_BY "+ str(InfraLib.getSignal(IR_RECEIVER, CLIENT)))

# Initialisation de la manette PS5
dualsense = pydualsense()
dualsense.init()

# Vérifie si la manette est connectée
if dualsense.device:
    print('Manette PS5 connectée.')
else:
    print('Manette PS5 non détectée. Vérifiez la connexion.')
    dualsense.close()
    exit()

#####################################################################
# Step 1 : Setting up Global variables to store data from the server
#####################################################################
color = ""
qr_code = ""

#####################################################################
# Methods Process the data
#####################################################################

# message received from the server
def on_message(client, userdata, message):
    global color, qr_code
    received_message = str(message.payload.decode("utf-8"))
    print("Received message: ", received_message)
    if received_message.startswith("TEAM"):
        color = received_message.split()[1]
        print("Received color:", color)

    if received_message.startswith("QR_CODE"):
        qr_code = received_message.split()[1]
        print("Received QR CODE:", qr_code)

#####################################################################
# CREDENTIALS
#####################################################################
# get the MAC address of the robot
TANK_ID = uuid.getnode()
# MQTT broker
BROKER = "192.168.0.109"
# create a client
CLIENT = mqtt.Client("TIMI")
# connect to the broker
CLIENT.connect(BROKER)

#####################################################################
# Step 1 : Initialisation
#####################################################################

CLIENT.subscribe("tanks/"+ str(TANK_ID) +"/init")
CLIENT.subscribe("tanks/"+ str(TANK_ID) +"/flag")
CLIENT.subscribe("tanks/"+ str(TANK_ID) +"/shots")
CLIENT.subscribe("tanks/"+ str(TANK_ID) +"/shots/out")
CLIENT.subscribe("tanks/"+ str(TANK_ID) +"/shots/in")
CLIENT.subscribe("tanks/"+ str(TANK_ID) +"/shots/in")
CLIENT.publish("tanks/"+ str(TANK_ID) +"/qr_code")



CLIENT.loop_start()
CLIENT.on_message = on_message
    
CLIENT.publish("init", "INIT "+ str(TANK_ID))
# CLIENT.on_message = on_message

time.sleep(1)

# setup the LED of out team

led = LED.LED()
if color == "RED":
    led.colorWipe(255, 0, 0)  # red

if color == "BLUE":
    led.colorWipe(0, 0, 255)  # blue

#####################################################################
# Step 2 : Flag Area with GPIO Interrupts
#####################################################################

# Variables pour le suivi de ligne
line_pin_middle = 16

# Configuration des GPIO
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_middle, GPIO.IN)

# Fonction callback pour les interruptions GPIO
def zone_callback(channel):
    if GPIO.input(line_pin_middle) == 0:  # Si le capteur détecte la zone
        CLIENT.publish("tanks/"+ str(TANK_ID) +"/flag", "ENTER_FLAG_AREA")
        print("Entered Zone")
    else:
        CLIENT.publish("tanks/"+ str(TANK_ID) +"/flag", "EXIT_FLAG_AREA")
        print("Exited Zone")

setup()  # Configuration des GPIO pour le suivi de ligne
GPIO.setup(IR_RECEIVER, GPIO.IN)
# Configuration de l'interruption GPIO
GPIO.add_event_detect(line_pin_middle, GPIO.BOTH, callback=zone_callback)
GPIO.add_event_detect(IR_RECEIVER, GPIO.FALLING, callback=get_shooting)



try:
    while True:
    # a = input("Press a to start engine, b to accelerate \n")
    # if a == "a":
    #     CLIENT.publish("play_sound", "start_engine")
        
    # else:
    #     CLIENT.publish("play_sound", "accelerate")

        # jeu de données

        if dualsense.state.ps:
            print("PS")
            # start engine
            CLIENT.publish("play_sound", "start_engine")


        if dualsense.state.cross:
            print("Cross")
            # capturer une image

            def decodeDisplay(image):

                barcodes = pyzbar.decode(image)

                for barcode in barcodes:
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type

                    text = "{} ({})".format(barcodeData, barcodeType)
                    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
                    CLIENT.publish("tanks/"+ str(TANK_ID) +"/qr_code", "QR_CODE "+ barcodeData)

                return image

            def take_picture():

                # prendre une photo avec Raspberry Pi Camera en lancant la commande suivante
                # raspistill -o image.jpg

                # code :
                commande = "libcamera-still -o image.jpg"
                os.system(commande)

                # lire l'image
                image = cv2.imread('image.jpg')

                return image


            def scan_qr_code(image):

                # decoder et afficher le QR code
                image = decodeDisplay(image)

            def main():

                # prendre une photo
                image = take_picture()

                # scanner le QR code
                scan_qr_code(image)

            main()

            CLIENT.publish("play_sound", "sui")
        
        if dualsense.state.circle:
            print("Circle")
            CLIENT.publish("play_sound", "disco")
            # make fun color and back to the original color
            led.colorWipe(255, 0, 0)  # red
            time.sleep(0.01)
            led.colorWipe(0, 0, 255)  # blue
            time.sleep(0.01)
            led.colorWipe(0, 255, 0)  # green
            time.sleep(0.01)
            led.colorWipe(255, 255, 255)  # white
            time.sleep(0.01)
            led.colorWipe(0, 0, 0)  # off
            time.sleep(0.01)
            led.colorWipe(255, 255, 0)  # yellow
            time.sleep(0.01)
            led.colorWipe(0, 255, 255)  # cyan
            time.sleep(0.01)
            led.colorWipe(255, 0, 255)  # magenta
            time.sleep(0.01)

            # back to the original color
            if color == "RED":
                led.colorWipe(255, 0, 0)
            
            else:
                led.colorWipe(0, 0, 255)

        if dualsense.state.square:
            print("Square")
            InfraLib.IRBlast(uuid.getnode(), "LASER")
            CLIENT.publish("play_sound", "missile")


        if dualsense.state.triangle:
            print("Triangle")
            CLIENT.publish("play_sound", "stop")

        if dualsense.state.L1:
            print("L1")
            
        
        if dualsense.state.R1:
            print("R1")
            CLIENT.publish("play_sound", "accelerate")

        if dualsense.state.L2:
            print("L2")
            speed_set = 20

        if dualsense.state.R2:
            print("R2")
            speed_set = 100

        if dualsense.state.DpadUp:
            print("DpadUp")
            # move forward
            speed_set = 100
            move.setup()
            if dualsense.state.DpadLeft:
                move.move(speed_set, 'forward', 'left', 1)

            elif dualsense.state.DpadRight:
                move.move(speed_set, 'forward', 'right', 1)

            else:
                move.move(speed_set, 'forward', 'no', 1)
            time.sleep(1.3)
            move.motorStop()
            move.destroy()

        if dualsense.state.DpadDown:
            print("DpadDown")
            # move backward
            speed_set = 100

            if dualsense.state.R2:
                speed_set = 100

            if dualsense.state.L2:
                speed_set = 20

            
            move.setup()
            if dualsense.state.DpadLeft:
                move.move(speed_set, 'backward', 'left', 1)

            elif dualsense.state.DpadRight:
                move.move(speed_set, 'backward', 'right', 1)

            else:
                move.move(speed_set, 'backward', 'no', 1)
                
            time.sleep(1.3)
            move.motorStop()
            move.destroy()

        

        if dualsense.state.share:
            print("Share")

        if dualsense.state.options:
            print("Options")

        # if dualsense.state.LX > 0:
        #     print("LX > 0")
        
        # if dualsense.state.LY > 0:
        #     print("LY > 0")

        # if dualsense.state.RX > 0:
        #     print("RX > 0")

        # if dualsense.state.RY > 0:
        #     print("RY > 0")


        time.sleep(0.1) # Délai pour limiter la fréquence des mises à jour

except KeyboardInterrupt:
    print('Arrêt du script.')

finally:
    dualsense.close()


# finally:
#     GPIO.cleanup()  # Nettoyage des GPIO à la fin du programme
