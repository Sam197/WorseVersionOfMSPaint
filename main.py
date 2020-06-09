import pygame
import os
import pickle
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
import random
import time

pygame.init()

SCREENX = 1000
SCREENY = 770

print(os.getcwd())

global TILE_SIZE
TILE_SIZE = 20
Brush_size = 2
TILE_BLOCK = pygame.image.load(os.path.join('Sprites', 'Transparent.png'))
TestBLOCK = pygame.image.load(os.path.join('Sprites', 'Test.png'))

COLOUR_FONT = pygame.font.SysFont('Comicsans', 30)
BUTTON_FONT = pygame.font.SysFont('Comicsans', 30)

def SaveImg(grid):
    for row in grid:
        for col in row:
            if col.curIMG == TILE_BLOCK:
                col.curIMG = None

    toSaveGrid = (TILE_SIZE, grid)
    root = Tk()
    root.withdraw()
    root.filename = filedialog.asksaveasfile(mode = "w")
    pickle_out = open(root.filename.name, "wb")
    pickle.dump(toSaveGrid, pickle_out)
    pickle_out.close()
    ConvertBack(grid)
    messagebox.showinfo('Save', 'Saved Sucessfully')
    root.destroy()

def LoadImg():

    global TILE_SIZE

    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfile(mode = "r")
    name = root.filename.name

    grid = []
    try:
        pickle_in = open(name, "rb")
        TILE_SIZE, grid = pickle.load(pickle_in)
    except:
        print("No Tile Size Serialized, loading grid, defulting to 20, please save again to give a Serialized")
        pickle_in = open(name, "rb")
        grid = pickle.load(pickle_in)
        TILE_SIZE = 20

    ConvertBack(grid)
    root.destroy()
    return grid

def ConvertBack(grid):
    for row in grid:
        for col in row:
            if col.curIMG == None:
                col.curIMG = TILE_BLOCK

class Tile:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 0
        self.g = 0
        self.b = 0
        self.curIMG = TILE_BLOCK

    def draw(self, screen):
        try:
            screen.blit(self.curIMG, (self.x, self.y))
        except:
            pygame.draw.rect(screen, (self.r, self.g, self.b), (self.x, self.y, TILE_SIZE, TILE_SIZE))

class Slider:

    def __init__(self, x, y, colour):
        self.x = x
        self.circleX = x
        self.y = y
        self.colour = colour

    def draw(self, screen):
        text = COLOUR_FONT.render(self.colour + "  -  " + str(int((self.circleX -10)/2)), 1, (0,0,0))
        screen.blit(text, (self.x, self.y))
        pygame.draw.rect(screen, (0,0,0), (self.x, self.y + 20, 510, 30))
        pygame.draw.rect(screen, (255,255,255), (self.x + 1, self.y + 21, 508, 28))
        pygame.draw.circle(screen, (0,0,0), (self.circleX, self.y + 35), 10)

class ButtonNotTk:

    def __init__(self, x, y, commandPos, ToShow, Acolour, Bcolour, length, height):
        self.x = x
        self.y = y
        self.isPressed = False
        self.commandPos = commandPos
        self.text = ToShow
        self.Acolour = Acolour
        self.Bcolour = Bcolour
        self.length = length
        self.height = height
    
    def pressed(self):
        if self.isPressed:
            self.isPressed = False
            print(self.isPressed)
            return 0
        else:
            self.isPressed = True
            print(self.isPressed)
            return self.commandPos

    def draw(self, screen):
        if not self.isPressed:
            self.Acolour = (255,255,255)
        if self.isPressed:
            self.Acolour = (255,0,0)
        pygame.draw.rect(screen, self.Bcolour, (self.x, self.y, self.length, self.height))
        pygame.draw.rect(screen, self.Acolour, (self.x +1, self.y + 1, self.length - 2, self.height - 2))
        text = BUTTON_FONT.render(self.text, 1, self.Bcolour)
        screen.blit(text, (self.x +5, self.y + 5))

def make_grid():
    final_grid = []
    for y in range(0, SCREENY - 150, TILE_SIZE):
        placeholder = []
        for x in range(0, SCREENX, TILE_SIZE):
            placeholder.append(Tile(x, y))
        final_grid.append(placeholder)
        del placeholder

    return final_grid

def drawALL(screen, grid, redSlider, greenSlider, blueSlider, buttons):
    for row in grid:
        for col in row:
            col.draw(screen)

    pygame.draw.line(screen, (0,0,0), (0, 600), (1000, 600), 1)

    redSlider.draw(screen)
    greenSlider.draw(screen)
    blueSlider.draw(screen)

    pygame.draw.rect(screen, colour, (530, 625, 20, 140))

    for btn in buttons:
        btn.draw(screen)

def main():

    screen = pygame.display.set_mode((SCREENX, SCREENY))
    screen.fill((255,255,255))
    pygame.display.update()

    global grid
    grid = make_grid()

    mouseDown = False

    red = 0
    green = 0
    blue = 0
    global colour
    colour = (red, green, blue)

    redSlider = Slider(10, 605, "Red")        #The total setup is 50pixels  + 5 gap
    greenSlider = Slider(10, 660, "Green")
    blueSlider = Slider(10, 715, "Blue")

    buttonCommands = [None, "Draw", "Erase", "Fill", "Line", "Pippette"]   # Just for refrence
    curCommand = 0
    buttons = []
    startofCoolDown = time.time()
    cooldowntime = 0.1

    drawButton = ButtonNotTk(560, 610, 1, "Draw", (255,255,255), colour, 100, 25)
    buttons.append(drawButton)
    curCommand = drawButton.pressed()

    #erasebutton here

    #fill button here
    fillButton = ButtonNotTk(560, 655, 3, "Fill", (255,255,255), colour, 100, 25)
    buttons.append(fillButton)


    #line button here

    pippetteButton = ButtonNotTk(560, 700, 5, "Pippette", (255,255,255), colour, 100, 25)
    buttons.append(pippetteButton)

    running = True
    while running:

        screen.fill((255,255,255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouseDown = False
                #print(drawButton.x, drawButton.y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    red = random.randint(0,255)
                    green = random.randint(0,255)
                    blue = random.randint(0,255)
                    redSlider.circleX = (red*2)+10
                    greenSlider.circleX = (green*2)+10
                    blueSlider.circleX = (blue*2)+10

        if mouseDown:
            #drawButton.x, drawButton.y = pygame.mouse.get_pos()
            LeftButton, MiddleButton, RightButton = pygame.mouse.get_pressed()
            x, y = pygame.mouse.get_pos()
            if y < 600:
                for row in grid:
                    for col in row:
                        if col.x <= x <= col.x + TILE_SIZE and col.y <= y <= col.y + TILE_SIZE:
                            if LeftButton and curCommand == 1:
                                col.curIMG = "This Will Cause An Exception"
                                col.r = red
                                col.g = green
                                col.b = blue
                            elif RightButton and curCommand == 1:
                                col.curIMG = TILE_BLOCK
                            elif LeftButton and curCommand == 3:
                                for row in grid:
                                    for col in row:
                                        col.curIMG = "This will Cause an Exception"
                                        col.r = red
                                        col.g = green
                                        col.b = blue
                            elif LeftButton and curCommand == 5 and col.curIMG == "This Will Cause An Exception":
                                redSlider.circleX = (col.r*2)+10
                                greenSlider.circleX = (col.g*2) + 10
                                blueSlider.circleX = (col.b*2) + 10

            elif 625 <= y <= 655 and 10 <= x <= 520:    # Red Slider
                redSlider.circleX = x
            elif 680 <= y <= 710 and 10 <= x <= 520:     # Green Slider
                greenSlider.circleX = x
            elif 635 <= y <= 765 and 10 <= x <= 520:     # Blue Slider
                blueSlider.circleX = x
            elif y > 600 and x > 520:
                if startofCoolDown + cooldowntime < time.time():
                    pressedButton = -1
                    for btn in buttons:
                        if btn.x <= x <= btn.x + btn.length and btn.y <= y <= btn.y + btn.height:
                            curCommand = btn.pressed()
                            startofCoolDown = time.time()
                            if curCommand != 0:
                                pressedButton = buttons.index(btn)
                                break
                    for x, btn in enumerate(buttons):   #Turn all other buttons off
                        if x != pressedButton:
                            btn.isPressed = False

            if MiddleButton:
                root = Tk()
                def SaveImgPl():
                    SaveImg(grid)
                    root.destroy()
                savebtn = Button(root, text = 'Save', command = SaveImgPl)
                savebtn.grid(column = 0, row = 0)
                def LoadImgPl():
                    global grid
                    grid.clear()
                    grid = LoadImg()
                    root.destroy()
                loadbtn = Button(root, text = 'Load', command = LoadImgPl)
                loadbtn.grid(column = 1, row = 0)
                def newImg():
                    global grid
                    todelete = False
                    response = messagebox.askyesnocancel('New File', 'Do you want to save your current file?')
                    if response:    
                        SaveImg(grid)
                        todelete = True
                    elif response == False:
                        todelete = True
                    elif response == None:
                        todelete = False
                    if todelete:
                        del grid
                        grid = []
                        grid = make_grid()
                    root.destroy()
                newGridBtn = Button(root, text = "New File", command = newImg)
                newGridBtn.grid(column = 2, row = 0)
                root.mainloop()

        red = int((redSlider.circleX - 10)/2)
        green = int((greenSlider.circleX - 10)/2)
        blue = int((blueSlider.circleX - 10)/2)

        del colour
        colour = (red, green, blue)
        drawALL(screen, grid, redSlider, greenSlider, blueSlider, buttons)
        pygame.display.update()

main()
