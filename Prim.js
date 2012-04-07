Maze.prototype.addFringe = function(fringes, row, col){
    node = maze.nodes[row][col];
    node.stat |= stacked;
    fringes.push([row, col]);
};

Maze.prototype.AddIn = function(fringes, row, col){
    var node = this.nodes[row][col];

    // Add neighbours to the fringes list
    if ((row > 0) && (maze.nodes[row-1][col].stat === untouched)){
        maze.addFringe(fringes, row-1, col);
    }
    if ((row < grid_rows-1) && (maze.nodes[row+1][col].stat === untouched)){
        maze.addFringe(fringes, row+1, col);
    }
    if ((col > 0) && (maze.nodes[row][col-1].stat === untouched)){
        maze.addFringe(fringes, row, col-1);
    }
    if ((col < grid_cols-1) && (maze.nodes[row][col+1].stat === untouched)){
        maze.addFringe(fringes, row, col+1);
    }

    // Mark the node as in.
    node.stat |= visited;
};

Maze.prototype.InNeighbours = function(fringe){
    var row = fringe[0]; var col = fringe[1];
    var neighbours = [];

    if( (row > 0) && (maze.nodes[row-1][col].stat & visited)){
            neighbours.push([row-1, col]);
    }
    if( (row < grid_rows-1) && (maze.nodes[row+1][col].stat & visited)){
            neighbours.push([row+1, col]);
    }
    if( (col > 0) && (maze.nodes[row][col-1].stat & visited)){
            neighbours.push([row, col-1]);
    }
    if( (col < grid_cols-1) && (maze.nodes[row][col+1].stat & visited)){
            neighbours.push([row, col+1]);
    }
    return neighbours;
};

Maze.prototype.Carve = function(n0, n1){
    var row0 = n0[0]; var col0 = n0[1];
    var row1 = n1[0]; var col1 = n1[1];
    if(row0 < row1){
        maze.nodes[row0][col0].TearDown(south);
        maze.nodes[row1][col1].TearDown(north);
    }
    if(row0 > row1){
        maze.nodes[row0][col0].TearDown(north);
        maze.nodes[row1][col1].TearDown(south);
    }
    if(col0 < col1){
        maze.nodes[row0][col0].TearDown(east);
        maze.nodes[row1][col1].TearDown(west);
    }
    if(col0 > col1){
        maze.nodes[row0][col0].TearDown(west);
        maze.nodes[row1][col1].TearDown(east);
    }
};

Maze.prototype.PrimGenerate = function(){
    maze = window.maze;
    // Initialization for the first run
    if( maze.cellStack.length > 0 ) {
        var stacktop = maze.cellStack.pop();
        row = stacktop[0]; col = stacktop[1];
        maze.AddIn(maze.fringes, row, col);
    }
    if(maze.fringes.length !== 0){
        anim_request = window.requestAnimFrame(maze.PrimGenerate);
    }
    else{ if(render_steps){ maze.DrawScreen(); } return; }

    // Choose a random fringe cell 
    var index = Math.floor(Math.random()*maze.fringes.length);
    fringe = maze.fringes[index];
    maze.fringes.splice(index, 1);


    maze.nodes[fringe[0]][fringe[1]].stat |= current;
    if(render_steps){ maze.DrawScreen(); }
    maze.nodes[fringe[0]][fringe[1]].stat ^= current;

    // Choose a random neighbour of the fringe and tear down the wall in between
    var neighbours = maze.InNeighbours(fringe);
    index = Math.floor(Math.random()*neighbours.length);
    var neighbour = neighbours[index];
    maze.Carve(fringe, neighbour);

    // Bring the fringe into the in set
    maze.AddIn(maze.fringes, fringe[0], fringe[1]);
};

window.PrimGen = function() {
    window.maze.fringes = [];
    window.maze.runAlgorithm(maze.PrimGenerate);
};
