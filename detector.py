import RPi.GPIO as GPIO
import boto3
import datetime, DbHandler, json
from time import sleep
from threading import Thread
from picamera import PiCamera

camera = PiCamera()
camera.rotation = 180
def uploadImage(time):
    camera.resolution = (1920, 1080)
    camera.start_preview()

    sleep(3)

    camera.capture('/home/pi/camera/{}.jpg'.format(time))
    camera.stop_preview()

    s3 = boto3.client('s3')

    s3.upload_file("/home/pi/camera/{}.jpg".format(time), "iot-images-s3642455", "{}.jpg".format(time))
    return time


GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.IN)  # Read output from PIR motion sensor on Pin 13

while True:
    i = GPIO.input(13)
    if i == 0:  # When output from motion sensor is LOW
        print("No detection", i)

    elif i == 1:  # When output from motion sensor is HIGH
        time = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        t1 = Thread(target=uploadImage, args=(time,))
        data = { "deviceId" : "0",
                 "deviceName" : "Raspberry Pi",
                 "time" : time,
                 "photoUrl" : "https://s3.amazonaws.com/iot-images-s3642455/{}.jpg".format(time)
                 }
        data = json.dumps(data)
        t2 = Thread(target=DbHandler.put, args=(data,))
        t1.start()
        t2.start()
        print("Movement detected, image is being uploaded", i)
        sleep(20)
        t1.join()
        t2.join()
    sleep(1)

