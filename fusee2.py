from fusee3 import MinecraftShape
from mcpi import block

class Rocket(MinecraftShape):
    def __init__(self, mc, pos, cleararea = True, makevisible = True):

        self.pos = pos
        self.mc = mc
        self.x = pos.x
        self.y = pos.y
        self.z = pos.z

        #init the MinecraftShape
        MinecraftShape.__init__(self, self.mc, self.pos, visible = False)

        #red wool fire!
        self.setBlock(0, 0, 0, 35, 14)
        #block wool wings
        self.setBlocks(-2, 1, 0, 2, 1, 0, 35, 15)
        self.setBlocks(0, 1, -2, 0, 1, 2, 35, 15)
        self.setBlocks(0, 2, -1, 0, 2, 1, 35, 15)
        self.setBlocks(-1, 2, 0, 1, 2, 0, 35, 15)
        #white steps on wings
        self.setBlock(-3, 1, 0, 156)
        self.setBlock(-2, 2, 0, 156)
        self.setBlock(0, 1, -3, 156, 2)
        self.setBlock(0, 2, -2, 156, 2)
        self.setBlock(3, 1, 0, 156, 1)
        self.setBlock(2, 2, 0, 156, 1)
        self.setBlock(0, 1, 3, 156, 3)
        self.setBlock(0, 2, 2, 156, 3)
        #white base
        self.setBlocks(1, 3, 0, -1, 3, 0, 155)
        self.setBlocks(0, 3, 1, 0, 3, -1, 155)
        #black band
        self.setBlocks(1, 4, 0, -1, 4, 0, 35, 15)
        self.setBlocks(0, 4, 1, 0, 4, -1, 35, 15)
        #main body
        self.setBlocks(0, 5, -1, 0, 10, -1, 155)
        self.setBlocks(-1, 10, 0, -1, 5, 0, 155)
        self.setBlocks(0, 5, 1, 0, 10, 1, 155)
        self.setBlocks(1, 10, 0, 1, 5, 0, 155)
        #white steps at the top
        self.setBlock(1, 11, 0, 156, 1)
        self.setBlock(0, 11, 1, 156, 3)
        self.setBlock(-1, 11, 0, 156)
        self.setBlock(0, 11, -1, 156, 2)
        #block on the top
        self.setBlock(0, 12, 0, 155)

        if cleararea:
            self.clearArea()

        #make the model visible
        if makevisible:
            self.draw()

    def clearArea(self):
        """
        Clears an area big enough to put the model in
        """
        self.mc.setBlocks(
            self.pos.x - 3,
            self.pos.y,
            self.pos.z - 3,
            self.pos.x + 3,
            self.pos.y + 12,
            self.pos.z + 3,
            block.AIR.id)

    def launch(self, height):
        for up in range(0, height):
            self.moveBy(0, 1, 0)

class LaunchPad(MinecraftShape):
    """
    A model of a launch pad which the rocket can sit on
    """
    def __init__(self, mc, pos, cleararea = True, makevisible = True):

        self.pos = pos
        self.mc = mc

        #init the MinecraftShape
        MinecraftShape.__init__(self, self.mc, self.pos, visible = False)

        #base
        self.setBlocks(-4, 0, -3, 4, 0, 3, 1, tag = "launch")
        self.setBlocks(3, 0, -4, -3, 0, -4, 1, tag = "launch")
        self.setBlocks(-3, 0, 4, 3, 0, 4, 1, tag = "launch")

        #steel tower
        self.setBlocks(4, 1, 2, 4, 10, 2, 42)
        self.setBlocks(4, 10, 2, 4, 10, -2, 42)
        self.setBlocks(4, 1, -2, 4, 10, -2, 42)

        #glass lift and tunnel
        self.setBlocks(4, 9, 0, 4, 1, 0, 20)
        self.setBlocks(3, 10, 0, 2, 10, 0, 20)

        if cleararea:
            self.clearArea()

        #make the model visible
        if makevisible:
            self.draw()

    def clearArea(self):
        """
        Clears an area big enough to put the model in
        """
        self.mc.setBlocks(
            self.pos.x - 4,
            self.pos.y,
            self.pos.z - 4,
            self.pos.x + 4,
            self.pos.y + 10,
            self.pos.z + 4,
            block.AIR.id)
