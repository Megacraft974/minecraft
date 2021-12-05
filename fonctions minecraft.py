from mcpi.minecraft import Minecraft
from time import sleep
from random import randint

mc = Minecraft.create()

def Chat(texte):
    mc.postToChat(texte)
    
def Sur_quel_bloc():
    while True:
        x,y,z = mc.player.getTilePos()
        block = mc.getBlock(x,y-1,z)
        print(block)
        sleep(0.1)

def Teleporter(posx,posy,posz):
    mc.player.setPos(posx, posy, posz)

def Poser_bloc(x,y,z,bloc=1):
    mc.setBlock(x, y, z, 11, 1)

def Piece(large,haut,x,y,z):
    stone = 1
    air = 0
    mc.setBlocks(x+1, y-1, z, x+large, y+haut, z, stone)
    mc.setBlocks(x+large, y-1, z, x+large, y+haut, z+large, stone)
    mc.setBlocks(x, y-1, z+1, x, y+haut, z+large, stone)
    mc.setBlocks(x+large, y-1, z+large, x, y+haut, z, stone)
    mc.setBlocks(x, y-1, z, x+large, y, z+large, stone)
    mc.setBlocks(x+1, y, z+1, x+large-1, y+haut-1, z+large-1, air)

def Mur(large,haut,long,x,y,z):
    mc.setBlocks(x,y,z,x+large,y+haut,z+long)
def Chateau():
    
    air = 0
    stone = 1
    x = 0
    y = 30
    z = 0
    
    Piece(15,30,x,y,z)

def Zombie():
    vert =35
    bleu =26
