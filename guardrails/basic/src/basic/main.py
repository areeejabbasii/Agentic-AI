import asyncio
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrail,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    RunConfig
)
config = RunConfig(

    tracing_disabled=True
)

class piaic_relevanceoutput(BaseModel):
    is_piaic_relevance:bool
    reasoning : str
guardrail_agent=Agent(
    name="guardrails_agent",
    instruction="you are for is output is good or bad",
    output_type=piaic_relevanceoutput
)
async def piaic_relevance_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list,
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context, run_config = config)
    final_output = result.final_output_as(piaic_relevanceoutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_piaic_relevant,
    )
agent=Agent(
    name="main agent",
    instruction="you are supervisior ",
    input_guardrails=[InputGuardrail(guardrail_function=piaic_relevance_guardrail)],
)
async def main():
 try:
    result = await Runner.run( agent, "What is the curriculum for PIAIC's AI course?", run_config = config)
    print("Response:", result.final_output)
 except InputGuardrailTripwireTriggered as e:
    print("Guardrail tripped: Input is not PIAIC-related.")
asyncio(main())

    
    



    



