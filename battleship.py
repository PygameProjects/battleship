#!/usr/bin/env python
# -*- coding: utf-8 -*-

#THIS IS PROJECT ONE, WE'LL FIRST TRY TO MAKE A BATTLESHIP GAME,
#PLEASE MAKE USE OF COMMENT WHEN PULLING REQUESTS


# Importing pygame modules
import random, sys, pygame
from pygame.locals import *
# and other modules needed

# ----------------------------------------------
# Set variables, like screen width and height 
# globals
FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TILESIZE = 40
BUTTONHEIGHT = 20
BUTTONWIDTH = 40
TEXT_HEIGHT = 25
TEXT_LEFT_POSN = 10
BOARDWIDTH = 12
BOARDHEIGHT = 12
DISPLAYWIDTH = 200
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * TILESIZE) - (DISPLAYWIDTH + 20)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * TILESIZE)) / 2)

BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
GREEN   = (  0, 204,   0)
GRAY    = ( 60,  60,  60)
BLUE    = (  0,  50, 255)
YELLOW  = (255, 255,   0)
DARKGRAY =( 40,  40,  40)

BGCOLOR = GRAY
BUTTONCOLOR = GREEN
TEXTCOLOR = WHITE
TILECOLOR = GREEN
BORDERCOLOR = BLUE
TEXTSHADOWCOLOR = BLUE
SHIPCOLOR = YELLOW


def main():
    global DISPLAYSURF, FPSCLOCK, BASICFONT, HELP_SURF, HELP_RECT, NEW_SURF, \
           NEW_RECT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    
    # create buttons
    HELP_SURF = BASICFONT.render("HELP", True, WHITE, GREEN)
    HELP_RECT = HELP_SURF.get_rect()
    HELP_RECT.topleft = (WINDOWWIDTH - 120, WINDOWHEIGHT - 593)
    NEW_SURF = BASICFONT.render("NEW GAME", True, WHITE, GREEN)
    NEW_RECT = NEW_SURF.get_rect()
    NEW_RECT.topleft = (WINDOWWIDTH - 120, WINDOWHEIGHT - 563)
    
    pygame.display.set_caption('Battleship')

    while True:
        run_game()
        show_text_screen('Game Over')
        
        
def run_game():
    revealed_boxes = generate_revealed_boxes(False)
    
    while True:
        DISPLAYSURF.fill(BGCOLOR)        
        DISPLAYSURF.blit(HELP_SURF, HELP_RECT)
        DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
        draw_board(revealed_boxes)

        check_for_quit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                #print (event.pos[0], event.pos[1])
                if HELP_RECT.collidepoint(event.pos):
                    DISPLAYSURF.fill(BGCOLOR)
                    show_help_screen()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        
def generate_revealed_boxes(val):
    revealed_boxes = []
    for i in range(BOARDWIDTH):
        revealed_boxes.append([val] * BOARDHEIGHT)
    return revealed_boxes
    
    
def check_for_quit():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()


def draw_board(revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = left_top_coords_box(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left, top, TILESIZE, TILESIZE))
            else:
                pygame.draw.rect(DISPLAYSURF, SHIPCOLOR, (left, top, TILESIZE, TILESIZE))
                
    for x in range(0, BOARDWIDTH * TILESIZE, TILESIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x + XMARGIN, YMARGIN), (x + XMARGIN, WINDOWHEIGHT - YMARGIN))
    for y in range(0, BOARDHEIGHT * TILESIZE, TILESIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (XMARGIN, y + YMARGIN), (WINDOWWIDTH - (DISPLAYWIDTH + 20 + XMARGIN), y + YMARGIN))

        
def left_top_coords_box(boxx, boxy):
    left = boxx * TILESIZE + XMARGIN
    top = boxy * TILESIZE + YMARGIN
    return (left, top)
 
 
def show_help_screen():
    # display the help screen until a button is pressed
    line1_surf, line1_rect = make_text_objs('Press a key to exit.', BASICFONT,
                                            TEXTCOLOR)
    line1_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT)
    DISPLAYSURF.blit(line1_surf, line1_rect)
    
    line2_surf, line2_rect = make_text_objs('Enter instructions here.', 
                                            BASICFONT, TEXTCOLOR)
    line2_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 2)
    DISPLAYSURF.blit(line2_surf, line2_rect)

    line3_surf, line3_rect = make_text_objs('Enter instructions here.', 
                                            BASICFONT, TEXTCOLOR)
    line3_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 3)
    DISPLAYSURF.blit(line3_surf, line3_rect)

    while check_for_keypress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

        
def check_for_keypress():
    # pulling out all KEYDOWN and KEYUP events from queue and returning any 
    # KEYUP else return None
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None
    
        
def make_text_objs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def show_text_screen(text):
    DISPLAYSURF.fill(BGCOLOR)
    titleSurf, titleRect = make_text_objs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    titleSurf, titleRect = make_text_objs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    pressKeySurf, pressKeyRect = make_text_objs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    
    while check_for_keypress() == None:
        pygame.display.update()
        FPSCLOCK.tick()    

        
    
if __name__ == "__main__": #This calls the game loop
    main()
