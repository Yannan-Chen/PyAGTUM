
from zaber_motion import Units
from zaber_motion.ascii import Connection

import time

ZABER_PORT = "COM4"

class stages:

    ctspmm = 10078  # counts per mm
    zPosOffset = 0.5
    stowPosition = [0, 0, 75]
    pickupPosition = stowPosition

    def __init__(self, axis):

        self.port = Connection.open_serial_port(ZABER_PORT)   #com port identified using Zaber console, which was used to renumber axes too
        self.port.enable_alerts()
        device_list = self.port.detect_devices()
	
        self.device = [None] * axis
        self.drive = [None] * axis
	
        for n in range(axis):
            i = n + 1
            print(i)
            self.device[n] = 'device{0}'.format(i)
            self.drive[n] = 'drive{0}'.format(i)
            print(self.device[n])
            print(self.drive[n])
            self.device[n] = device_list[i-1] #.poll_until_idle(i)
            self.drive[n] = self.device[n].get_axis(1)
        self.is_parked = False

    def Disconnect(self):
        self.port.close()
        return

    def Connect(self):
        self.port.open()
        return

    def homeAll(self):
        self.moveZabs(75)
        self.moveYabs(0)
        self.moveXabs(0)
        self.drive[0].home()
        self.drive[1].home()
        self.drive[2].home()
        self.moveYabs(0)

    # Relative moves
    def moveAllRel(self,*argv):
        if len(argv) != len(self.drive):
            print("invalid number of arguments")
        else:
            self.moveZrel(argv[2])
            self.moveYrel(argv[1])
            self.moveXrel(argv[0])

    def moveXrel(self, move):
        pos = self.drive[0].get_position(Units.LENGTH_MILLIMETRES)
        if (move > 0 and pos + move > 300) or (move < 0 and pos + move < 0):
            print('Xpos = ' + str(pos) + ', Move = ' + str(move))
            print("Move out of range of 0 to 300")
        else:
            self.drive[0].move_relative(move, Units.LENGTH_MILLIMETRES)

    def moveYrel(self, move):
        pos = 75 - self.drive[1].get_position(Units.LENGTH_MILLIMETRES)
        if (move > 0 and pos + move > 75) or (move < 0 and pos + move < 0):
            print('Ypos = ' + str(pos) + ', Move = ' + str(move))
            print("Move out of range of 0 to 75")
        else:
            self.drive[1].move_relative(-move, Units.LENGTH_MILLIMETRES)

    def moveZrel(self, move):
        pos = 75 - self.drive[2].get_position(Units.LENGTH_MILLIMETRES)
        if (move > 0 and pos + move > 75) or (move < 0 and pos + move < 0):
            print('Zpos = ' + str(pos) + ', Move = ' + str(move))
            print("Move out of range of 0 to 75")
        else:
            self.drive[2].move_relative(-move , Units.LENGTH_MILLIMETRES)

    #Absolute moves
    def moveAllAbs(self,*argv):
        if len(argv) != len(self.drive):
            print("invalid number of arguments")
        else:
            self.moveZabs(argv[2])
            self.moveYabs(argv[1])
            self.moveXabs(argv[0])

    def moveXabs(self, move):
        if move > 300 or move < 0:
            print("Move out of range of 0 to 300")
        else:
            self.drive[0].move_absolute(move, Units.LENGTH_MILLIMETRES)

    def moveYabs(self, move):
        if move > 75 or move < 0:
            print("Move out of range of 0 to 75")
        else:
            self.drive[1].move_absolute(75 - move, Units.LENGTH_MILLIMETRES)

    def moveZabs(self, move):
        if move > 75 or move < 0:
            print("Move out of range of 0 to 75")
        else:
            self.drive[2].move_absolute(75 - move, Units.LENGTH_MILLIMETRES)


    def getAllPos(self):
        pos = [0, 0, 0]
        pos[0] = self.drive[0].get_position(Units.LENGTH_MILLIMETRES)
        pos[1] = 75 - self.drive[1].get_position(Units.LENGTH_MILLIMETRES)
        pos[2] = 75 - self.drive[2].get_position(Units.LENGTH_MILLIMETRES)

        return pos

    def moveToStow(self):
        self.moveZabs(75)  # position after homing
        self.moveYabs(0)  # position after homing
        self.moveXabs(0)  # positon after homing

        return

    def setPickupPositionNoOffset(self):
        self.pickupPosition = self.getAllPos()

        return self.pickupPosition

    def setPickupPositionWithOffset(self):
        self.pickupPosition = self.getAllPos()
        self.pickupPosition[2] += self.zPosOffset # move up in Z by offset to clear boat bottom

        return self.pickupPosition

    def moveToPickup(self):
        self.moveZabs(75) # move Z to top of stroke to avoid collisions
        self.moveYabs(0) # move Y to zero to avoid collisions

        self.moveXabs(self.pickupPosition[0]) # move to X pickup position
        self.moveYabs(self.pickupPosition[1]) # move to Y pickup position
        self.moveZabs(self.pickupPosition[2]) # finally drop down to Z pickup position

    def EStop(self):
        self.device[0].all_axes.stop()
        self.device[1].all_axes.stop()
        self.device[2].all_axes.stop()
        return

    def Park(self):
        self.device[0].all_axes.park()
        self.device[1].all_axes.park()
        self.device[2].all_axes.park()
        return

    def Unpark(self):
        self.device[0].all_axes.unpark()
        self.device[1].all_axes.unpark()
        self.device[2].all_axes.unpark()
        return

    def getParkState(self):
        if self.is_parked == True:
            action = "Unpark"
            color = "orange red"
            self.is_parked = False
        else:
            action = "Park"
            color = "pale green"
            self.is_parked = True
        return [action , color]




