from gpiozero import Motor
from time import sleep

left_motor = Motor(forward=17, backward=18, enable=12)
right_motor = Motor(forward=27, backward=22, enable=13)

speed = 1
duration = 2

print("BEGINNING MOTOR MOVEMENT TEST")

try:
    # FORWARD
    print(f"Moving forward at {speed*100}% speed for {duration} seconds...")
    left_motor.forward(speed=speed)
    right_motor.forward(speed=speed)
    sleep(duration)

    # BACKWARD
    print(f"Moving backward at {speed*100}% speed for {duration} seconds...")
    left_motor.backward(speed=speed)
    right_motor.backward(speed=speed)
    sleep(duration)

    # RIGHT
    print(f"Turning right for {duration} seconds...")
    left_motor.forward(speed=speed)
    right_motor.backward(speed=speed)
    sleep(duration)

    # 4. LEFT
    print(f"Turning left for {duration} seconds...")
    left_motor.backward(speed=speed)
    right_motor.forward(speed=speed)
    sleep(duration)

    # 5. STOP
    print("Stopping motors.")
    left_motor.stop()
    right_motor.stop()
    print("Test finished.")

except KeyboardInterrupt:
    print("Stopping motors.")
    left_motor.stop()
    right_motor.stop()