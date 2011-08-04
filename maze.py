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
    
north = 1
east = 2
south = 4
west = 8

   
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

class node(object):
    """ Stores data regarding the self.nodes:
            - which walls are up
            - visited flag"""

    def __init__(self, row, col):
        self.walls = north | south | east | west
        if col == 0:               self.walls = self.walls ^ west
        if col == grid_cols - 1:   self.walls = self.walls ^ east
        if row == 0:               self.walls = self.walls ^ north
        if row == grid_rows - 1:   self.walls = self.walls ^ south
        self.visited = False

    def TearDown(self, wall):
        self.walls = self.walls ^ wall

    def Erect(self, wall):
        self.walls = self.walls | wall

    def IsStanding(self, wall):
        return self.walls & wall

    def AreAllWallsUp(self, row, col):
        """ Return true if the node has all Walls up, 
            false otherwise """

        if  ((row < 0) or (row >= grid_rows)):
                return False
        if ((col < 0) and (col >= grid_col)):
                return False


        if ((row != 0) and not(self.IsStanding(north))):
            return False
        if ((row != grid_rows-1) and not(self.IsStanding(south))):
            return False
        if ((col != 0) and not(self.IsStanding(west) )):
            return False
        if ((col != grid_cols-1) and not(self.IsStanding(east))):
            return False

        return True


    

class maze(object):
    """This class handles all of the maze generation and solving functions.

    Should be treated as a singleton until I figure out this member variable thing.
    
    For now this class will also take care of rendering the maze. Not sure if this is the best design but we'll use it for now"""
    
    def __init__(self):
        self.nodes = [None] * grid_rows
        for i in range(grid_rows):
            self.nodes[i] = [None] * grid_cols

        # initialize the array as a valid grid.
        for i in range(grid_rows):
            for j in range(grid_cols):
                self.nodes[i][j] = node(i, j)

        
        self.cellStack = deque()
        self.cellStack.append((0,0))


    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                #if event.type == pygame.KEYUP:
                   # if event.key == pygame.K_RIGHT:
            self.DoIteration();

            screen.fill(black)
            self.DrawScreen(screen)
            clock.tick(40)
            
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

                if self.nodes[row][col].IsStanding(north):
                    assert row > 0, "Can't draw north of row 0"
                    assert self.nodes[row-1][col].IsStanding(south), "Node %d, %d should have 'south' set"  % (row-1, col)
                    pygame.draw.line(screen, white, (off_x+2, off_y), (off_x+square_pixels-2, off_y), 2)

                if self.nodes[row][col].IsStanding(west):
                    assert col > 0, "Can't draw west of col 0"
                    assert self.nodes[row][col-1].IsStanding(east), "Node %d, %d should have 'east' set"  % (row, col-1)
                    pygame.draw.line(screen, white, (off_x, off_y+2), (off_x, off_y+square_pixels-2), 2)

                if self.nodes[row][col].visited:
                    rect = (off_x+4, off_y+4,  square_pixels - 6, square_pixels - 6)
                    #pygame.draw.rect(screen, grey, rect)
        try:
            node = self.cellStack.pop()
            row = node[0]
            col = node[1]
            off_x = base_offset + col * square_pixels
            off_y = base_offset + row * square_pixels
            rect = (off_x+4, off_y+4,  square_pixels - 6, square_pixels - 6)
            pygame.draw.rect(screen, green, rect)
            self.cellStack.append(node)
        except IndexError:
            pygame.display.flip()

        pygame.display.flip()


    def DFSGenerate(self):
        neighbors = []
        try:
            while True:  
                top = self.cellStack.pop()
                row = top[0] 
                col = top[1]
                node = self.nodes[row][col]
                if (node.IsStanding(north)) and self.nodes[row-1][col].AreAllWallsUp(row-1, col):
                    neighbors.append(north)

                if (node.IsStanding(south)) and self.nodes[row+1][col].AreAllWallsUp(row+1, col):
                    neighbors.append(south)

                if (node.IsStanding(west)) and self.nodes[row][col-1].AreAllWallsUp(row, col-1):
                    neighbors.append(west)

                if (node.IsStanding(east)) and self.nodes[row][col+1].AreAllWallsUp(row, col+1):
                    neighbors.append(east)

                if(neighbors.__len__() == 0):
                    continue

                index = random.randint(0,neighbors.__len__()-1)
                direction = neighbors[index]

                if(direction & north):
                    assert self.nodes[row-1][col].IsStanding(south), \
                                    "Node %d, %d should have 'south' set"  % (row-1, col)
                    self.nodes[row-1][col].TearDown(south)
                    node.TearDown(north)
                    new_loc = (row-1, col)

                elif(direction & south):
                    assert self.nodes[row+1][col].IsStanding(north), \
                                    "Node %d, %d should have 'north' set"  % (row+1, col)
                    self.nodes[row+1][col].TearDown(north)
                    node.TearDown(south)
                    new_loc = (row+1, col)

                elif(direction & east):
                    assert self.nodes[row][col+1].IsStanding(west), \
                                    "Node %d, %d should have 'east' set"  % (row, col+1)
                    self.nodes[row][col+1].TearDown(west)
                    node.TearDown(east)
                    new_loc = (row, col+1)

                elif(direction & west):
                    assert self.nodes[row][col-1].IsStanding(east), \
                                    "Node %d, %d should have 'south' set"  % (rows, col+1)
                    self.nodes[row][col-1].TearDown(east)
                    node.TearDown(west)
                    new_loc = (row, col-1)

                node.visited = True
                self.cellStack.append(top)
                self.cellStack.append(new_loc)
                return

        except IndexError, e:
            return
            




if __name__ == "__main__":
    myMaze = maze()
    myMaze.run()

