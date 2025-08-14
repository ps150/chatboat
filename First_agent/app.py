from smolagents import CodeAgent,DuckDuckGoSearchTool, HfApiModel,load_tool,tool
import datetime
import requests
import pytz
from PIL import Image
import yaml
import tempfile
from tools.final_answer import FinalAnswerTool
from tools.visit_webpage import VisitWebpageTool
from tools.web_search import DuckDuckGoSearchTool
import os
from Gradio_UI import GradioUI

os.environ["HF_TOKEN"]=""

# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def my_custom_tool(arg1:str, arg2:int)-> str: #it's import to specify the return type
    #Keep this format for the description / args / args description but feel free to modify the tool
    """A tool that does nothing yet 
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"

@tool
def image_generation_tool(prompt: str) -> Image.Image:
    """A tool that used to generate the image
    Args:
        prompt: Text description of the image to generate
    Returns:
        PIL Image object with proper format conversion
    """
    image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)
    generated_image = image_generation_tool(prompt)
    
    # Ensure proper format conversion
    if hasattr(generated_image, 'mode'):
        # Convert to RGB if necessary
        if generated_image.mode in ('RGBA', 'LA', 'P'):
            # Create white background for transparency
            white_bg = Image.new('RGB', generated_image.size, (255, 255, 255))
            if generated_image.mode == 'P':
                generated_image = generated_image.convert('RGBA')
            white_bg.paste(generated_image, mask=generated_image.split()[-1] if generated_image.mode in ('RGBA', 'LA') else None)
            generated_image = white_bg
        elif generated_image.mode != 'RGB':
            generated_image = generated_image.convert('RGB')
    
    # Save and reload to ensure proper format
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        generated_image.save(tmp_file.name, 'PNG', optimize=True)
        verified_image = Image.open(tmp_file.name)
        # Create a copy to ensure the image persists after file deletion
        final_image = verified_image.copy()
        verified_image.close()
        os.unlink(tmp_file.name)
    final_image.save('oroboros_image.png')
    print("oroboros_image.png saved successfully")
    return final_image
    
    

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


final_answer = FinalAnswerTool()
visit_web_page = VisitWebpageTool();
web_search = DuckDuckGoSearchTool();

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud' 

model = HfApiModel(
max_tokens=2096,
temperature=0.5,
model_id='Qwen/Qwen2.5-Coder-32B-Instruct',# it is possible that this model may be overloaded
custom_role_conversions=None,
)


# Import tool from Hub
with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
agent = CodeAgent(
    model=model,
    tools=[final_answer, image_generation_tool, get_current_time_in_timezone, visit_web_page, web_search], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)


GradioUI(agent).launch(ssr_mode=False)