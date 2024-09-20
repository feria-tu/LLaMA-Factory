from openai import OpenAI
import os
import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Path to your image
image_path = r"C:\Users\LEGION\Desktop\LLaMA-Factory\uploads\ECG.png"

# Getting the base64 string
base64_image = encode_image(image_path)

def get_response(input_text):
    client = OpenAI(
        api_key="sk-ae585937ce0b4f529b79dc5bae307cdc",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-vl-max-0809",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": input_text},
                    # {
                    #     "type": "image_url",
                    #     "image_url": {
                    #         "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"
                    #     },
                    # },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        top_p=0.8,
        stream=True,
        stream_options={"include_usage": True},
    )
    for chunk in completion:
        if 'content' not in chunk.model_dump_json() or chunk.choices[0].delta.content == "":  
            continue
        yield chunk.choices[0].delta.content


if __name__ == "__main__":
    # input_text = input("用户：")  # 根据心电图，最有可能诊断出什么心血管疾病
    input_text = "根据心电图，最有可能诊断出什么心血管疾病"
    result = get_response(input_text)
    for i in result:
        print(i, end="", flush=True)
