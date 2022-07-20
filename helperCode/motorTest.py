from machine import Pin, PWM
import utime as time

FREQUENCY = 200

leftPWM = PWM(Pin(32), FREQUENCY)

if __name__ == "__main__":
    speed = 0
    while True:
        speed += 10
        if speed > 500:
            speed = 0
        leftPWM.duty(int(speed))
        print("Speed: ", speed)
        time.sleep(0.5)