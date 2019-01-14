import numpy as np
import cv2, wx
from PIL import ImageGrab
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:\Program Files (x86)\Tesseract-OCR\Tesseract.exe"

class SelectableFrame(wx.Frame):

    c1 = None
    c2 = None

    def __init__(self, parent=None, id=-1, title=""):
        wx.Frame.__init__(self, parent, id, title, size=wx.DisplaySize())
        self.panel = wx.Panel(self, size=self.GetSize())

        self.panel.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.panel.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)
        self.SetTransparent(50)

    def OnMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            self.c2 = event.GetPosition()
            self.Refresh()

    def OnMouseDown(self, event):
        self.c1 = event.GetPosition()
        c1 = (str(self.c1).strip("( )"))

    def OnMouseUp(self, event):
        c1 = (str(self.c1).strip("( )"))
        c2 = (str(self.c2).strip("( )"))
        global box_pos
        box_pos = c1 + ", " + c2
        global x1
        global y1
        global x2
        global y2

        x1, y1, x2, y2 = box_pos.split(",")
        self.Destroy()

    def OnPaint(self, event):
        if self.c1 is None or self.c2 is None: return

        dc = wx.PaintDC(self.panel)
        dc.SetPen(wx.Pen('red', 1))
        dc.DrawRectangle(self.c1.x, self.c1.y, self.c2.x - self.c1.x, self.c2.y - self.c1.y)

    def PrintPosition(self, pos):
        return str(pos.x) + " " + str(pos.y)

class MyApp(wx.App):

    def OnInit(self):
        frame = SelectableFrame()
        frame.Show(True)
        self.SetTopWindow(frame)

        return True

app = MyApp(0)
app.MainLoop()

while True:
    orig_img = ImageGrab.grab(bbox=(int(x1) + 10, int(y1) + 30, int(x2) + 10, int(y2) + 30))

    np_im = np.array(orig_img)

    img = cv2.cvtColor(np_im, cv2.COLOR_BGR2GRAY)

    im = Image.fromarray(img)

    im.save("img.png")

    cv2.imshow('window', img)

    text = pytesseract.image_to_string(Image.open('img.png'))

    print(text)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
