from sense_hat import SenseHat
from mcpi.minecraft import Minecraft
from minecraftcolours import*

sense = SenseHat()
mc = Minecraft.create()

known_blocks = {}

def get_blocks():
    global known_blocks

    x, y, z = mc.player.getTilePos()
    y -= 1

    blocks = []
    for dz in range(z-3, z+5):
        for dx in range(x-3, x+5):
            b = (dx, y, dz)
            if b in known_blocks:
                block = known_blocks[b]
            else:
                block = mc.getBlock(dx, y, dz)
                known_blocks[b] = block
            blocks.append(block)

    return blocks

def lookup_colour(block):
    if block in colours:
        return colours[block]
    else:
        return white

def map_blocks_to_colours(blocks):
    return [lookup_colour(block) for block in blocks]

player_pos = 27

while True:
    
    blocks = get_blocks()
    pixels = map_blocks_to_colours(blocks)
    pixels[player_pos] = black  # denote player as black pixel
    sense.set_pixels(pixels)
