from tkinter import *
from Calculator import *
import numpy as np
import requests
import datetime
from PIL import ImageTk, Image
from io import BytesIO

# values for icon and window size
TEAM_ICON_W = 64
TEAM_ICON_H = TEAM_ICON_W
MIDFRAME_W = 700
MIDFRAME_H = MIDFRAME_W

ans = [[]]  # initializes variable to hold 2D list of all (superlative) circles of suck
uDict = []  # initializes variable to hold list of url's to team icons
iterable = 0  # variable to index through ans
R = 250  # variable that dictates radius of circle of suck


def getIcon(url):
    response = requests.get(url)
    img_data = response.content  # getting image data from url
    image = Image.open(BytesIO(img_data))  # convert to PIL image
    img = ImageTk.PhotoImage(image.resize((TEAM_ICON_W, TEAM_ICON_H)))  # image sized to define width and height
    return img


def getSymbol(url, phi):
    image = Image.open(url)
    img = ImageTk.PhotoImage(image.rotate(phi))  # greater than symbol rotated as desired in drawSuck
    return img


def coordinates(iter, total):
    global R
    c_x = MIDFRAME_W / 2
    c_y = MIDFRAME_H / 2
    tau = np.pi * 2
    frac = iter / total
    x = R * np.sin(tau * frac) + c_x
    y = -R * np.cos(tau * frac) + c_y
    phi = -frac * 360.0
    return x, y, phi  # returns coordinates and rotation data for team icons and greater than symbol


def getAllCircs(yr, cf, sp):
    global R
    calcObj = Calculator(int(yr), cf)  # new Calculator obj based on user input
    if sp == "biggest":
        answer = calcObj.findMaxCircs()
        R = 250
    else:
        answer = calcObj.findMinCircs()
        R = 125
    return answer, calcObj.urlDict


def drawSuck(iter):
    global canvas, ans, MIDFRAME_W, MIDFRAME_H
    canvas.delete("all")
    canvas.images.clear()  # erase canvas
    if ans.__len__() == 0:
        canvas.create_text(MIDFRAME_W/2, MIDFRAME_H/2, text="Data not available for this request")
    else:
        for i in range(ans[iter].__len__()):  # positions all images on canvas
            xpos1, ypos1, _ = coordinates(i, ans[iter].__len__())
            xpos2, ypos2, ang = coordinates(i + 0.5, ans[iter].__len__())
            icon = getIcon(uDict[ans[iter][i]])
            symbol = getSymbol("greater_than.png", ang)
            canvas.create_image(xpos1, ypos1, image=icon)
            canvas.create_image(xpos2, ypos2, image=symbol)
            canvas.images.append(symbol)
            canvas.images.append(icon)



def resetFlipper():
    global flipLbl, rightBtn, leftBtn, iterText, iterable, iterText, ans

    iterText.set(f"{str(iterable + 1)} of {str(ans.__len__())}")  # tells user which circle they're viewing
    flipLbl = Label(frame2, textvariable=iterText)
    rightBtn = Button(frame2, text=">>", command=goRight)
    leftBtn = Button(frame2, text="<<", command=goLeft)


def goLeft():
    global flipLbl, rightBtn, leftBtn, canvas, iterable, frame2, root, iterText
    if iterable > 0:
        iterable = iterable - 1
        drawSuck(iterable)  # paints previous circle of suck

        resetFlipper()
        root.update()


def goRight():
    global flipLbl, rightBtn, leftBtn, canvas, iterable, frame2, root, iterText, ans
    if iterable < ans.__len__() - 1:
        iterable = iterable + 1
        drawSuck(iterable)  # paints next circle of suck

        resetFlipper()
        root.update()


def rotRight():
    global ans, iterable, root
    holder = ans[iterable].pop()
    ans[iterable].insert(0, holder)  # shifts list, effectively "rotating" circle once painted
    drawSuck(iterable)

    root.update()


def rotLeft():
    global ans, iterable, root
    holder = ans[iterable][0]
    del ans[iterable][0]
    ans[iterable].append(holder)  # shifts list, effectively "rotating" circle once painted
    drawSuck(iterable)

    root.update()


def goClicked():
    global ans, uDict, yearDef, conferenceDef, superlativeDef, iterable, root, flipLbl, rightBtn, leftBtn, iterText
    ans, uDict = getAllCircs(yearDef.get(), conferenceDef.get(), superlativeDef.get())
    iterable = 0  # 0th list from ans as default
    drawSuck(iterable)  # draw circle of suck

    resetFlipper()
    root.update()


root = Tk()
root.title("Circle of Suck Calculator")
root.geometry("1250x750")

today = datetime.date.today()
year = today.year
yrArray = list(map(str, list(range(year - 0, 1979, -1))))  # create array for year selection on GUI

iterText = StringVar(root)
iterText.set(f"{str(iterable + 1)} of {str(ans.__len__() + 1)}")  # create text to tell user which circle they're viewing

frame1 = Frame(root, width=1250)
frame1.pack()

canvas = Canvas(root, width=MIDFRAME_W, height=MIDFRAME_H)
canvas.pack()
canvas.images = list()

frame2 = Frame(root, height=1250)
frame2.pack()

# setting defaults for dropdowns
superlativeDef = StringVar(root)
superlativeDef.set("biggest")
conferenceDef = StringVar(root)
conferenceDef.set("B1G")
yearDef = StringVar(root)
yearDef.set("2015")

# setting widgets on top of GUI
iWantLbl = Label(frame1, text="I want the ")
superlDD = OptionMenu(frame1, superlativeDef, *["biggest", "smallest"])
cSuckLbl = Label(frame1, text=" circle of suck from the ")
cnfnceDD = OptionMenu(frame1, conferenceDef, *["B1G", "SEC", "B12", "ACC", "PAC", "MWC"])
theirsDD = Label(frame1, text=" Conference's ")
yearDD = OptionMenu(frame1, yearDef, *yrArray)
seasonDD = Label(frame1, text=" season. ")
calcBtn = Button(frame1, text="GO!", command=goClicked)

# getting first circle of suck answer as "ans"
ans, uDict = getAllCircs(yearDef.get(), conferenceDef.get(), superlativeDef.get())

#display top widgets
iWantLbl.pack(side=LEFT)
superlDD.pack(side=LEFT)
cSuckLbl.pack(side=LEFT)
cnfnceDD.pack(side=LEFT)
theirsDD.pack(side=LEFT)
yearDD.pack(side=LEFT)
seasonDD.pack(side=LEFT)
calcBtn.pack(side=LEFT, padx=10)

#setting bottom widgets
rotLBtn = Button(frame2, text="↺", command=rotLeft)
leftBtn = Button(frame2, text="<<", command=goLeft)
flipLbl = Label(frame2, textvariable=iterText)
rightBtn = Button(frame2, text=">>", command=goRight)
rotRBtn = Button(frame2, text="↻", command=rotRight)

#display bottom widgets
rotLBtn.pack(side=LEFT, padx=10)
leftBtn.pack(side=LEFT, padx=10)
flipLbl.pack(side=LEFT)
rightBtn.pack(side=LEFT, padx=10)
rotRBtn.pack(side=LEFT, padx=10)

drawSuck(iterable)

root.mainloop()
