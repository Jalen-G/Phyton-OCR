import numpy as np
import cv2
from PIL import ImageGrab
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

box_pos = (631, 231, 691, 305)

while True:
    orig_img = ImageGrab.grab(box_pos)

    np_im = np.array(orig_img)

    img = cv2.cvtColor(np_im, cv2.COLOR_BGR2GRAY)

    im = Image.fromarray(img)

    im.save("img.png")

    cv2.imshow('window',img)

    text = pytesseract.image_to_string(Image.open("img.png"))


    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
