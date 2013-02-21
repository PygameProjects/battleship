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
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
TILESIDE = 80
BUTTONHEIGHT = 20
BUTTONWIDTH = 40
BASICFONTSIZE = 20
TEXT_HEIGHT = 25
TEXT_LEFT_POSN = 10

BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
GREEN   = (  0, 204,   0)
GRAY    = ( 60,  60,  60)

BGCOLOR = GRAY
BUTTONCOLOR = GREEN
TEXTCOLOR = WHITE


def main():
    global DISPLAYSURF, FPSCLOCK, BASICFONT, HELP_SURF, HELP_RECT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    HELP_SURF = BASICFONT.render("HELP", True, WHITE, GREEN)
    HELP_RECT = HELP_SURF.get_rect()
    HELP_RECT.topleft = (WINDOWWIDTH - 60, WINDOWHEIGHT - 473)
    pygame.display.set_caption('Battleship')

    while True:
        check_for_quit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                #print (event.pos[0], event.pos[1])
                if HELP_RECT.collidepoint(event.pos):
                    DISPLAYSURF.fill(BGCOLOR)
                    show_help_screen()
        DISPLAYSURF.fill(BGCOLOR)        
        DISPLAYSURF.blit(HELP_SURF, HELP_RECT)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        
def check_for_quit():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
        
        
def show_help_screen():
    # display the help screen until a button is pressed
    line1_surf, line1_rect = make_text_objs('Press a key to exit.', BASICFONT, TEXTCOLOR)
    line1_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT)
    DISPLAYSURF.blit(line1_surf, line1_rect)
    
    line2_surf, line2_rect = make_text_objs('Enter instructions here.', BASICFONT, TEXTCOLOR)
    line2_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 2)
    DISPLAYSURF.blit(line2_surf, line2_rect)

    line3_surf, line3_rect = make_text_objs('Enter instructions here.', BASICFONT, TEXTCOLOR)
    line3_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 3)
    DISPLAYSURF.blit(line3_surf, line3_rect)

    while check_for_keypress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

        
def check_for_keypress():
    # pulling out all KEYDOWN and KEYUP events from queue and returning any KEYUP else
    # return None
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None
    
    
def make_text_objs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

    
    
if __name__ == "__main__": #This calls the game loop
    main()
