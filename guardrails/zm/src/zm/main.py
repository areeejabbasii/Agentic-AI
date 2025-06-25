import asyncio
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrail,
    OutputGuardrail,
    OutputGuardrailTripwireTriggered,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    RunConfig
)
class mathrelevant(BaseModel):
    mathrelevant:bool
    reasoning:str
guardrails_agent=Agent(
    name="guardrails_agent",
    instruction="you are helpful assistant and you are guardrails agent",
    output_type=mathrelevant #must 
)
@InputGuardrail
async def math_guardrails(
    ctx:RunContextWrapper,agent:Agent,input:str
)->GuardrailFunctionOutput:
    result=await Runner.run(guardrails_agent,input,ctx=ctx.context)
    final_output=result.final_ouput_as(mathrelevant)# also this
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_mathrelevant
    )
agent=Agent(
    name="main agent",
     instruction="you are supervisior ",
    input_guardrails=[InputGuardrail(guardrail_function=guardrails_agent)],
)
async def main():
 try:
    result = await Runner.run( agent, "What is 2+2") 
    print("Response:", result.final_output)
 except InputGuardrailTripwireTriggered as e:
    print("Guardrail tripped: Input is not PIAIC-related.")
asyncio(main())



    