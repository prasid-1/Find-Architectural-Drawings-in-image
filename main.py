from anot import gptPrompter
import asyncio
from pdfFormulation import buildPdf
import os
import cv2 as cv

async def main():
    img_path = "input_image/image_resized.png"
    prompt = f" Detect only architectural drawings in provide image {getImageSize(img_path)}. Do not detect text or other informational figures. Draw bounding box in each drawing. You MUST call the tool 'annotTool' for EVERY bounding box you detect. Output bounding box coordinates to user in json format. Never describe bounding boxes in text. The ONLY valid output for drawing rectangles is calling annotTool. Whenever you detect or mention any bounding box, immediately call annotTool."
    
    with open("pdfFormulation/bounding_box_response.txt", "w", encoding="utf-8") as f:
        f.write("")  # Clear previous content

    await gptPrompter.main(img_path, prompt, stream_chunk=stream_chunk )

    buildPdf.main(img_path) # builds python code to annotate pdf

    os.system('python bbox.py') # run built pdf annotation python file

# get image dimensions
def getImageSize(image_path):
    img = cv.imread(image_path)
    h, w, channels = img.shape

    return f"({w} X {h})"

#used for streamming
def stream_chunk(text):
    print(text, end='', flush=True)

if __name__ == "__main__":
    asyncio.run(main())