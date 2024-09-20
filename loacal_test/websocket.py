from fastapi import FastAPI, WebSocket, File, UploadFile
import os
from fastapi.responses import JSONResponse, HTMLResponse
from openai import OpenAI
import base64

app = FastAPI()

# 设置图片保存路径
UPLOAD_FOLDER = r'C:\Users\LEGION\Desktop\LLaMA-Factory\uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.websocket("/ws/uploadfile")
async def websocket_upload(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        data = await websocket.receive_json()
        
        if 'file' not in data or 'text' not in data:
            await websocket.send_json({"message": "No file or text provided"})
            continue
        
        file = data['file']
        text = data['text']
        
        # 保存文件
        file_path = os.path.join(UPLOAD_FOLDER, file['filename'])
        with open(file_path, "wb") as buffer:
            buffer.write(base64.b64decode(file['data']))
        
        # 将上传的图片加密
        base64_image = encode_image(file_path)  
        result = get_response(base64_image, text)
        
        # 发送流式数据
        for i in result:
            await websocket.send_text(i)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
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
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)