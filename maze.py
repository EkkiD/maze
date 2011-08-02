import sys, pygame
from collections import deque
import random

pygame.init()

grid_size = grid_rows, grid_cols = 20, 25
square_pixels = 20
base_offset = 50

size = width, height = (2*base_offset)+(grid_cols*square_pixels), (2*base_offset)+(grid_rows*square_pixels)

black = 0,0,0
white = 255,255,255
grey  = 0x6E6D6Da
green = 0x008000
    

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
       
    screen = pygame.display.set_mode(size)
    
    clock = pygame.time.Clock()
    
    def __init__(self):
        self.nodes = [None] * grid_rows
        for i in range(grid_rows):
            self.nodes[i] = [None] * grid_cols

        # initialize the array as a valid grid.
        for i in range(grid_rows):
            for j in range(grid_cols):
                self.nodes[i][j] = self.north | self.east | self.south | self.west
                if j == 0:               self.nodes[i][j] = self.nodes[i][j] ^ self.west
                if j == grid_cols - 1:   self.nodes[i][j] = self.nodes[i][j] ^ self.east
                if i == 0:               self.nodes[i][j] = self.nodes[i][j] ^ self.north
                if i == grid_rows - 1:   self.nodes[i][j] = self.nodes[i][j] ^ self.south

        
        self.cellStack = deque()
        self.cellStack.append((0,0))


    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.DoIteration();
    
            self.screen.fill(black)
            self.DrawScreen(maze.screen)
            self.clock.tick(40)
            
    def DoIteration(self):
        self.DFSGenerate()     
    
    
    def DrawScreen(self, screen): 
        
        #draw the outer border
        border_rect = (base_offset, base_offset, (grid_cols*square_pixels), (grid_rows*square_pixels))
        pygame.draw.rect(screen, grey, border_rect, 2)
    
    
        for row in range(grid_rows):
            for col in range(grid_cols):
                off_x = base_offset + col * square_pixels
                off_y = base_offset + row * square_pixels
                if self.nodes[row][col] & self.north:
                    assert row > 0, "Can't draw north of row 0"
                    assert self.nodes[row-1][col] & self.south, "Node %d, %d should have 'south' set"  % (row-1, col)
                    pygame.draw.line(screen, grey, (off_x+2, off_y), (off_x+square_pixels-2, off_y), 2)
                if self.nodes[row][col] & self.west:
                    assert col > 0, "Can't draw west of col 0"
                    assert self.nodes[row][col-1] & self.east, "Node %d, %d should have 'east' set"  % (row, col-1)
                    pygame.draw.line(screen, grey, (off_x, off_y+2), (off_x, off_y+square_pixels-2), 2)

        for node in self.cellStack:
            col = node[0]
            row = node[1]
            off_x = base_offset + col * square_pixels
            off_y = base_offset + row * square_pixels
            rect = (off_x+4, off_y+4,  square_pixels - 6, square_pixels - 6)
            pygame.draw.rect(screen, green, rect)

    
        pygame.display.flip()


    def DFSGenerate(self):
        neighbors = []
        try:
            while True:  
                top = self.cellStack.pop()
                row = top[0] 
                col = top[1]
                if (self.nodes[row][col] & self.north) and self.CheckCellForWalls(row-1, col):
                    neighbors.append(self.north)

                if (self.nodes[row][col] & self.south) and self.CheckCellForWalls(row+1, col):
                    neighbors.append(self.south)

                if (self.nodes[row][col] & self.west) and self.CheckCellForWalls(row, col-1):
                    neighbors.append(self.west)

                if (self.nodes[row][col] & self.east) and self.CheckCellForWalls(row, col+1):
                    neighbors.append(self.east)

                if(neighbors.__len__() == 0):
                    continue

                index = randint(0,neighbors.__len__()-1)
                direction = neighbors[index]
                if(direction & self.north):
                    assert self.nodes[row-1][col] & self.south, "Node %d, %d should have 'south' set"  % (row-1, col)
                    self.nodes[row-1][col] ^ self.south
                    self.nodes[row][col] ^ self.north
                    new_loc = (row-1, col)

                elif(direction & self.south):
                    assert self.nodes[row+1][col] & self.north, "Node %d, %d should have 'north' set"  % (row+1, col)
                    self.nodes[row+1][col] ^ self.north
                    self.nodes[row][col] ^ self.south
                    new_loc = (row+1, col)

                elif(direction & self.east):
                    assert self.nodes[row][col+1] & self.west, "Node %d, %d should have 'east' set"  % (row, col+1)
                    self.nodes[row][col+1] ^ self.west
                    self.nodes[row][col] ^ self.east
                    new_loc = (row, col+1)

                elif(direction & self.west):
                    assert self.nodes[row][col-1] & self.east, "Node %d, %d should have 'south' set"  % (rows, col+1)
                    self.nodes[row][col-1] ^ self.east
                    self.nodes[row][col] ^ self.west
                    new_loc = (row, col-1)

                self.cellStack.push(top)
                self.cellStack.push(new_loc)
                return

        except IndexError:
            return
            


    #TODO: Make a separate class for nodes, and add this function to that class.
    def CheckCellForWalls(self, row, col):
        """ Return true if the node has all Walls up, 
            false otherwise """

        if  ((row < 0) or (row >= grid_rows)):
                return False
        if ((col < 0) and (col >= grid_col)):
                return False

        this_node = self.nodes[row][col]

        if ((row != 0) and not(this_node & self.west)):
            return False
        if ((row != grid_rows-1) and not(this_node & self.east)):
            return False
        if ((col != 0) and not(this_node & self.north)):
            return False
        if ((col != grid_cols-1) and not(this_node & self.south)):
            return False

        return True


if __name__ == "__main__":
    myMaze = maze()
    myMaze.run()
