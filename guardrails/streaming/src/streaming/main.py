#here is the concept of streaming 
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent,Runner
async def main():
    agent=Agent(
        name="joker"
    )
    result=Runner.run_streamed(agent,input="please say five jokes")
    async for event in result.stream_events():
        if event.type=="raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
             print(event.data.delta, end="", flush=True)
asyncio(main())             
