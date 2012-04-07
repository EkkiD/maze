window.solve = function() {
    window.maze.runAlgorithm(maze.DFSSolve);
};

Maze.prototype.DFSSolve = function(){
    maze = window.maze;
    if (render_steps){
        maze.DrawScreen();
    }
    try{
        var stacktop = maze.cellStack.pop();
        //If we're at the destination, we can abort

        if((stacktop[0] === maze.solve_end_x) && (stacktop[1] === maze.solve_end_y)){
            return;
        }
        else{ 
            anim_request = window.requestAnimFrame(maze.DFSSolve);
        }
        var row =  stacktop[0];
        var col = stacktop[1];

        var node = maze.nodes[row][col];
        node.stat = visited;
        var neighbours = [];


        if ( (row > 0) && !(node.IsStanding(north)) 
            && (maze.nodes[row-1][col].stat === untouched)){
            neighbours.push(north);
        }
        if ( (row < grid_rows-1) && !(node.IsStanding(south)) 
            && (maze.nodes[row+1][col].stat === untouched)){
            neighbours.push(south);
        }
        if ( (col > 0) && !(node.IsStanding(west))
            && (maze.nodes[row][col-1].stat === untouched)){
            neighbours.push(west);
        }
        if ( (col < grid_cols-1) && !(node.IsStanding(east)) 
            && (maze.nodes[row][col+1].stat === untouched)){
            neighbours.push(east);
        }

        // Pop off the stack if there are no neighbours
        if (neighbours.length === 0){
            stacktop = maze.cellStack.pop();
            maze.nodes[stacktop[0]][stacktop[1]].stat = current;
            maze.cellStack.push(stacktop);
            return;
        }

        var index = Math.floor(Math.random()*neighbours.length);
        var direction = neighbours[index];
        var new_loc = [0, 0];

        if (direction & north){
            new_loc = [row-1, col];
        }
        if (direction & south){
            new_loc = [row+1, col];
        }
        if (direction & east){
            new_loc = [row, col+1];
        }
        if (direction & west){
            new_loc = [row, col-1];
        }
        node.stat = stacked;
        maze.cellStack.push(stacktop);
        maze.cellStack.push(new_loc);
        maze.nodes[new_loc[0]][new_loc[1]].stat = current;
    }
    catch(e){
        if((e instanceof TypeError) && (e.message === "stacktop is undefined")){
            return;
        }
        else{
            throw e;
        }
    }
};

window.DFSGen = function() {
    window.maze.runAlgorithm(maze.DFSGenerate);
};
