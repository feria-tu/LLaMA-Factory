from fastapi import FastAPI, File, Form, UploadFile
import os
from fastapi.responses import JSONResponse
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from openai import OpenAI
import base64

app = FastAPI()

# 设置图片保存路径
UPLOAD_FOLDER = r'C:\Users\LEGION\Desktop\LLaMA-Factory\uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/uploadfile")
async def upload_file(file: UploadFile = File(...), text: str = Form(...)):
    if not file:
        return JSONResponse(status_code=400, content={"message": "No file provided"})
    if not text:
        return JSONResponse(status_code=400, content={"message": "No text provided"})

    # 保存文件
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 可以在这里保存文件路径到数据库或其他地方
    print(f'File saved to {file_path}')
    print(f'Text received: {text}')

    # 将上传的图片加密
    base64_image = encode_image(file_path)  
    result = get_response(base64_image, text)
    for i in result:
        print(i, end="", flush=True)

    return JSONResponse(status_code=200, content={"message": f"File uploaded successfully: {file.filename}", "text": text})

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        # print('Decoding ...')
        return base64.b64encode(image_file.read()).decode("utf-8")
def get_response(base64_image, input_text):
    client = OpenAI(
        # https://bailian.console.aliyun.com/?apiKey=1#/api-key
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
    # 根据心电图，最有可能诊断出什么心血管疾病
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)