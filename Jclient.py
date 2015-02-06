import socket
import pygame
import time

#computes and draws the stuff that appears on screen.
def Jodclient(IP, port):
    input_string = ""
    output_string = ""
    IPlink = socket.socket()
    IPlink.connect((IP, port))

    #define pygame values
    BOARD = 11 #this value is the x,y amount of tiles for the board.
    SQUARE = 12
    SCREEN = (SQUARE * BOARD)

    #initialise screen
    pygame.init()
    WINDOW = pygame.display.set_mode((SCREEN, SCREEN))
    image = pygame.image.load("Alloy_curses_12x12.png")
    pastel = pygame.Surface(image.get_size(), depth=24)
    key = (255, 0, 255)
    pastel.fill(key)
    pastel.set_colorkey(key)
    pastel.blit(image, (0, 0))
    pygame.display.set_caption("Test program")
    SURFACE = pygame.display.get_surface()

    #define local functions
    def draw(data, surf, rect, screen_size, pastl):
        #cleans screen
        pygame.draw.rect(surf, (0, 0, 0), (0, 0 , screen_size, screen_size))
        length = len(data)
        i = 0

        x = 0
        y = 0
        while (i < length):
            if (data[i] == "n"):
                x = 0
                y += 1
            else:
                if (data[i] == "."):
                    surf.blit(pastl, (x*rect, y*rect), (14*rect, 2*rect, rect, rect))
                elif (data[i] == "#"):
                    surf.blit(pastl, (x*rect, y*rect), (3*rect, 2*rect, rect, rect))
                elif (data[i] == "@"):
                    surf.blit(pastl, (x*rect, y*rect), (0, 4*rect, rect, rect))
                x += 1
            i += 1

        pygame.display.flip()

    #event loop
    input_string = "."
    IPlink.send(input_string + "\n")
    output_string = IPlink.recv(4096)
    draw(output_string, SURFACE, SQUARE, SCREEN, pastel)

    while 1:
        key=pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                IPlink.send("I quit\n")
                return
            if key[pygame.K_UP]: input_string = "up"
            if key[pygame.K_DOWN]: input_string = "down"
            if key[pygame.K_LEFT]: input_string = "left"
            if key[pygame.K_RIGHT]: input_string = "right"
    
            print "input is now", input_string

            if (not input_string == ""):
                IPlink.send(input_string + "\n")
                output_string = IPlink.recv(4096)
                draw(output_string, SURFACE, SQUARE, SCREEN, pastel)

            input_string = ""

    IPlink.close()


Jodclient("127.0.0.1", 6789) #127.0.0.1 == localhost, change if needed
