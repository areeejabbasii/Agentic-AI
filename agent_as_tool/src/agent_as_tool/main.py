
from agents import Agent,OpenAIChatCompletionsModel,AsyncOpenAI, ItemHelpers, MessageOutputItem, Runner, trace
import chainlit as cl
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, Runner

api_key="sk-" #  Replace with your real key or use env vars for safety

external_client = AsyncOpenAI(api_key=api_key)

model = OpenAIChatCompletionsModel(
    model="gpt-4o",
    openai_client=external_client,
)


spanish_agent = Agent(
    name="spanish agent",
    instructions="you answer in spanish",
    model=model,
    handoff_description="English to Spanish translator",
)

french_agent = Agent(
    name="french agent",
    instructions="you answer in french",
    model=model,
    handoff_description="English to French translator",
)

italian_agent = Agent(
    name="italian agent",
    instructions="you answer in italian",
    model=model,
    handoff_description="English to Italian translator",
)

# Orchestrator agent(manager)
orchestrator_agent = Agent(
    name="orchestrator agent",
    instructions=(
        "You are a translation agent. Use the tools to translate. "
        "You never translate yourself; always delegate."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
        italian_agent.as_tool(
            tool_name="translate_to_italian",
            tool_description="Translate the user's message to Italian",
        ),
    ],
    model=model,
)


@cl.on_message
async def on_message(message: cl.Message):
    
    result = await Runner.run(orchestrator_agent, message.content)

    
    await cl.Message(content=result.final_output).send()
