import os
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, tool

os.environ["HF_TOKEN"]="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"

model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-3B-Instruct")

@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on the occasion.
    Args:
        occasion (str): The type of occasion for the party. Allowed values are:
                        - "casual": Menu for casual party.
                        - "formal": Menu for formal party.
                        - "superhero": Menu for superhero party.
                        - "custom": Custom menu.
    """
    if occasion == "casual":
        return "Pizza, snacks, and drinks."
    elif occasion == "formal":
        return "3-course dinner with wine and dessert."
    elif occasion == "superhero":
        return "Buffet with high-energy and healthy food."
    else:
        return "Custom menu for the butler."

agent = CodeAgent(tools=[suggest_menu], model=model)

agent.run("Search for the best music recommendations for a party at the Wayne's mansion.")