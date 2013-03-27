#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing pygame modules
import random, sys, pygame
from pygame.locals import *
from explosion import Blowup

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
BOARDWIDTH = 10
BOARDHEIGHT = 10
DISPLAYWIDTH = 200
BUTTONRADIUS = 40
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
HIGHLIGHTCOLOR = BLUE


def main():
    global DISPLAYSURF, FPSCLOCK, BASICFONT, HELP_SURF, HELP_RECT, NEW_SURF, \
           NEW_RECT, SHOTS_SURF, SHOTS_RECT, BIGFONT, COUNTER_SURF, \
           COUNTER_RECT, HBUTTON_SURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    
    # create buttons
    HELP_SURF = BASICFONT.render("HELP", True, WHITE)
    HELP_RECT = HELP_SURF.get_rect()
    HELP_RECT.topleft = (WINDOWWIDTH - 180, WINDOWHEIGHT - 350)
    HBUTTON_SURF = pygame.draw.circle(DISPLAYSURF, GREEN, HELP_RECT.topleft, BUTTONRADIUS)
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
    revealed_tiles = generate_default_tiles(False)
    main_board = generate_default_tiles((None, None))
    ship_objs = make_ships() # list of ships to be used, holds list of tuples
                             # of coords
    main_board = add_ships_to_board(main_board, ship_objs)
    mousex, mousey = 0, 0
    counter = [] # counter to track number of shots fired
        
    while True:
        # counter display (it needs to be here in order to refresh it)
        COUNTER_SURF = BASICFONT.render(str(len(counter)), True, WHITE)
        COUNTER_RECT = SHOTS_SURF.get_rect()
        COUNTER_RECT.topleft = (WINDOWWIDTH - 680, WINDOWHEIGHT - 570)
        # end of the counter
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(HBUTTON_SURF)
        #pygame.draw.circle(DISPLAYSURF, GREEN, (WINDOWWIDTH - 180, WINDOWHEIGHT - 350), BUTTONRADIUS)
        DISPLAYSURF.blit(HELP_SURF, HELP_RECT)
        DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
        DISPLAYSURF.blit(SHOTS_SURF, SHOTS_RECT)
        DISPLAYSURF.blit(COUNTER_SURF, COUNTER_RECT)
        draw_board(main_board, revealed_tiles)
        mouse_clicked = False     

        check_for_quit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if HELP_RECT.collidepoint(event.pos):
                    DISPLAYSURF.fill(BGCOLOR)
                    show_help_screen()
                elif NEW_RECT.collidepoint(event.pos):
                    main()
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
                reveal_tile_animation(main_board, [(tilex, tiley)])
                revealed_tiles[tilex][tiley] = True
                if check_revealed_tile(main_board, [(tilex, tiley)]):
                if main_board[tile_to_reveal[0][0]][tile_to_reveal[0][1]] != (None, None):
                    blowup_animation((left, top))
                counter.append((tilex, tiley))
                
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generate_default_tiles(default_value):
    '''
    returns list of 10 x 10 tiles set to False
    '''
    default_tiles = []
    for i in range(BOARDWIDTH):
        default_tiles.append([default_value] * BOARDHEIGHT)
    return default_tiles

    
def blowup_animation(coord):
	'''
	coord --> tuple of tile coords to apply the blowup animation
	'''
	ex = Blowup()	
	ex.is_going_on = True
	while ex.is_going_on:
		ex.update()
		ex.image = pygame.transform.scale(ex.image, (TILESIZE+10,TILESIZE+10))
		DISPLAYSURF.blit(ex.image,coord)
		pygame.display.flip()
		FPSCLOCK.tick(10)


def check_revealed_tile(board, tile_to_check):
    if board[tile_to_reveal[0][0]][tile_to_reveal[0][1]] != (None, None):
        
        
def reveal_tile_animation(board, tile_to_reveal):
    '''
    board: list of board tiles
    tile_to_reveal: tuple of tile coords to apply the reveal animation to
    '''
    left, top = left_top_coords_tile(tile_to_reveal[0][0], tile_to_reveal[0][1])
    if board[tile_to_reveal[0][0]][tile_to_reveal[0][1]] != (None, None):
    	blowup_animation((left,top))
        pygame.draw.rect(DISPLAYSURF, SHIPCOLOR, (left, top, TILESIZE,
                                                  TILESIZE))
    else:
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, TILESIZE, 
                                                TILESIZE))
    
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    

def check_for_quit():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()


def draw_board(board, revealed):
    '''
    board: list of board tiles
    revealed: list of revealed tiles
    '''
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            left, top = left_top_coords_tile(tilex, tiley)
            if not revealed[tilex][tiley]:
                pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left, top, TILESIZE,
                                                          TILESIZE))
            else:
                if board[tilex][tiley] != (None, None):
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


def make_ships():
    '''
    returns list of tuples of ships, each section of a ship has
    the tuple (ship name, shot)
    '''
    slist = []
    # make battleship
    ship = []
    for i in range(4):
        ship.append(('battleship',False))
    slist.append(ship)    
    # make destroyer
    ship = []
    for i in range(3):
        ship.append(('destroyer',False))
    slist.append(ship)
    # make submarine
    ship = []
    for i in range(3):
        ship.append(('submarine',False))
    slist.append(ship)
    
    return slist
                

def add_ships_to_board(board, ships):
    '''
    return list of board tiles with ships placed on certain tiles
    board: list of board tiles
    ships: list of ships (name, bool) to place on board
    '''
    new_board = board[:]
    for ship in ships:
        for i in range(len(ship)):
            if ship[i][0] == 'battleship':
                new_board[1][1+i] = ship[i]
            elif ship[i][0] == 'destroyer':
                new_board[3][2+i] = ship[i]
            elif ship[i][0] == 'submarine':
                new_board[3+i][8] = ship[i]
    return new_board

        
def left_top_coords_tile(tilex, tiley):
    '''
    returns left and top pixel coords
    tilex: int
    tiley: int
    return: tuple (int, int)
    '''
    left = tilex * TILESIZE + XMARGIN
    top = tiley * TILESIZE + YMARGIN
    return (left, top)
    
    
def get_tile_at_pixel(x, y):
    '''
    returns tile coordinates of pixel at top left, defaults to (None, None)
    x: int
    y: int
    return: tuple (tilex, tiley)
    '''
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            left, top = left_top_coords_tile(tilex, tiley)
            tile_rect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tile_rect.collidepoint(x, y):
                return (tilex, tiley)
    return (None, None)
    
    
def draw_highlight_tile(tilex, tiley):
    '''
    tilex: int
    tiley: int
    '''
    left, top = left_top_coords_tile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR,
                    (left, top, TILESIZE, TILESIZE), 4)


def show_help_screen():
    # display the help screen until a button is pressed
    line1_surf, line1_rect = make_text_objs('Press a key to return to the game', 
                                            BASICFONT, TEXTCOLOR)
    line1_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT)
    DISPLAYSURF.blit(line1_surf, line1_rect)
    
    line2_surf, line2_rect = make_text_objs('This is the classic game of ' \
                                            'battleship. Your objective is ' \
                                            'to sink as many ships', 
                                            BASICFONT, TEXTCOLOR)
    line2_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 3)
    DISPLAYSURF.blit(line2_surf, line2_rect)

    line3_surf, line3_rect = make_text_objs('as possible using only 20 shots.', 
                                            BASICFONT, TEXTCOLOR)
    line3_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 4)
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
    '''
    text: string
    font: Font object
    color: tuple of color (red, green blue)
    return: surface object, rectangle object
    '''
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def show_text_screen(text):
    '''
    text: string
    '''
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
