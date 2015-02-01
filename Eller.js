var cur_id = 0;

function randomize(array) {
    if (!array || array.length == 0) {
        return array;
    }
    var i = array.length, j, temp;
    while ( --i )
    {
        j = Math.floor( Math.random() * (i + 1) );
        temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    return array;
}

function NodeSet() {
    this.nodes = new Array();
    this.id = cur_id;
    cur_id = cur_id + 1;
    window.maze.nodeSets.push(this);
}

NodeSet.prototype.unmark = function() {
    for (var i = 0; i < this.nodes.length; i++){
        this.nodes[i].stat = visited;
    }
}

NodeSet.prototype.mark = function() {
    for (var i = 0; i < this.nodes.length; i++){
        this.nodes[i].stat = stacked;
    }
}

Maze.prototype.merge = function(set1, set2) {
    window.maze.nodeSets.splice(window.maze.nodeSets.indexOf(set2), 1);
    for (var i = 0; i < set2.nodes.length; i++){
        set2.nodes[i].nodeSet = set1;
    }
    set1.nodes = set1.nodes.concat(set2.nodes);
    set2.nodes = [];
}

Maze.prototype.GetVerticals = function(row) {
    var maze = window.maze;
    var verticals = [];
    for (var i = 0; i < maze.nodeSets.length; i++){
        var aSet = maze.nodeSets[i];
        nodes = aSet.nodes.filter(function(a) { return a.row === row; });
        nodes = randomize(nodes).slice(0, 1 + Math.floor(Math.random()*(nodes.length-1)));
        verticals = verticals.concat(nodes);
    }
    return verticals;
}

Maze.prototype.markSet = function(node) {
    var maze = window.maze;
    aSet = node.nodeSet;

    if (maze.curSet && maze.curSet != aSet) {
       maze.curSet.unmark();
    }

    maze.curSet = aSet;

    maze.curSet.mark();
}

Maze.prototype.EllerPhase2 = function() {
    var maze = window.maze;
    if (maze.cCol == 0) {
        maze.verticals = maze.GetVerticals(maze.cRow);
    }

    // Step 2: each set must randomly trickle down
    var node = maze.verticals[maze.cCol];
    var aSet = node.nodeSet;

    if (render_steps){
        maze.markSet(node);
        node.stat = current;
        maze.DrawScreen();
    }

    node.TearDown(south);
    sNode = maze.nodes[node.row+1][node.col];
    sNode.TearDown(north);

    sSet = new NodeSet();
    sSet.nodes.push(sNode);
    maze.merge(aSet, sSet);

    maze.cCol = maze.cCol + 1;

    if (maze.cCol == maze.verticals.length) {
        maze.cCol = 0;
        maze.cRow = maze.cRow + 1;
        maze.verticals = [];
        anim_request = window.requestAnimFrame(maze.EllerGenerate);
    }
    else {
        anim_request = window.requestAnimFrame(maze.EllerPhase2);
    }
}

Maze.prototype.clearRow = function(row) {
    var maze = window.maze;
    if (maze.nodes[row]) {
        for (var i = 0; i < maze.nodes[row].length; i++) {
            maze.nodes[row][i].stat = visited;
        }
    }
}

Maze.prototype.initRow = function(aRow) {
    var maze = window.maze;

    for(i = 0; i < grid_cols; i++){
        node = maze.nodes[aRow][i];

        if (node.nodeSet === undefined){
            node.nodeSet = new NodeSet();
            node.nodeSet.nodes.push(node);
        }
    }
}

Maze.prototype.EllerGenerate = function(){
    var maze = window.maze;
    if (maze.nodeSets === undefined) {
        maze.nodeSets = [];
    }
    // Initialize row - give sets to anything without sets
    if (maze.cCol == 0) {
        maze.initRow(maze.cRow);
    }

    // Step 1: merge randomly in current row
    lNode = maze.nodes[maze.cRow][maze.cCol];
    rNode = maze.nodes[maze.cRow][maze.cCol+1];
    cFlip = Math.floor(Math.random()*2);

    if (render_steps){
        maze.markSet(lNode);
        lNode.stat = current;
        maze.DrawScreen();
    }

    if ((lNode.nodeSet !== rNode.nodeSet) && (cFlip === 0 || maze.cRow == grid_rows-1)) {
        lNode.TearDown(east);
        rNode.TearDown(west);
        maze.merge(lNode.nodeSet, rNode.nodeSet);
    }
    maze.cCol = maze.cCol + 1;

    if (maze.cCol < grid_cols-1) {
        maze.clearRow(row);
        anim_request = window.requestAnimFrame(maze.EllerGenerate);
    }
    else if (maze.cRow < grid_rows-1){
        maze.cCol = 0;
        anim_request = window.requestAnimFrame(maze.EllerPhase2);
    }
    if (maze.cRow >= grid_rows-1 && maze.cCol >= grid_cols-1) {
        maze.curSet.unmark();
        maze.DrawScreen();
    }
}

window.EllerGen = function() {
    window.maze.cRow = 0;
    window.maze.cCol = 0;
    window.maze.nodeSets = [];
    window.maze.runAlgorithm(maze.EllerGenerate);
};
