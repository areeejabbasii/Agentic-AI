'''import chainlit as cl
from agent import run_agent

@cl.on_chat_start
async def start():
    await cl.Message(content="Hello! I'm a weather bot. How can I help you today?").send()

@cl.on_message
async def on_message(message: str):
    print(f"received message :{message.content}")
    result = run_agent(message.content)
    print(f"Agent response: {result}")
    await cl.Message(content=result).send()'''

    import chainlit as cl
from hello import get_weather  # Make sure you have a file hello.py with a get_weather function

@cl.on_chat_start
async def start():
    await cl.Message(content="Hello! I'm a weather bot. Type your city name to get the current weather.").send()

@cl.on_message
async def on_message(message: cl.Message):
    city = message.content.strip()
    try:
        weather = get_weather(city)
        await cl.Message(content=weather).send()
    except Exception as e:
        await cl.Message(content=f"Sorry, an error occurred: {str(e)}").send()



