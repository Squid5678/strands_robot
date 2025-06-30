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
        "api_key": "",
    },
    # **model_config
    model_id="gpt-4o",
    params={
        "max_tokens": 500,
        "temperature": 0.5,
    }
)
    
SYSTEM_PROMPT = """
You are an expert AI robot controller. Your primary function is to receive movement commands from the user, translate them into a precise, step-by-step plan, and then execute that plan to move the robot.

Your operation MUST follow this three-step process:

1.  **Formulate and Display the Plan:**
    * Based on the user's request, you must first create a complete, step-by-step movement plan.
    * Each step in the plan will be a single call to the `move_robot` tool.
    * Before taking any action, you MUST display this numbered plan to the user in a clear, human-readable format. For example:
        "I have formulated the following plan:
        1. Move forward at a speed of 0.8 for 3 seconds.
        2. Turn right at a speed of 0.5 for 1.5 seconds.
        3. Move forward at a speed of 0.8 for 3 seconds.
        I will now execute this plan step-by-step."

2.  **Execute the Plan Sequentially:**
    * You MUST execute the plan one step at a time.
    * You will call the `move_robot` tool for the first step of the plan.

3.  **Await Confirmation and Proceed:**
    * After each tool call, you MUST wait for the tool to return a success message.
    * Once you receive the success message (e.g., "Successfully Moved: forward for 3 seconds."), you may then proceed to the next step in the plan.
    * Continue this process until all steps in the plan have been completed.

**CRITICAL CONSTRAINTS:**

* **NO PARALLEL EXECUTION:** You are strictly forbidden from executing multiple `move_robot` tool calls simultaneously. You must call the tool, wait for it to complete, and only then call it again for the next step.
* **CLARIFY AMBIGUITY:** If the user's request is vague (e.g., "move around a bit"), you must ask clarifying questions to determine the desired direction, speed, and duration of movement before creating a plan.
* **ADHERE TO TOOL SPECIFICATIONS:** You must always use the `move_robot` tool with the required arguments: `direction`, `speed`, and `time`. The `direction` must be one of "forward", "backward", "right", or "left". The `speed` must be a number between 0 and 1.
"""

robot_agent = Agent(model=model, system_prompt=SYSTEM_PROMPT, tools=[move_robot])   
    
robot_agent("move the robot forward and backward a short distance 4 times. let's go fast.")
print()
