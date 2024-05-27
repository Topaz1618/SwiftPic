import os
import json
import asyncio
import redis
from time import time, sleep

from typing import List
from PIL import Image, ImageOps
import io
import base64

from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, File, UploadFile, Form, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, FileResponse  # 确保包括 FileResponse

from utilities.gray_converter import GrayImageProcessor
from utilities.overlay_effects import OverlayEffectsProcessor
from utilities.video_ocr_processor import VideoProcessor
from enums import UpdateField, FileStatus

VIDEO_FOLDER = "instance/video"
templates = Jinja2Templates(directory="templates")

app = FastAPI()
active_connections = set()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/videos", StaticFiles(directory="instance/video"), name="videos")

r = redis.Redis(host="127.0.0.1", port=6379)


@app.get("/")
def main():
    return FileResponse('templates/index.html')


@app.get("/test/{page_id}")
def test():
    return FileResponse('templates/test.html')


async def ws_callback(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        data = json.loads(data)
        res_dict = {}

        for video_name in data["videos"]:
            res = r.hgetall(video_name)
            decoded_result = {}
            for key, value in res.items():
                decoded_key = key.decode('utf-8')
                decoded_value = value.decode('utf-8')
                decoded_result[decoded_key] = decoded_value
            res_dict[video_name] = decoded_result
        # await websocket.send_text(json.dumps({ "a.mp4": {"status": FileStatus.COMPLETED.value},"b.mp4": {"status": FileStatus.COMPLETED.value, "result": f"page{page_id} {time()}"}}))
        await websocket.send_text(json.dumps(res_dict))


@app.websocket("/ws/{page_id}")
async def websocket_endpoint(websocket: WebSocket, page_id: str):
    await ws_callback(websocket)


# WebSocket 路由，处理连接
@app.websocket("/ws/video_progress")
async def websocket_endpoint(websocket: WebSocket):
    await ws_callback(websocket)


@app.post("/upload_image")
async def upload_image(image: UploadFile = File(...), operation: str = Form(...)):
    contents = await image.read()

    img = Image.open(io.BytesIO(contents))

    if operation == 'grayscale':
        img = GrayImageProcessor().process_bytes(img)

    elif operation == 'overlay_effects':
        img = OverlayEffectsProcessor().process_bytes(img)

    elif operation == 'invert':
        img = ImageOps.invert(img.convert('RGB'))

    elif operation == 'rotate':
        img = img.rotate(90, expand=True)

    img_str = base64.b64encode(img).decode('utf-8')

    return JSONResponse(content={"data": img_str})


@app.get("/video_text_extractor_page")
async def video_text_extractor_page(request: Request):
    return templates.TemplateResponse("video_text_extractor.html", {"request": request})


@app.get("/api/video_text_extractor")
async def fetch_uploaded_video(request: Request):
    current_page = int(request.query_params.get('current_page', 1))
    page_limitation = int(request.query_params.get('page_limitation', 10))

    upload_folder = VIDEO_FOLDER
    all_files = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
    all_files.sort(key=lambda x: os.path.getmtime(os.path.join(upload_folder, x)), reverse=True)

    total_images = len(all_files)  # 总图片数量
    total_pages = (total_images + page_limitation - 1) // page_limitation

    # Calculate start and end slicing indices
    start = (current_page - 1) * page_limitation
    end = start + page_limitation

    # Paginate the files
    paginated_files = all_files[start:end]
    return JSONResponse({'uploaded_images': paginated_files, 'total': total_images, 'currentPage': current_page,
                         'totalPages': total_pages})


@app.post("/api/video_text_extractor")
async def video_text_extractor(request: Request):
    from time import sleep, time

    # data = await request.json()
    # processor = VideoProcessor(data["videos"])
    # result = await asyncio.get_event_loop().run_in_executor(None, processor.process_videos)

    data = await request.json()
    print("Before:", time(), data)

    processor = VideoProcessor(data["videos"])
    loop = asyncio.get_event_loop()
    asyncio.gather(loop.run_in_executor(None, processor.process_videos), )

    # print("After:", time(), result)
    # return JSONResponse(result)
    return "ok"


def process_videos():
    from time import time, sleep
    print(f"process {time()}")

    sleep(5)
    return int(time())

#
# @app.get("/t")
# async def test(request: Request):
#     from time import sleep, time
#
#     print("Before:", time())
#     data = await request.json()
#     processor = VideoProcessor(data["videos"])
#     loop = asyncio.get_event_loop()
#     asyncio.gather(loop.run_in_executor(None, processor.process_videos, data), )
#
#     print("After:", time())
#     # return JSONResponse(result)
#     return "ok"
