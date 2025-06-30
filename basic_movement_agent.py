from strands import Agent
from strands.models.openai import OpenAIModel
from strands import tool

from gpiozero import Motor
from time import sleep

left_motor = Motor(forward=17, backward=18, enable=12)
right_motor = Motor(forward=27, backward=22, enable=13)

@tool
def move_robot(direction: str, speed: float, time: float) -> str:
    """
    This tool will move the robot in a specific direction, at a 
    specified speed, for a specified amount of time.
    
    Args:
        direction: one of four possible strings:
            - "forward": moves the robot forward
            - "backward": moves the robot backward
            - "right": rotates the robot to the right in place
            - "left": rotates the robot to the left in place
        
        speed: a decimal value between 0 - 1, where 0 is no power
        and 1 is max power.
        
        time: the amount of time to move the robot in the specific
        direction, in seconds.
        
    Returns:
        A success message once the robot has successfully moved in the
        direction that was specified, for the specified direction.
    """
    if direction.lower() not in ["forward", "backward", "right", "lower"]:
        raise ValueError("INVALID DIRECTION SPECIFIED")
    
    if direction.lower() == "forward":
        left_motor.forward(speed=speed)
        right_motor.forward(speed=speed)
        sleep(time)
    if direction.lower() == "backward":
        left_motor.backward(speed=speed)
        right_motor.backward(speed=speed)
        sleep(time)
    if direction.lower() == "right":
        left_motor.forward(speed=speed)
        right_motor.backward(speed=speed)
        sleep(time)
    if direction.lower() == "left":
        left_motor.backward(speed=speed)
        right_motor.forward(speed=speed)
        sleep(time)
    
    return f"Successfully Moved: {direction} for {time} seconds."

model = OpenAIModel(
    client_args={
        "api_key": "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",
    },
    # **model_config
    model_id="gpt-4o",
    params={
        "max_tokens": 500,
        "temperature": 0.5,
    }
)
    
SYSTEM_PROMPT = """
"""

robot_agent = Agent(model=model, system_prompt=SYSTEM_PROMPT, tools=[move_robot])   
    