import sys, pygame

pygame.init()

size = width, height = 720, 620
speed = [2, 2]
black = 0,0,0
white = 255,255,255
grey  = 0x6E6D6D

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

while 1:
    clock.tick(1000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.fill(black)
    
    pygame.draw.line(screen, grey, (0, 0), (100, 100), 4)
    

    pygame.display.flip()
