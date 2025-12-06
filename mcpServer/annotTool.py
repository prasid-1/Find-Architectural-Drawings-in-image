from mcp.server.fastmcp import FastMCP

mcp = FastMCP("annotationTool")

@mcp.tool()
def annotTool(x1: int, y1: int, x2: int, y2: int):
    """
    Use this tool for EVERY bounding box annotation in the image.
    The model MUST call this tool instead of describing the bounding box in text.
    This tool writes the bounding box to a file which will be rendered later.

    Args:
        x1 (int): The x-coordinate of the top-left corner.
        y1 (int): The y-coordinate of the top-left corner.
        x2 (int): The x-coordinate of the bottom-right corner.
        y2 (int): The y-coordinate of the bottom-right corner.

    Returns:
        str: A string representation of the rectangle drawing code.
    """
    with open ("pdfFormulation/bounding_box_response.txt", "a") as f:
        f.write(f"image = cv.rectangle(image, ({x1}, {y1}), ({x2}, {y2}), color=(0, 255, 0), thickness=2)\n")

    return f"image = cv.rectangle(image, ({x1}, {y1}), ({x2}, {y2}), color=(0, 255, 0), thickness=2)\n"


if __name__ == "__main__":
    mcp.run(transport="stdio")