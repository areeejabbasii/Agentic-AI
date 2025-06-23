import asyncio
from agents import Agent
from agents.tool import tool  # ✅ correct for v0.0.19
from agents.guardrail import input_guardrail, GuardrailFunctionOutput
from agents.exceptions import InputGuardrailTripwireTriggered
from agents.run_context import RunContextWrapper
from agents.agent import Agent as BaseAgent
from typing import Any


@tool  # ✅ use tool decorator here
def greet(name: str) -> str:
    return f"Hello, {name}!"


@input_guardrail
async def block_bad_words(
    context: RunContextWrapper[Any],
    agent: BaseAgent[Any],
    user_input: str
) -> GuardrailFunctionOutput:
    banned = ["hack", "violence", "kill"]
    for word in banned:
        if word in user_input.lower():
            return GuardrailFunctionOutput(
                tripwire_triggered=True,
                output_info="🚫 This topic is not allowed!"
            )
    return GuardrailFunctionOutput(
        tripwire_triggered=False,
        output_info=None
    )


agent = Agent(
    name="SimpleAgent",
    tools=[greet],
    guardrails=[block_bad_words]
)


async def main():
    try:
        user_input = input("Ask me something: ")
        result = await agent.run(user_input)
        print(result.message.content)
    except InputGuardrailTripwireTriggered as e:
        print(e.tripwire.message)


if __name__ == "__main__":
    asyncio.run(main())
