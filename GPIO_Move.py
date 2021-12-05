from mcpi.minecraft import Minecraft
from gpiozero import Button

mc = Minecraft.create()
pos = mc.player.getPos()
#rot = mc.player.getRotation()

direction = "up"

up = Button(6)
down = Button(22)
left = Button(17)
right = Button(27)

upDir = [[1, 0, 0], [-1, 0, 0], [0, 0, -1], [0, 0, 1]]
downDir = [[-1, 0, 0], [1, 0, 0], [0, 0, 1], [0, 0, -1]]
leftDir = [[0, 0, 1], [0, 0, -1], [1, 0, 0], [-1, 0, 0]]
rightDir = [[0, 0, -1], [0, 0, 1], [-1, 0, 0], [1, 0, 0]]
moveDir = upDir

while True:
    pos = mc.player.getPos()
    rot = mc.player.getRotation()
    if up.is_pressed:
        mc.player.setPos(pos.x + moveDir[0][0], pos.y + moveDir[0][1], pos.z + moveDir[0][2])
        up.wait_for_release()
    elif down.is_pressed:
        mc.player.setPos(pos.x + moveDir[1][0], pos.y + moveDir[1][1], pos.z + moveDir[1][2])
        down.wait_for_release()
    elif left.is_pressed:
        mc.player.setPos(pos.x + moveDir[2][0], pos.y + moveDir[2][1], pos.z + moveDir[2][2])
        left.wait_for_release()
    elif right.is_pressed:
        mc.player.setPos(pos.x + moveDir[3][0], pos.y + moveDir[3][1], pos.z + moveDir[3][2])
        right.wait_for_release()

    if rot > -45 and rot < 45:
        moveDir = upDir
    elif rot > 135 or rot < -135:
        moveDir = downDir
    elif rot > -135 and rot < -45:
        moveDir = leftDir
    elif rot > 45 and rot < -135:
        moveDir = rightDir

        

    
