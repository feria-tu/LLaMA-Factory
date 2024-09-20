from fastapi import FastAPI, UploadFile, File
import uvicorn
from pathlib import Path
from openai import OpenAI
import os
import base64

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadfile")
async def create_upload_file(text: str, file: UploadFile = File(...)):
    # 指定图片保存路径
    save_path = Path("uploads") / file.filename
    # print("save_path:", save_path)  
    # 确保目录存在
    save_path.parent.mkdir(parents=True, exist_ok=True)
    # 保存文件
    with open(save_path, 'wb') as f:
        content = await file.read()
        f.write(content)
        print("图像上传成功")
        print("用户输入：", text)

    # 将上传的图片加密
    base64_image = encode_image(save_path)  
    result = get_response(base64_image, text)
    for i in result:
        print(i, end="", flush=True)
    return {"filename": file.filename, "text": text}

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        # print('Decoding ...')
        return base64.b64encode(image_file.read()).decode("utf-8")

def get_response(base64_image, input_text):
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
    uvicorn.run(app, host="127.0.0.1", port=8000)