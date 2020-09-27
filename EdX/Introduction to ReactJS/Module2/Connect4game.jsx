/**
 * Function component: creates a white Cricle
 */ 
function CircleF(props)
{
  let circleStyle = {
    backgroundColor: "white",
    border: "1px solid black",
    borderRadius: "100%",
    paddingTop: "98%"
  };
  return(
    <div style = {circleStyle}>  </div>
  );
}


/**
 * Class Component. This component renders a circle on the page. It
 * has a numeric property called cell. If cell is equals to 1, than 
 * the circle is rendered BLACK. If the cell is 2, it renders RED. 
 * Otherwise, it renders WHITE. 
 */ 
class Circle extends React.Component 
{
  constructor(props)
  {
    super(props);
  }

  render()
  {
    let color = "white";
    if(this.props.cell == 1)
    {
      color = "black";
    }
    else if(this.props.cell == 2)
    {
      color = "red";
    }
    let circleStyle = {
      backgroundColor: color,
      border: "1px solid black",
      borderRadius: "100%",
      paddingTop: "98%"
    };
    return(
      <div style = {circleStyle}> </div>
    );
  }
}

/**
 * Class component to represents the grid cell where each 
 * circle is placed.  I has the follow props:
 * - handleClick: handler methods passed to process the click event
 * - row: the grid row 
 * - col: the grid column 
 * - cell: cell collor, passet to the Circle component
 */ 
class GridCell extends React.Component 
{
  constructor(props)
  {
    super(props);
  }

  render()
  {
    let gridCellStyle = {
      height: "50px",
      width: "50px",
      border: "1px solid black",
      backgroundColor: "yellow"
    }
    console.log("-- render a GridCell this.props.row :" + this.props.row + 
    ", this.props.col:" + this.props.col + 
    ", this.props.cell: " + this.props.cell);
    return(
      <div style = {gridCellStyle} 
           onClick={() => this.props.handleClick(this.props.row, this.props.col)}>
        <Circle cell={this.props.cell}/>
      </div>
    );
  }
}

/**
 * Class component. Represents a grid row. It has the follow properties:
 * - ncells: number of cells per row
 * - handleClick: function that will be called when a cell is clicked
 * - row: the row number 
 * - key: holds the number of the cell
 */
class GridRow extends React.Component
{
  constructor(props){
    super(props);
    this.state = {
      ncells:7
    }
  }

  componentWillMount()
  {
    let newNCells = (this.props.ncells==null)?this.state.ncells:this.props.ncells;
    console.log("-- GridRow.componentWillMount newNCells:" + newNCells);
    this.setState({ncells: newNCells});
  }

  render(){
    console.log("-- GridRow.render ");
    let rowCells = [];
    var gridRowsStyle = {
      display: "flex"
    };
    console.log("-- adding GridCell's");
    for(let i=0; i<this.state.ncells; i++)
    {
      //console.log("push GridCell key:" + i + ", this.props.cells[i]:" + cells[i] + ", this.props.row:" + this.props.row);
      rowCells.push(<GridCell  key={i} cell={this.props.cells[i]} row={this.props.row}
        col={i} handleClick={this.props.handleClick} />);
    }
    console.log("-- returning GridRow(rowCells[])");
    return(
      <div style={gridRowsStyle}>
        {rowCells}
      </div>
    );
  }
}

/**
 * Class component theat will hold the whole board game.
 * It holds the follow porps:
 * - ncells: holds the number of rows
 */
class Board extends React.Component
{
  // constructor
  constructor(props)
  {
    super(props);
    this.state = {
      ncells: 7
    };
  }
  // comport mounting
  componentWillMount()
  {
    let newNCells = (this.props.ncells==null)?this.state.ncells:this.props.ncells;
    this.setState({ncells: newNCells});
    console.log("Board.componentWillMount ncells:" + newNCells);
  }
  // render component
  render()
  {
    let boardRows = [];
    for(let i=0; i<this.state.ncells; i++)
    {
      boardRows.push(<GridRow key={i} row={i} cells={this.props.cells[i]}
        handleClick={this.props.handleClick} ncells={this.state.ncells}/>);
    }
    return(
      <div>
        {boardRows}
      </div>
    );
  }
}

/**
 * Class component: game controller.
 */
class Game extends React.Component
{
  constructor(props)
  {
    super(props);
    let cells = []; // matrix of states of each cell in the board
    for (let i=0; i<7; i++)
    {
      cells.push(new Array(7).fill(0));
    }
    // state
    // playerTurn: true:black, false:read
    // winner: 0:none, 1:black, 2:red
    // cells: matrix of states of each cell
    this.state = {
      cells: cells,
      playerTurn: false,
      winner: 0
    }
    this.handleClick = this.handleClick.bind(this);
  }

  restart()
  {
      let cells = [];
      for(let i = 0; i < 7; i++ )
      {
        cells.push(new Array(7).fill(0));
      }
      this.setState({ 
                      playerTurn : false, 
                      cells : cells, 
                      winner:0})
  }  

  findAvailableRow(col)
  {
    console.log('col='+col);
    //for(var i = 0; i < 7; i++){
    //  if(this.state.cells[i][col] == 0){
    //    return i;
    //  }
    //}
    for(var i = 0; i < 7; i++)
    {
      if(this.state.cells[i][col] == 0)
      {
        console.log("\tfindAvailableRow:" + i);
        return i;
      }
    }
    console.log("\tfindAvailableRow: -1");
    return -1;
  }

  checkDiagonal(row,col)
  {
      //find right and left tops
      var c = this.state.cells;
      var val = this.state.playerTurn? 2:1;
      var rR = row;
      var cR = col;
      while(rR < 5 && cR < 6)
      {
          rR++;
          cR++;
      }

      while( rR >= 3 && cR >= 3)
      {
          if(c[rR][cR] == val && 
             c[rR-1][cR-1] == val && 
             c[rR-2][cR-2] == val && 
             c[rR-3][cR-3] == val)
          {
            return 1;
          }
          rR--;
          cR--;
      }

      var rL = row;
      var cL = col;

      while(rL < 5 && cL > 0){
          rL++
          cL--
      }

      while(rL >= 3 && cL <= 3){
          if(c[rL][cL] == val && 
             c[rL-1][cL+1] == val && 
             c[rL-2][cL+2] == val && 
             c[rL-3][cL+3] == val)
          {
            return 1;
          }
          rL--;
          cL++;
      }
      return 0
  }

  checkHorizontal(row,col)
  {
      var c = this.state.cells;
      var i = 6;
      var val = this.state.playerTurn? 2:1;

      while( i >= 3)
      {
          if(c[row][i] == val && 
             c[row][i-1] == val && 
             c[row][i-2] == val && 
             c[row][i-3] == val ){
              return 1;
          }
          i--;
      }
      return 0;
  }

  checkVertical(row,col)
  {
      var c = this.state.cells;
      var i = row;
      var val = this.state.playerTurn? 2: 1;

      if(i >= 3)
      {
          if(c[i][col] == val && 
             c[i - 1][col] == val && 
             c[i - 2][col] == val && 
             c[i - 3][col] == val)
          {
            return 1;
          }
      }
      return 0;

  }

  checkVictory(row,col)
  {
      return this.checkVertical(row,col)   || 
             this.checkHorizontal(row,col) ||   
             this.checkDiagonal(row,col)
  }

  // click handler function
  handleClick(row, col)
  {
    console.log("");
    console.log("############################################################");
    console.log("# Click: row: " + row + " | col: " + col);
    console.log("############################################################");
    console.log("Current cells state:"); 
    console.log(this.state.cells);
    if(this.state.winner)
    {
      return;
    } 
    let temp = [];
    console.log("-- load old state");
    for (let i = 0; i<7; i++)
    {
      //console.log('this.state.cells[i]='+this.state.cells[i]);
      temp.push(this.state.cells[i].slice());
    }
    console.log("-- findAvailableRow(" + col + ")");
    let newRow = this.findAvailableRow(col);
    temp[newRow][col] = this.state.playerTurn? 1 : 2;
    this.setState({cells:temp, playerTurn: !this.state.playerTurn}, () => {
        if(this.checkVictory(newRow,col) > 0)
        {
            console.log("win");
            this.setState({winner:this.state.playerTurn?2:1});
        }
        else
        {
          console.log("not-win");
        }
    })
  }

  render()
  {
    return(
    <div>
      <h1>{this.state.winner > 0 ?  this.state.winner == 1? "Black Wins":"Red Wins": this.state.player? "Blacks Turn" : "Reds Turn"} </h1>
      <Board cells={this.state.cells} handleClick={this.handleClick}/>
    <button onClick = { () => this.restart()}>Restart</button>
    </div>
    );
  }

}

ReactDOM.render
(
  <div>
     <Game/>
  </div>,
	document.getElementById("root")
)
