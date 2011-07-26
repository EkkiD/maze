def main():
    screen = pygame.display.set_mode(size)
    
    clock = pygame.time.Clock()
    
    # initialize the array as a valid grid.
    for i in range(grid_rows):
        for j in range(grid_cols):
            nodes[i][j] = north | east | south | west
            if j == 0:               nodes[i][j] = nodes[i][j] ^ west
            if j == grid_cols - 1:   nodes[i][j] = nodes[i][j] ^ east
            if i == 0:               nodes[i][j] = nodes[i][j] ^ north
            if i == grid_rows - 1:   nodes[i][j] = nodes[i][j] ^ south
     
    while 1:
        clock.tick(1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        screen.fill(black)
        
        DoIteration(screen)
    


def DoIteration(screen): 
    
    #draw the outer border
    border_rect = (base_offset, base_offset, (grid_cols*square_pixels), (grid_rows*square_pixels))
    pygame.draw.rect(screen, grey, border_rect, 2)


    for row in range(grid_rows):
        for col in range(grid_cols):
            off_x = base_offset + col * square_pixels
            off_y = base_offset + row * square_pixels
            if nodes[row][col] & north:
                assert row > 0, "Can't draw north of row 0"
                assert nodes[row-1][col] & south
                pygame.draw.line(screen, grey, (off_x+2, off_y), (off_x+square_pixels-2, off_y), 2)
            if nodes[row][col] & west:
                assert col > 0, "Can't draw west of col 0"
                assert nodes[row][col-1] & east, "Node %d, %d should have 'east' set"  % (row, col)
                pygame.draw.line(screen, grey, (off_x, off_y+2), (off_x, off_y+square_pixels-2), 2)

    pygame.display.flip()



if __name__ == "__main__":
    import sys, pygame

    pygame.init()

    grid_size = grid_rows, grid_cols = 20, 25
    square_pixels = 20
    base_offset = 50

    size = width, height = (2*base_offset)+(grid_cols*square_pixels), (2*base_offset)+(grid_rows*square_pixels)


    black = 0,0,0
    white = 255,255,255
    grey  = 0x6E6D6Da
    
    north = 1
    east = 2
    south = 4
    west = 8

    nodes = [None] * grid_rows
    for i in range(grid_rows):
        nodes[i] = [None] * grid_cols
    
    
    main()
