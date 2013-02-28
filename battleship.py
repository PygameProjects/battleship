#!/usr/bin/env python
# -*- coding: utf-8 -*-
#THIS IS PROJECT ONE, WE'LL FIRST TRY TO MAKE A BATTLESHIP GAME,
#PLEASE MAKE USE OF COMMENT WHEN PULLING REQUESTS


# Importing pygame modules
import random, sys, pygame
from pygame.locals import *
# and other modules needed

# Set variables, like screen width and height 
# globals
FPS = 30
REVEALSPEED = 8
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
COUNTER = []

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
HIGHLIGHTCOLOR = BLUE


def main():
    global DISPLAYSURF, FPSCLOCK, BASICFONT, HELP_SURF, HELP_RECT, NEW_SURF, \
           NEW_RECT, SHOTS_SURF, SHOTS_RECT, BIGFONT, COUNTER, COUNTER_SURF, \
           COUNTER_RECT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    
    # create buttons
    HELP_SURF = BASICFONT.render("HELP", True, WHITE)
    HELP_RECT = HELP_SURF.get_rect()
    HELP_RECT.topleft = (WINDOWWIDTH - 180, WINDOWHEIGHT - 350)
    NEW_SURF = BASICFONT.render("NEW GAME", True, WHITE)
    NEW_RECT = NEW_SURF.get_rect()
    NEW_RECT.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 200)

    # 'Shots:' label
    SHOTS_SURF = BASICFONT.render("Shots: ", True, WHITE)
    SHOTS_RECT = SHOTS_SURF.get_rect()
    SHOTS_RECT.topleft = (WINDOWWIDTH - 750, WINDOWHEIGHT - 570)
    
    pygame.display.set_caption('Battleship')

    while True:
        run_game()
        show_text_screen('Game Over')
        
        
def run_game():
    revealed_tiles = generate_default_tiles()
    main_board = generate_default_tiles()
    add_ships_to_board(main_board)
    mousex, mousey = 0, 0

    
    while True:
        # counter display (it needs to be here in order to refresh it)
        COUNTER_SURF = BASICFONT.render(str(len(COUNTER)), True, WHITE)
        COUNTER_RECT = SHOTS_SURF.get_rect()
        COUNTER_RECT.topleft = (WINDOWWIDTH - 680, WINDOWHEIGHT - 570)
        # end of the counter
        DISPLAYSURF.fill(BGCOLOR)        
        DISPLAYSURF.blit(HELP_SURF, HELP_RECT)
        DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
        DISPLAYSURF.blit(SHOTS_SURF, SHOTS_RECT)
        DISPLAYSURF.blit(COUNTER_SURF, COUNTER_RECT)
        draw_board(main_board, revealed_tiles)
        mouse_clicked = False 
    

        check_for_quit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                #print (event.pos[0], event.pos[1])
                if HELP_RECT.collidepoint(event.pos):
                    DISPLAYSURF.fill(BGCOLOR)
                    show_help_screen()
                elif NEW_RECT.collidepoint(event.pos):
                    restart_game()
                else:
                    mousex, mousey = event.pos
                    mouse_clicked = True
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                    
        tilex, tiley = get_tile_at_pixel(mousex, mousey)
        if tilex != None and tiley != None:
            if not revealed_tiles[tilex][tiley]:
                draw_highlight_tile(tilex, tiley)
            if not revealed_tiles[tilex][tiley] and mouse_clicked:
                reveal_tiles_animation(main_board, [(tilex, tiley)])
                revealed_tiles[tilex][tiley] = True
                add_shot('y')
                
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def add_shot(x):
    # adds a shot to the COUNTER
    if x == 'y':
        COUNTER.append('shot')    
    
        
def generate_default_tiles():
    default_tiles = []
    for i in range(BOARDWIDTH):
        default_tiles.append([False] * BOARDHEIGHT)
    return default_tiles

    
def reveal_tiles_animation(board, tiles_to_reveal):
    for coverage in range(TILESIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        draw_tile_covers(board, tiles_to_reveal, coverage)

        
def draw_tile_covers(board, tiles, coverage):
    for tile in tiles:
        left, top = left_top_coords_tile(tile[0], tile[1])
        if board[tile[0]][tile[1]] == True:
            pygame.draw.rect(DISPLAYSURF, SHIPCOLOR, (left, top, TILESIZE,
                                                      TILESIZE))
        else:
            pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, TILESIZE, 
                                                    TILESIZE))
        if coverage > 0:
            pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left, top, coverage, 
                                                      TILESIZE))
            
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    

def check_for_quit():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()


def draw_board(board, revealed):
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            left, top = left_top_coords_tile(tilex, tiley)
            if not revealed[tilex][tiley]:
                pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left, top, TILESIZE,
                                                          TILESIZE))
            else:
                if board[tilex][tiley] == True:
                    pygame.draw.rect(DISPLAYSURF, SHIPCOLOR, (left, top, 
                                     TILESIZE, TILESIZE))
                else:
                    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, 
                                     TILESIZE, TILESIZE))
                
    for x in range(0, BOARDWIDTH * TILESIZE, TILESIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x + XMARGIN, YMARGIN), \
                        (x + XMARGIN, WINDOWHEIGHT - YMARGIN))
    for y in range(0, BOARDHEIGHT * TILESIZE, TILESIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (XMARGIN, y + YMARGIN), \
                (WINDOWWIDTH - (DISPLAYWIDTH + 20 + XMARGIN), y + YMARGIN))
        

def add_ships_to_board(board):
    # this is a stub for the prototype only. needs to be refactored for next
    # milestone
    new_board = board
    board[1][1] = True
    board[1][2] = True
    board[1][8] = True
    board[2][8] = True
    board[3][8] = True
    board[5][8] = True

        
def left_top_coords_tile(tilex, tiley):
    left = tilex * TILESIZE + XMARGIN
    top = tiley * TILESIZE + YMARGIN
    return (left, top)
    
    
def get_tile_at_pixel(x, y):
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            left, top = left_top_coords_tile(tilex, tiley)
            tile_rect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tile_rect.collidepoint(x, y):
                return (tilex, tiley)
    return (None, None)
    
    
def draw_highlight_tile(tilex, tiley):
    left, top = left_top_coords_tile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR,
                    (left, top, TILESIZE, TILESIZE), 4)


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


def restart_game():
    del COUNTER[:]
    main()

        
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
    
    pressKeySurf, pressKeyRect = make_text_objs('Press a key to play.', 
                                                BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    
    while check_for_keypress() == None:
        pygame.display.update()
        FPSCLOCK.tick()    

        
    
if __name__ == "__main__": #This calls the game loop
    main()
