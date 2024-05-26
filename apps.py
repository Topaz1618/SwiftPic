import os

from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, FileResponse  # 确保包括 FileResponse

from PIL import Image, ImageOps
import io
import base64

from utilities.gray_converter import GrayImageProcessor
from utilities.overlay_effects import OverlayEffectsProcessor


VIDEO_FOLDER = "instance/video"
templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/videos", StaticFiles(directory="instance/video"), name="videos")


@app.get("/")
def main():
    return FileResponse('templates/index.html')


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


@app.post("/api/video_text_extractor")
async def video_text_extractor(request: Request):
    data = await request.json()

    current_page = int(data.get('current_page', 1))
    page_limitation = int(data.get('page_limitation', 10))

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
