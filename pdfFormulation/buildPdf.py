
def main(image_path: str):
    with open ("bbox.py", "w") as bbox_file:
        bbox_file.write("# auto generated\n")
        bbox_file.write("import cv2 as cv\n")
        bbox_file.write(f"image = cv.imread('{image_path}')\n")
        with open("pdfFormulation/bounding_box_response.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                bbox_file.write(line)
        bbox_file.write("cv.imshow('Image with Bounding Box', image)\n")
        bbox_file.write("cv.waitKey(0)\n")

if __name__ == "__main__":
    main()