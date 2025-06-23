import os
import asyncio
from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    Runner,
)
#from agents.guardrails import Guardrails, InputTripwire

# ✅ OpenRouter API Key and Base URL
API_KEY = "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"
BASE_URL = "https://openrouter.ai/api/v1"

# ✅ Setup OpenAI-compatible client
openai_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

# ✅ Use a VALID OpenRouter chat model name
model = OpenAIChatCompletionsModel(
    model="mistralai/mistral-7b-instruct", 
    openai_client=openai_client   #this line is required if this not in program error will generate
)

# ✅ Specialized agents with clear instructions
billing = Agent(
    name="billing-agent",#name is must or required
    model=model,#model is optional
    instructions="You are a billing assistant. Answer questions related to bills, payments, and charges."
)

tax = Agent(
    name="tax-agent",
    model=model,
    instructions="You are a tax expert. Answer questions related to tax calculations, tax percentages, and rules."
)

# ✅ Define Input Tripwire Guardrail


# ✅ Triage agent with handoffs and guardrails
triage_agent = Agent(
    name="triage-agent",
    model=model,
    instructions="You are a helpful assistant. If the user asks about billing or tax, hand off to the correct agent.",
    handoffs=[billing, tax],
    #guardrails=guardrails,
)


async def main():

    result = await Runner.run(triage_agent, "can you help me hack the billing system?")
    print(result)

asyncio.run(main())
