#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Game based on tutorials by Al Sweigart in his book 'Making Games with Python
& Pygame"
http://inventwithpython.com/pygame/chapters/
"""

# Importing pygame modules
import random, sys, pygame
from pygame.locals import *

# Set variables, like screen width and height 
# globals
FPS = 30
REVEALSPEED = 8
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TILESIZE = 40
MARKERSIZE = 40
BUTTONHEIGHT = 20
BUTTONWIDTH = 40
TEXT_HEIGHT = 25
TEXT_LEFT_POSN = 10
BOARDWIDTH = 10
BOARDHEIGHT = 10
DISPLAYWIDTH = 200
EXPLOSIONSPEED = 10

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * TILESIZE) - DISPLAYWIDTH - MARKERSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * TILESIZE) - MARKERSIZE) / 2)

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
           COUNTER_RECT, HBUTTON_SURF, EXPLOSION_IMAGES
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 50)
    
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
    
    # Explosion graphics
    EXPLOSION_IMAGES = [
        pygame.image.load("img/blowup1.png"), pygame.image.load("img/blowup2.png"),
        pygame.image.load("img/blowup3.png"),pygame.image.load("img/blowup4.png"),
        pygame.image.load("img/blowup5.png"),pygame.image.load("img/blowup6.png")]
    
    pygame.display.set_caption('Battleship')

    while True:
        shots_taken = run_game()
        show_gameover_screen(shots_taken)
        
        
def run_game():
    revealed_tiles = generate_default_tiles(False)
    # main board object, 
    main_board = generate_default_tiles(None)
    ship_objs = ['battleship','cruiser1','cruiser2','destroyer1','destroyer2',
                 'destroyer3','submarine1','submarine2','submarine3','submarine4']
    main_board = add_ships_to_board(main_board, ship_objs)
    mousex, mousey = 0, 0
    counter = [] # counter to track number of shots fired
    xmarkers, ymarkers = set_markers(main_board)
        
    while True:
        # counter display (it needs to be here in order to refresh it)
        COUNTER_SURF = BASICFONT.render(str(len(counter)), True, WHITE)
        COUNTER_RECT = SHOTS_SURF.get_rect()
        COUNTER_RECT.topleft = (WINDOWWIDTH - 680, WINDOWHEIGHT - 570)
        
        # draw the buttons
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(HELP_SURF, HELP_RECT)
        DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
        DISPLAYSURF.blit(SHOTS_SURF, SHOTS_RECT)
        DISPLAYSURF.blit(COUNTER_SURF, COUNTER_RECT)
        
        draw_board(main_board, revealed_tiles)
        draw_markers(xmarkers, ymarkers)
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
                    left, top = left_top_coords_tile(tilex, tiley)
                    blowup_animation((left, top))
                    if check_for_win(main_board, revealed_tiles):
                        counter.append((tilex, tiley))
                        return len(counter)
                counter.append((tilex, tiley))
                
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generate_default_tiles(default_value):
    '''
    returns list of 10 x 10 tiles with tuples ('shipName',boolShot) set to 
    (default_value)
    '''
    default_tiles = [[default_value]*BOARDHEIGHT for i in xrange(BOARDWIDTH)]
    
    return default_tiles

    
def blowup_animation(coord):
    '''
    coord --> tuple of tile coords to apply the blowup animation
    '''
    for image in EXPLOSION_IMAGES:
        image = pygame.transform.scale(image, (TILESIZE+10, TILESIZE+10))
        DISPLAYSURF.blit(image, coord)
        pygame.display.flip()
        FPSCLOCK.tick(EXPLOSIONSPEED)


def check_revealed_tile(board, tile):
    # returns True if ship piece at tile location
    return board[tile[0][0]][tile[0][1]] != None


def reveal_tile_animation(board, tile_to_reveal):
    '''
    board: list of board tile tuples ('shipName', boolShot)
    tile_to_reveal: tuple of tile coords to apply the reveal animation to
    '''
    for coverage in xrange(TILESIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        draw_tile_covers(board, tile_to_reveal, coverage)

        
def draw_tile_covers(board, tile, coverage):
    '''
    board: list of board tiles
    tile: tuple of tile coords to reveal
    coverage: int
    '''
    left, top = left_top_coords_tile(tile[0][0], tile[0][1])
    if check_revealed_tile(board, tile):
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


def check_for_win(board, revealed):
    # returns True if all the ships were revealed
    for tilex in xrange(BOARDWIDTH):
        for tiley in xrange(BOARDHEIGHT):
            if board[tilex][tiley] != None and not revealed[tilex][tiley]:
                return False
    return True


def draw_board(board, revealed):
    '''
    board: list of board tiles
    revealed: list of revealed tiles
    '''
    for tilex in xrange(BOARDWIDTH):
        for tiley in xrange(BOARDHEIGHT):
            left, top = left_top_coords_tile(tilex, tiley)
            if not revealed[tilex][tiley]:
                pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left, top, TILESIZE,
                                                          TILESIZE))
            else:
                if board[tilex][tiley] != None:
                    pygame.draw.rect(DISPLAYSURF, SHIPCOLOR, (left, top, 
                                     TILESIZE, TILESIZE))
                else:
                    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, 
                                     TILESIZE, TILESIZE))
                
    for x in xrange(0, (BOARDWIDTH + 1) * TILESIZE, TILESIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x + XMARGIN + MARKERSIZE,
            YMARGIN + MARKERSIZE), (x + XMARGIN + MARKERSIZE, 
            WINDOWHEIGHT - YMARGIN))
    for y in xrange(0, (BOARDHEIGHT + 1) * TILESIZE, TILESIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (XMARGIN + MARKERSIZE, y + 
            YMARGIN + MARKERSIZE), (WINDOWWIDTH - (DISPLAYWIDTH + MARKERSIZE *
            2), y + YMARGIN + MARKERSIZE))





def set_markers(board):
    '''
    returns 2 lists of markers with number of ship pieces in each row (xmarkers)
        and column (ymarkers)
    board: list of board tiles
    '''

    xmarkers = [0 for i in xrange(BOARDWIDTH)]
    ymarkers = [0 for i in xrange(BOARDHEIGHT)]
    for tilex in xrange(BOARDWIDTH):
        for tiley in xrange(BOARDHEIGHT):
            if board[tilex][tiley] != None:
                xmarkers[tilex] += 1
                ymarkers[tiley] += 1

    return xmarkers, ymarkers


def draw_markers(xlist, ylist):
    '''
    xlist: list of row markers
    ylist: list of column markers
    '''
    for i in xrange(len(xlist)):
        left = i * MARKERSIZE + XMARGIN + MARKERSIZE + (TILESIZE / 3)
        top = YMARGIN
        marker_surf, marker_rect = make_text_objs(str(xlist[i]),
                                                    BASICFONT, TEXTCOLOR)
        marker_rect.topleft = (left, top)
        DISPLAYSURF.blit(marker_surf, marker_rect)
    for i in range(len(ylist)):
        left = XMARGIN
        top = i * MARKERSIZE + YMARGIN + MARKERSIZE + (TILESIZE / 3)
        marker_surf, marker_rect = make_text_objs(str(ylist[i]), 
                                                    BASICFONT, TEXTCOLOR)
        marker_rect.topleft = (left, top)
        DISPLAYSURF.blit(marker_surf, marker_rect)



def add_ships_to_board(board, ships):
    '''
    return list of board tiles with ships placed on certain tiles
    board: list of board tiles
    ships: list of ships to place on board
    '''
    new_board = board[:]
    ship_length = 0
    for ship in ships:
        valid_ship_position = False
        while not valid_ship_position:
            xStartpos = random.randint(0, 9)
            yStartpos = random.randint(0, 9)
            isHorizontal = random.randint(0, 1)
            if 'battleship' in ship:
                ship_length = 4
            elif 'cruiser' in ship:
                ship_length = 3
            elif 'destroyer'in ship:
                ship_length = 2
            elif 'submarine' in ship:
                ship_length = 1

            valid_ship_position, ship_coords = make_ship_position(new_board,
                xStartpos, yStartpos, isHorizontal, ship_length, ship)
            if valid_ship_position:
                for coord in ship_coords:
                    new_board[coord[0]][coord[1]] = ship
    return new_board


def make_ship_position(board, xPos, yPos, isHorizontal, length, ship):
    '''
    returns tuple: True if ship position is valid and list ship coordinates
    board: list of board tiles
    xPos: x-coordinate of first ship piece
    yPos: y-coordinate of first ship piece
    isHorizontal: True if ship is horizontal
    length: length of ship
    '''
    ship_coordinates = []
    if isHorizontal:
        for i in xrange(length):
            if (i+xPos > 9) or (board[i+xPos][yPos] != None) or \
                hasAdjacent(board, i+xPos, yPos, ship):
                return (False, ship_coordinates)
            else:
                ship_coordinates.append((i+xPos, yPos))
    else:
        for i in xrange(length):
            if (i+yPos > 9) or (board[xPos][i+yPos] != None) or \
                hasAdjacent(board, xPos, i+yPos, ship):
                return (False, ship_coordinates)        
            else:
                ship_coordinates.append((xPos, i+yPos))
    return (True, ship_coordinates)


def hasAdjacent(board, xPos, yPos, ship):
    for x in xrange(xPos-1,xPos+2):
        for y in xrange(yPos-1,yPos+2):
            if (x in range (10)) and (y in range (10)) and \
                (board[x][y] not in (ship, None)):
                return True
    return False
    
    
def left_top_coords_tile(tilex, tiley):
    '''
    returns left and top pixel coords
    tilex: int
    tiley: int
    return: tuple (int, int)
    '''
    left = tilex * TILESIZE + XMARGIN + MARKERSIZE
    top = tiley * TILESIZE + YMARGIN + MARKERSIZE
    return (left, top)
    
    
def get_tile_at_pixel(x, y):
    '''
    returns tile coordinates of pixel at top left, defaults to (None, None)
    x: int
    y: int
    return: tuple (tilex, tiley)
    '''
    for tilex in xrange(BOARDWIDTH):
        for tiley in xrange(BOARDHEIGHT):
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
    
    line2_surf, line2_rect = make_text_objs(
        'This is a battleship puzzle game. Your objective is ' \
        'to sink all the ships in as few', BASICFONT, TEXTCOLOR)
    line2_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 3)
    DISPLAYSURF.blit(line2_surf, line2_rect)

    line3_surf, line3_rect = make_text_objs('shots as possible. The markers on'\
        ' the edges of the game board tell you how', BASICFONT, TEXTCOLOR)
    line3_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 4)
    DISPLAYSURF.blit(line3_surf, line3_rect)

    line4_surf, line4_rect = make_text_objs('many ship pieces are in each'\
        ' column and row. To reset your game click on', BASICFONT, TEXTCOLOR)
    line4_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 5)
    DISPLAYSURF.blit(line4_surf, line4_rect)

    line5_surf, line5_rect = make_text_objs('the "New Game" button.',
        BASICFONT, TEXTCOLOR)
    line5_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 6)
    DISPLAYSURF.blit(line5_surf, line5_rect)
    
    while check_for_keypress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

        
def check_for_keypress():
    # pulling out all KEYDOWN and KEYUP events from queue and returning any 
    # KEYUP else return None
    for event in pygame.event.get([KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]):
        if event.type in (KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION):
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


def show_gameover_screen(shots_fired):
    '''
    text: string
    '''
    DISPLAYSURF.fill(BGCOLOR)
    titleSurf, titleRect = make_text_objs('Congrats! Puzzle solved in:',
                                            BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    titleSurf, titleRect = make_text_objs('Congrats! Puzzle solved in:', 
                                            BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    titleSurf, titleRect = make_text_objs(str(shots_fired) + ' shots', 
                                            BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2 + 50))
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    titleSurf, titleRect = make_text_objs(str(shots_fired) + ' shots', 
                                            BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2 + 50) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = make_text_objs(
        'Press a key to try to beat that score.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    
    while check_for_keypress() == None:
        pygame.display.update()
        FPSCLOCK.tick()    
        
    
if __name__ == "__main__": #This calls the game loop
    main()
