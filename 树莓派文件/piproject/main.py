# !/usr/bin/python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO # 导入Rpi.GPIO库函数命名为GPIO
import time # 导入计时time函数


def main():
    # GPIO port
    switchIn = 36
    switchOut = 18
    flowSensor = 12
    light = 32
    
    # time(s)
    inTime = 18
    waitTime = 10
    outTime = 32
    nextTime = 5

    GPIO.setmode(GPIO.BOARD) #将GPIO编程方式设置为BOARD模式
    GPIO.setup(switchIn, GPIO.OUT) #设置物理引脚负责输出电压
    GPIO.setup(switchOut, GPIO.OUT)
    GPIO.setup(flowSensor, GPIO.IN)
    GPIO.setup(light, GPIO.OUT)
    
    while 1:
        try:
            # 充气过程
            print("start inflation, {} s".format(inTime))
            GPIO.output(switchIn, GPIO.HIGH) # switchIn输出高电平
            GPIO.output(switchOut, GPIO.LOW)
            GPIO.output(light, GPIO.LOW)
            time.sleep(inTime)
            GPIO.output(switchIn, GPIO.LOW) # switchIn输出低电平
            print("waiting for {} s".format(waitTime))
            time.sleep(waitTime)
            
            # 放气过程
            print("start deflation, {} s".format(outTime))
            GPIO.output(switchOut, GPIO.HIGH)
            start = time.time()
            while True:
                flow = GPIO.input(flowSensor)
                if flow:
                    GPIO.output(light, GPIO.HIGH)
                    while True:
                        current = time.time()
                        if (current - start > outTime):
                            break
                current = time.time()
                if (current - start > outTime):
                    print("waiting for {} s".format(nextTime))
                    time.sleep(nextTime)
                    break
        except (KeyboardInterrupt, SystemExit):
            GPIO.cleanup()
            break

if __name__ == '__main__':
    main()

