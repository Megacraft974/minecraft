from mcpi import minecraft
from picamera import PiCamera
from time import sleep

def prendre_la_photo():
    with PiCamera() as camera:
        camera.start_preview()
        sleep(2)
        camera.capture('/home/pi/selfie.jpg')

mc = minecraft.Minecraft.create()
mc.postToChat("Trouver le photomaton.")
while True:
    x, y, z, =mc.player.getPos()
    sleep(3)
    if x == 82.7 and y==3.0 and z==-130.5:
        mc.postToChat("Tu es dans le photomaton!")
        sleep(1)
        mc.postToChat("Souriez!")
        sleep(1)
        prendre_la_photo()
        mc.postToChat("Consultez votre photo.")
        break
