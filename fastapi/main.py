import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from magenta.styleTransfer import StyleTransfer

app = FastAPI()
styleTransfer = StyleTransfer()
path = os.getcwd()


@app.get("/")
async def root():
  return {"message": "Hello World"}


class CreateImageRequest(BaseModel):
  content_image_url: str
  style_image_url: str


@app.post("/api/createImage")
async def createImage(request: CreateImageRequest):
  print(request.content_image_url)
  print(request.style_image_url)
  imageId = styleTransfer.create(request.content_image_url, request.style_image_url)
  return imageId


@app.get("/api/image/")
async def getImage(id: str):
  file_path = os.path.join(path, f'outputImages/{id}.png')
  if os.path.exists(file_path):
    return FileResponse(file_path, media_type="image/png")
  raise HTTPException(status_code=404, detail="Item not found")
