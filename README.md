**Project**

- **Description:** Find and annotate architectural drawings in a provided image. The project uses an LLM-driven prompter to detect drawing regions, outputs bounding box coordinates, and generates an OpenCV script to visualize those boxes on the image.

**Requirements**

- **Python:**: 3.8+.
- **Dependencies:**: See `requirements.txt`. At minimum the project requires `opencv-python` and any packages referenced by `anot/gptPrompter.py` (LLM/HTTP client libraries).

**Quick Start**

- **1. Create and activate a virtual environment (PowerShell):**

  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

- **2. Install dependencies:**

  ```powershell
  python -m pip install -r requirements.txt
  ```

- **3. Add an input image:** Put your image file at `input_image/image_resized.png` or change the path in `main.py`.

- **4. Run the pipeline:**

  ```powershell
  python main.py
  ```

**What the pipeline does**

- **`main.py`**: Entry point that composes a detection prompt, clears previous responses, calls the LLM prompter, builds an annotation script, and runs it.
- **LLM step**: `anot/gptPrompter.py` is expected to call an LLM (configured in that module) and write bounding boxes in `pdfFormulation/bounding_box_response.txt` and/or call the project's tool `annotTool` for each bounding box as required by the prompt.
- **`pdfFormulation/buildPdf.py`**: Converts the bounding-box output into a runnable Python annotation file (`bbox.py`).
- **`bbox.py`**: Auto-generated script that draws rectangles on `input_image/image_resized.png` using OpenCV and displays the result.

**Files & Purpose**

- **`main.py`**: Orchestrates the detection -> build -> annotate flow.
- **`anot/gptPrompter.py`**: LLM prompt sender / response handler. Configure your API credentials or settings here if needed.
- **`pdfFormulation/buildPdf.py`**: Takes the bounding-box response and writes `bbox.py` (visualizer/annotator).
- **`pdfFormulation/bounding_box_response.txt`**: Text output produced by the LLM or prompter containing bounding box coordinates.
- **`bbox.py`**: Generated script that uses OpenCV to draw bounding boxes and show the image.
- **`mcpServer/annotTool.py`**: Tool expected to be invoked by the prompter/LLM for each bounding box (project-specific integration).
- **`input_image/`**: Place input images here. The pipeline expects `image_resized.png` by default.

**Usage notes & tips**

- **LLM configuration:**: If `anot/gptPrompter.py` uses an external LLM or API, set any required API keys or environment variables before running. Check that module for details.
- **Headless environments:**: `bbox.py` uses `cv2.imshow` to display images. On headless servers, modify `bbox.py` to save the annotated image instead (use `cv2.imwrite`) or run locally with a display.
- **Adjusting detection prompt or image path:**: Edit `main.py` to change the prompt or to point to another input image.

**Troubleshooting**

- **OpenCV errors on import:**: Ensure `opencv-python` is installed in the active environment.
- **No bounding boxes produced:**: Check `pdfFormulation/bounding_box_response.txt` and `anot/gptPrompter.py` logs — the LLM may not be returning the expected tool calls or JSON. Confirm the prompt format and LLM configuration.
- **`bbox.py` not generated:**: Verify `buildPdf.py` ran and that `pdfFormulation` has write permission.

**Extending this project**

- Replace the simple `bbox.py` generation with a library that writes results directly to PDF or overlays vector boxes.
- Add unit tests for parsing the LLM response and for `buildPdf.py` logic.
