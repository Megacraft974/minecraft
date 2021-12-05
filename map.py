from mcpi.minecraft import Minecraft
from random import randint

mc = Minecraft.create()

def grotte():
    def forme(x,y,z):
        mc.setBlocks(x,y-2,z,x+3,y+2,z,0)
        mc.setBlocks(x-1,y-1,z,x+4,y+1,z,0)
    for i in range(0,randint(1000,10000)):
        x = randint(-168,96)
        y = randint(-63,6)
        z = randint(-168,96)
        forme(x,y,z)
        for o in range(100,1000):
            x = x + randint(-2,2)
            y = y + randint(-2,2)
            z = z + randint(-2,2)
            forme(x,y,z)
    
def superplat():
    x = 200
    y = 0
    z = 200
    while x > -200:
        while z > -200:
            while y < 200:
                
