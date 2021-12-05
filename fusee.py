from mcpi.minecraft import Minecraft
from time import sleep
from random import randint
import math
from fusee2 import*

mc = Minecraft.create()

def findPointOnCircle(cx, cy, radius, angle):
    x = cx + math.sin(math.radians(angle)) * radius
    y = cy + math.cos(math.radians(angle)) * radius
    return((int(x + 0.5),int(y + 0.5)))

def fusee2():
    rocketPos = mc.player.getTilePos()
    rocketPos.x += 5
    rocketPos.y = mc.getHeight(rocketPos.x, rocketPos.z) - 1
    launchpad = LaunchPad(mc, rocketPos)
    rocket = Rocket(mc, rocketPos)
    try:
        launch = False
        while not launch:
            for hit in mc.events.pollBlockHits():
                shapeblockhit = launchpad.getShapeBlock(hit.pos.x, hit.pos.y, hit.pos.z)
                if shapeblockhit != None:
                    if shapeblockhit.tag == "launch":
                        launch = True
        for count in range(3, 0, -1):
            mc.postToChat(str(count))
            sleep(1)
        mc.postToChat("Mise a feu")
        #teleporte()
        for up in range(0, 15):
            rocket.moveBy(0, 1, 0)
        pitch = 0
        for up in range(0, 75):
            z, y = findPointOnCircle(0, 0, 1, pitch)
            rocket.rotate(0, pitch, 0)
            rocket.moveBy(0, y, z)
            if pitch < 60:
                pitch += 3
    finally:
        rocket.clear()
        launchpad.clear()
        

def fusee():
    mc.setBlocks(x,y,z,x+2,y+5,z+2,35,7)#Tronc de la fusee
    
    mc.setBlocks(x+1,y+1,z+1,x+1,y+4,z+1,0)#L'air à l'interieur
    
    mc.setBlocks(x+1,y,z-1,x+1,y+4,z-1,35,0)#L'arrondi
    mc.setBlocks(x-1,y,z+1,x-1,y+4,z+1,35,0)#Idem
    mc.setBlocks(x+3,y,z+1,x+3,y+4,z+1,35,0)#Idem
    mc.setBlocks(x+1,y,z+3,x+1,y+4,z+3,35,0)#Idem
    
    mc.setBlock(x+1,y+6,z+1,35,0)#Le bout pointu
    
    mc.setBlocks(x+1,y,z-2,x+1,y+1,z-2,35,7)#Les ailerons
    mc.setBlocks(x-2,y,z+1,x-2,y+1,z+1,35,7)#Idem
    mc.setBlocks(x+4,y,z+1,x+4,y+1,z+1,35,7)#Idem
    mc.setBlocks(x+1,y,z+4,x+1,y+1,z+4,35,7)#Idem

def porte(bloc):
    mc.setBlocks(x-1,y+3,z,x-3,y+4,z,bloc)

def piece():
    mc.setBlocks(x-5,y-40,z-5,x+5,y-35,z+5,1)
    mc.setBlocks(x-4,y-39,z-4,x+4,y-34,z+4,0)
    mc.setBlocks(x-5,y-37,z-4,x+4,y-37,z+4,89)
    mc.setBlocks(x-4,y-39,z-4,x-1,y-35,z-4,0)
    mc.setBlock(x-4,y-38,z-4,1)
    mc.setBlock(x-3,y-39,z-4,1)
    

def teleporte():
    x2,y2,z2 = mc.player.getTilePos()
    while not x2-x==1 and z2-z==1:
        x2,y2,z2 = mc.player.getTilePos()
        sleep(1)
    porte(1)
    sleep(1)
    piece()
    mc.player.setPos(x, y-39, z)

def cratere():
    x2=randint(-50,50)
    y2=-62
    z2=randint(-50,50)
    mc.setBlocks(x2-1,y2-1,z2-1,x2+2,y2-1,z2+2,13)
    mc.setBlocks(x2-2,y2-1,z2+1,x2+3,y2-1,z2+2,13)
    mc.setBlocks(x2+1,y2-1,z2-2,x2+2,y2-1,z2+3,13)
    mc.setBlocks(x2,y2,z2,x2+3,y2,z2+1,13)
    mc.setBlocks(x2+1,y2,z2-1,x2+2,y2,z2+2,13)
    mc.setBlocks(x2+1,y2,z2,x2+2,y2,z2+1,0)
    
def lune():
    mc.setBlocks(-50,-64,-50,50,-60,50,0)
    mc.setBlocks(-50,-64,-50,50,-64,50,82)
    for boucle in range(200):
        cratere()
    mc.player.setPos(0, -62, 0)
def run():
    global x,y,z
    x,y,z = mc.player.getTilePos()
    x=x+5
    z=z-1
    mc.setBlocks(x+5,y,z+5,x-10,y,z-4,1)
    fusee()
    #fusee2()
    #sleep(10)
    #lune()

run()
