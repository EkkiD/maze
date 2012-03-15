var grey  = "#6E6D6Da";
var green = "#008000";
var dark  = "#302226";
var brightgreen = "#00ff00";
var red = "#ff0000";

var grid_rows = 20; var grid_cols = 25;
var square_pixels = 20;
var width =  600;
var height = 500;
var base_offset = 100;

var north = 1;
var east = 2;
var south = 4;
var west = 8;

var untouched = 0;
var visited = 1;
var stacked = 2;
var current = 3;

var render_steps = true;

function Node(row, col) {
    this.stat = untouched;
    this.walls = north | south | east | west;
    if (col === 0) { this.walls = this.walls ^ west; }
    if (col === grid_cols - 1) { this.walls = this.walls ^ east; }
    if (row === 0) { this.walls = this.walls ^ north; }
    if (row === grid_rows - 1) { this.walls = this.walls ^ south; }

    this.TearDown = function(wall){
        this.walls = this.walls ^ wall;
    };
    this.Erect = function(wall) { 
        this.walls = this.walls | wall;
    };
    this.IsStanding = function(wall) {
        return this.walls & wall;
    };
    this.AreAllWallsUp = function(row, col){
        if  ((row < 0) || (row >= grid_rows)){ return false; }
        if ((col < 0) && (col >= grid_cols)){ return false; }
        if ((row !== 0) && !(this.IsStanding(north))){ return false; }
        if ((row !== grid_rows-1) && !(this.IsStanding(south))){ return false; }
        if ((col !== 0) && !(this.IsStanding(west) )){ return false; }
        if ((col !== grid_cols-1) && !(this.IsStanding(east))){ return false; }
        return true;
    };

}


function Maze(context){
    this.context = context;
    // This is repeated in clearMaze, maybe we can call it here?
    this.nodes = [];
    var i,j;
    for(i = 0; i < grid_rows; i++){
        this.nodes[i] = [];
        for(j = 0; j < grid_cols; j++){
            this.nodes[i][j] = new Node(i, j);
        }
    }
    this.solve_start_x = 0;
    this.solve_start_y = 0;
    this.solve_end_x = grid_rows-1;
    this.solve_end_y = grid_cols-1;

    this.cellStack = [];

    this.FillSquare = function(row, col, color, context){
        var off_x = base_offset + col * square_pixels;
        var off_y = base_offset + row * square_pixels;
        context.fillStyle = color;
        context.strokeStyle = color;
        context.fillRect(off_x+4, off_y+4, square_pixels-8, square_pixels-8);
        context.strokeRect(off_x+4, off_y+4, square_pixels-8, square_pixels-8);
    };

    this.DrawScreen = function(){
        context.clearRect(base_offset, base_offset, grid_cols*square_pixels, grid_rows*square_pixels);
        context.beginPath();
        context.rect(50, 50, width, height);
        context.fillStyle = "#000000";
        context.fill();
        context.lineWidth = 1;
        context.strokeStyle = "black";
        context.stroke();

        var row, col;

        context.strokeStyle = "#ffffff";
        context.strokeRect(base_offset, base_offset, grid_cols*square_pixels, grid_rows*square_pixels);

        for(row = 0; row < grid_rows; row++){
            for(col = 0; col < grid_cols; col++){
                var node = this.nodes[row][col];
                var off_x = base_offset + col * square_pixels;
                var off_y = base_offset + row * square_pixels;
                if (node.IsStanding(north)){
                    context.moveTo(off_x+2, off_y);
                    context.lineTo(off_x + square_pixels - 2, off_y);
                    context.strokeStyle = "white";
                    context.lineWidth = 2;
                    context.stroke();
                }
                if (node.IsStanding(west)){
                    context.moveTo(off_x, off_y+2);
                    context.lineTo(off_x, off_y+square_pixels-2);
                    context.strokeStyle = "white";
                    context.lineWidth = 2;
                    context.stroke();
                }
                if (node.stat === stacked){
                    this.FillSquare(row, col, dark, context);
                }
                if (node.stat === current){
                    this.FillSquare(row, col, green, context);
                }
                if (row === this.solve_start_x && col === this.solve_start_y){
                    this.FillSquare(row, col, brightgreen, context);
                }
                if (row === this.solve_end_x && col === this.solve_end_y){
                    this.FillSquare(row, col, red, context);
                }
            }
        }
    };

    this.runAlgorithm = function(algorithm){
        this.clearStatus();
        start_x = 0; start_y = 0;

        if (algorithm === this.DFSSolve){
            start_x = this.solve_start_x;
            start_y = this.solve_start_y;
        }
        else{
            start_x =  Math.floor(Math.random()*grid_rows);
            start_y =  Math.floor(Math.random()*grid_cols);
        }
        algorithm(this, [start_x, start_y]);
        this.DrawScreen();
    };

    this.moveCurrentSolve = function(x, y){
        this.solve_start_x = x;
        this.solve_start_y = y;
    };

    this.clearMaze = function(){
        this.cellStack = [];
        this.solve_start_x = 0;
        this.solve_start_y = 0;
        // reinitialize nodes
        for(i = 0; i < grid_rows; i++){
            this.nodes[i] = [];
            for(j = 0; j < grid_cols; j++){
                this.nodes[i][j] = new Node(i, j);
            }
        }
        this.DrawScreen();
    };

    this.clearStatus = function(){
        for( row = 0; row < grid_rows; row++){
            for ( col = 0; col < grid_cols; col++){
                this.nodes[row][col].stat = untouched;
            }
        }
    };

    this.DFSGenerate = function(maze, loc){
        maze.cellStack.push(loc);
        var count = 10;
        while (true){
            count -= 1;
            if (maze.cellStack.length === 0 || count <= 0) {return;}
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

            if (neighbours.length === 0){
                stacktop = maze.cellStack.pop();
                maze.nodes[stacktop[0]][stacktop[1]].stat = current;
                maze.cellStack.push(stacktop);
                if (render_steps){
                    window.requestAnimationFrame(maze.DrawScreen);
                }
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
            if (render_steps){
                console.log("Draw The Screen");
                maze.DrawScreen();
            }
        }
    };
}

window.draw = function(){
    window.maze.DrawScreen();
    window.maze.clearMaze();
};

window.onload = function(){
    var canvas = document.getElementById("myCanvas");
    var context = canvas.getContext("2d");
    window.maze = new Maze(context);
    draw(window.maze);
};

window.go = function() {
    window.maze.runAlgorithm(maze.DFSGenerate);
};

