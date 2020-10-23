# @Auther pb-dn@outlook.com
# Sep 12 2020 v1.0
# Copyright WTFPL
# README
# Apply for miio philips_bulb
# This 
# Register the light base on the describtion down there
# (Optional) Modify the config variable to fit the needs


# TODO keep in json
# Format [[IP:token]..]
lights = [['192.168.0.1', 'aerd123gaeddfg31762491744c8d02cc'],
             ['192.168.0.1', '0e0d416a101bd1744c8d9dd0104dde'],
                ['192.168.0.1', '945d86a7761a02asgdg654e78f88']]

# Configuration 
# [[HHMM, Brightness(1-100), color_temperature(1-100)],..]
# Plz keep the initial item & the last
config = [[-1,1,1], [700,30,30], [730,60,50], [800,80,50], [1000,80,80], [1200,100,90], 
            [1400,80,80], [1600,80,70], [1800,60,60], [2000,40,40], [2200,30,30],[2400,1,1]]

from miio.philips_bulb import PhilipsBulb
import time

class Group:
    # Register Device{}
    def __init__(self):
        self.group = []
        for item in lights:
            print(item)
            object = PhilipsBulb(item[0], item[1])
            self.group.append(object)

    def do(self, function, level):
        # Using IoC ideology to execute methods
        result = []
        for object in self.group:
            # tryTimes = 0
            try:
                result.append(getattr(object, function)(level))
            except :
                result.append(getattr(object, function)(level))
        # return result

def main():
    p = 0
    # Get targetTime time and deltaTime
    # targetTime: nearest time that in config
    # deltaTime:  second to next config time
    while True:
        minute = time.localtime().tm_min
        hour = time.localtime().tm_hour
        while True:
            if (targetH:=config[p][0] // 100) > hour:
                targetM = config[p][0] % 100
                if targetM < minute:
                    deltaTime = ((targetH - time.localtime().tm_hour - 1)*60 + 60-minute + targetM)*60
                    break
                deltaTime = ((targetH - time.localtime().tm_hour)*60 + 60-minute + targetM)*60
                break
            elif (targetH:=config[p][0] // 100) == hour and (targetM:=config[p][0] % 100) >= minute:
                deltaTime = (targetM - minute)*60
                break
            else: p += 1
            if p == len(config):
                p = 0

        targetUTS = time.time() + deltaTime

        baseHour = config[p-1][0] // 100
        baseMinute = config[p-1][0] % 100
        if targetH > baseHour:
            deltaTime = ((targetH - baseHour)*60 + 60-baseMinute + targetM)*60      
        else : deltaTime = (targetM - baseMinute)*60

        deltaB = config[p][1] - config[p-1][1]
        deltaC = config[p][2] - config[p-1][2]

        # step by step to adjust light / temperature
        group = Group()
        oldB, oldC = 0,0
        while (uts:=time.time()) < targetUTS:
            setB = int(config[p-1][1] + deltaB*(1-(targetUTS - uts)/deltaTime))
            setC = int(config[p-1][2] + deltaC*(1-(targetUTS - uts)/deltaTime))
            if setB == oldB:
                pass
            else:
                oldB = setB
                group.do('set_brightness',setB)
            if setC == oldC:
                pass
            else:
                oldC = setC
                group.do('set_color_temperature',setC)
            time.sleep(120)

if __name__ == "__main__":
    main()