from gpiozero import PWMLED
from time import sleep
from gpiozero import CPUTemperature

measureDelay = 15
thisPin = PWMLED(14)

while True:
    currentCpuTemp = CPUTemperature().temperature
    pwmPercentage = ((((currentCpuTemp-float(30.0))/5)*0.1) + 0.1)
    thisPin.value = pwmPercentage
    print("Current CPU Temperature is %.1f"%(currentCpuTemp))
    print("PWM percentage is %.3f"%(pwmPercentage))
    sleep(measureDelay)
