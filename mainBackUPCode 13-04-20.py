import pygame
import os
import pickle
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
import random

pygame.init()

SCREENX = 1000
SCREENY = 770

TILE_SIZE = 20
TILE_BLOCK = pygame.image.load(os.path.join('Sprites', 'Transparent.png'))
TestBLOCK = pygame.image.load(os.path.join('Sprites', 'Test.png'))

COLOUR_FONT = pygame.font.SysFont('Comicsans', 30)

def SaveImg(grid):
    for row in grid:
        for col in row:
            if col.curIMG == TILE_BLOCK:
                col.curIMG = None

    root = Tk()
    root.withdraw()
    root.filename = filedialog.asksaveasfile(mode = "w")
    pickle_out = open(root.filename.name, "wb")
    pickle.dump(grid, pickle_out)
    pickle_out.close()
    ConvertBack(grid)
    messagebox.showinfo('Save', 'Saved Sucessfully')
    root.destroy()

def LoadImg():

    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfile(mode = "r")
    name = root.filename.name

    pickle_in = open(name, "rb")
    grid = []
    grid = pickle.load(pickle_in)

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

def make_grid():
    final_grid = []
    for y in range(0, SCREENY - 150, TILE_SIZE):
        placeholder = []
        for x in range(0, SCREENX, TILE_SIZE):
            placeholder.append(Tile(x, y))
        final_grid.append(placeholder)
        del placeholder

    return final_grid

def drawALL(screen, grid, redSlider, greenSlider, blueSlider):
    for row in grid:
        for col in row:
            col.draw(screen)

    pygame.draw.line(screen, (0,0,0), (0, 600), (1000, 600), 1)

    redSlider.draw(screen)
    greenSlider.draw(screen)
    blueSlider.draw(screen)
    pygame.draw.rect(screen, colour, (530, 650, 20, 20))

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

        if mouseDown:
            LeftButton, MiddleButton, RightButton = pygame.mouse.get_pressed()
            x, y = pygame.mouse.get_pos()
            if y < 600:
                for row in grid:
                    for col in row:
                        if col.x <= x <= col.x + 20 and col.y <= y <= col.y + 20:
                            if LeftButton:
                                col.curIMG = "This Will Cause An Exception"
                                col.r = red
                                col.g = green
                                col.b = blue
                            elif RightButton:
                                col.curIMG = TILE_BLOCK
            elif 625 <= y <= 655 and 10 <= x <= 520:    # Red Slider
                redSlider.circleX = x
            elif 680 <= y <= 710 and 10 <= x <= 520:     # Green Slider
                greenSlider.circleX = x
            elif 635 <= y <= 765 and 10 <= x <= 520:     # Blue Slider
                blueSlider.circleX = x
            
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
                root.mainloop()

        red = int((redSlider.circleX - 10)/2)
        green = int((greenSlider.circleX - 10)/2)
        blue = int((blueSlider.circleX - 10)/2)

        del colour
        colour = (red, green, blue)
        drawALL(screen, grid, redSlider, greenSlider, blueSlider)
        pygame.display.update()

main()
