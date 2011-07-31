import sys, pygame

pygame.init()

grid_size = grid_rows, grid_cols = 20, 25
square_pixels = 20
base_offset = 50

size = width, height = (2*base_offset)+(grid_cols*square_pixels), (2*base_offset)+(grid_rows*square_pixels)

black = 0,0,0
white = 255,255,255
grey  = 0x6E6D6Da

class maze:
    """This class handles all of the maze generation and solving functions.

    Should be treated as a singleton until I figure out this member variable thing.

    Stores the maze as a 2-d array of nodes which store a bitfield to indicate what sides have a wall.
    
    north  = 0x1
    east   = 0x2
    south  = 0x4
    west   = 0x8
    
    For now this class will also take care of rendering the maze. Not sure if this is the best design but we'll use it for now"""

    north = 1
    east = 2
    south = 4
    west = 8
    
    nodes = [None] * grid_rows
    for i in range(grid_rows):
        nodes[i] = [None] * grid_cols

    screen = pygame.display.set_mode(size)
    
    clock = pygame.time.Clock()
    
    def __init__(self):
        
        # initialize the array as a valid grid.
        for i in range(grid_rows):
            for j in range(grid_cols):
                maze.nodes[i][j] = maze.north | maze.east | maze.south | maze.west
                if j == 0:               maze.nodes[i][j] = maze.nodes[i][j] ^ maze.west
                if j == grid_cols - 1:   maze.nodes[i][j] = maze.nodes[i][j] ^ maze.east
                if i == 0:               maze.nodes[i][j] = maze.nodes[i][j] ^ maze.north
                if i == grid_rows - 1:   maze.nodes[i][j] = maze.nodes[i][j] ^ maze.south


    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        maze.DoIteration();
    
            maze.screen.fill(black)
            maze.DrawScreen(self, maze.screen)
            maze.clock.tick(40)
            
    def DoIteration(self):
        global grey
    
    
    def DrawScreen(self, screen): 
        
        #draw the outer border
        border_rect = (base_offset, base_offset, (grid_cols*square_pixels), (grid_rows*square_pixels))
        pygame.draw.rect(screen, grey, border_rect, 2)
    
    
        for row in range(grid_rows):
            for col in range(grid_cols):
                off_x = base_offset + col * square_pixels
                off_y = base_offset + row * square_pixels
                if maze.nodes[row][col] & maze.north:
                    assert row > 0, "Can't draw north of row 0"
                    assert maze.nodes[row-1][col] & maze.south, "Node %d, %d should have 'south' set"  % (row-1, col)
                    pygame.draw.line(screen, grey, (off_x+2, off_y), (off_x+square_pixels-2, off_y), 2)
                if maze.nodes[row][col] & maze.west:
                    assert col > 0, "Can't draw west of col 0"
                    assert maze.nodes[row][col-1] & maze.east, "Node %d, %d should have 'east' set"  % (row, col-1)
                    pygame.draw.line(screen, grey, (off_x, off_y+2), (off_x, off_y+square_pixels-2), 2)
    
        pygame.display.flip()
    


if __name__ == "__main__":
    myMaze = maze()
    myMaze.run()
