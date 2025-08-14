import os
from huggingface_hub import InferenceClient

os.environ["HF_TOKEN"]=""

client = InferenceClient("meta-llama/Llama-3.2-3B-Instruct")
# if the outputs for next cells are wrong, the free model may be overloaded. You can also use this public endpoint that contains Llama-3.2-3B-Instruct
#client = InferenceClient("https://jc26mwg228mkj8dw.us-east-1.aws.endpoints.huggingface.cloud")
# As seen in the LLM section, if we just do decoding, **the model will only stop when it predicts an EOS token**, 
# and this does not happen here because this is a conversational (chat) model and we didn't apply the chat template it expects.

# output = client.text_generation(
#     "The capital of france is",
#     max_new_tokens=100,
# )

# prompt="""<|begin_of_text|><|start_header_id|>user<|end_header_id|>

# The capital of France is<|eot_id|><|start_header_id|>assistant<|end_header_id|>

# """
# output = client.text_generation(
#     prompt,
#     max_new_tokens=100,
# )

# print(output)

output = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "The capital of France is"}
    ],
    stream=False,
    max_tokens=1024,
)
print(output.choices[0].message.content)

