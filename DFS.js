Maze.prototype.DFSGenerate = function(){
    maze = window.maze;
    if (render_steps){
        maze.DrawScreen();
    }
    if(maze.cellStack.length !== 0){
        anim_request = window.requestAnimFrame(maze.DFSGenerate);
    }
    try{
        var stacktop = maze.cellStack.pop();
        var row =  stacktop[0];
        var col = stacktop[1];

        var node = maze.nodes[row][col];
        node.stat = visited;
        var neighbours = [];

        if ( (node.IsStanding(north)) && (maze.nodes[row-1][col].AreAllWallsUp(row-1, col))){
            neighbours.push(north);
        }
        if ( (node.IsStanding(south)) && (maze.nodes[row+1][col].AreAllWallsUp(row+1, col))){
            neighbours.push(south);
        }
        if ( (node.IsStanding(west)) && (maze.nodes[row][col-1].AreAllWallsUp(row, col-1))){
            neighbours.push(west);
        }
        if ( (node.IsStanding(east)) && (maze.nodes[row][col+1].AreAllWallsUp(row, col+1))){
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
            maze.nodes[row-1][col].TearDown(south);
            node.TearDown(north);
            new_loc = [row-1, col];
        }
        if (direction & south){
            maze.nodes[row+1][col].TearDown(north);
            node.TearDown(south);
            new_loc = [row+1, col];
        }
        if (direction & east){
            maze.nodes[row][col+1].TearDown(west);
            node.TearDown(east);
            new_loc = [row, col+1];
        }
        if (direction & west){
            maze.nodes[row][col-1].TearDown(east);
            node.TearDown(west);
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
