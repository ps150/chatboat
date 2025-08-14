from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.tools import FunctionTool
from llama_index.core.workflow import Context

import asyncio
import os;

os.environ["HF_TOKEN"]=""


hf_token = os.getenv("HF_TOKEN")
def multiply(a : int, b: int) -> int:
    """Multiply two integers and return the resulting integer"""
    return a * b;

async def main():
    llm = HuggingFaceInferenceAPI(model_name="Qwen/Qwen2.5-Coder-32B-Instruct")
    agent = AgentWorkflow.from_tools_or_functions(
        [FunctionTool.from_defaults(multiply)],
        llm=llm
    )

    response = await agent.run("What is 2 times 2?")
    print(response)

    # remembering state
    ctx = Context(agent)

    response = await agent.run("My name is Bob.", ctx=ctx)
    # print(response)
    response = await agent.run("What was my name again?", ctx=ctx)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
