import React from 'react';
import JsxParser from 'react-jsx-parser';
import './App.css';
import Cell from './components/Cell';
import Bomb from './components/Bomb';
import Player from './components/Player';
import Finish from "./components/Finish";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      board:[],
      playerMap:[],
      playerPos:{
        x:0,
        y:0,
      },
      finshPos:{
        x:0,
        y:0,
      },
      boardRenderer:null,
      size:{
        width:16,
        height:16
      },
      gameState:"game"
    }
  }
  componentWillMount()  {
    var {width,height} = this.state.size;
    this.fillArrMap(width,height);
    this.updatePlayerMap(width,height);
    // this.boardRendering();
    // this.setState({boardRenderer:this.boardRendering()})
  }
  fillArrMap(width,height) {
    // var playerPos = this.state.playerPos;
    // var {x,y} = playerPos;
    var board = [];
    for (let i = 0;i<height;i++) {
      board.push([]);
      for (let j = 0;j<width;j++) {
        if (j%2===0) {
          board[i].push(0);
        } else {
          if (i%2===Math.floor(Math.random()*board.length)) {
            board[i].push(1);
          } else {
            board[i].push(0);
          }
        }
        // board[i].push(Math.floor(Math.random()*1.1));
      }
    }
    board[Math.floor(Math.random()*board.length)]
    [board.length-1] = 2;
    this.setState({board});
    console.log(this.state.board);
    // return board;
  }
  updatePlayerMap(width,height) {
    var playerMap = [];
    for (let i = 0;i<height;i++) {
      playerMap.push([]);
      for (let j = 0;j<width;j++) {
        if (i===this.state.playerPos.y 
          && j===this.state.playerPos.x) {
            playerMap[i].push(1);
        } else {
          playerMap[i].push(0);
        }
      }
    }
    // console.log("VARIABLE: ",playerMap);
    this.setState({playerMap});
    // console.log("PLAYER MAP: ",this.state.playerMap);
    if (this.state.board.length!==0) {
      this.boardRendering(this.state.playerPos.x,this.state.playerPos.y);
    }
  }
  boardRendering(posX,posY) {
    var str = "";
    this.setState({
      finishPos:{
        x:this.state.size.width-1,
        y:Math.floor(Math.random()*this.state.size.height)
      }
    });
    for (let i = 0;i<this.state.board.length;i++) {
      str+=`<div style={{display:"flex"}}>`;
      for (let j = 0;j<this.state.board[i].length;j++) {
        if (i===posY && j===posX) {
          // console.log(posX,posY);
          // str+=`<div>
          //   <div class="player"></div>
          // </div>`;
          str+=`<Player
          width={${this.state.width}}
          height={${this.state.height}}
          ></Player>`;
          if (this.state.board[i][j]===1) {
              this.setState({gameState:"gameOver"})
          }
          if (this.state.board[i][j]===2) {
              this.setState({gameState:"finished"})
          }
        } else if (this.state.board[i][j]===0) {
        //   str+=`<div>
        //   <div class="cell"></div>
        // </div>`;
          str+=`<Cell
          width={${this.state.width}}
          height={${this.state.height}}
          ></Cell>`
        } else if (this.state.board[i][j]===1) {
          // str+=`<div>
          //   <div class="bomb">
          //     <img src={require("./assets/img/mine.png")} />
          //   </div>
          // </div>`;
          str+=`<Bomb
          width={${this.state.width}}
          height={${this.state.height}}
          ></Bomb>`;
        } else if (this.state.board[i][j]===2) {
          str+=`<Finish
          width={${this.state.width}}
          height={${this.state.height}}
          ></Finish>`;
        }
      }
      str+=`</div>`;
    }
    // console.log(str);
    this.setState({boardRenderer:str});
    return str;
  }
  movePlayer(key) {
    var playerPos = this.state.playerPos;
    // var {x,y} = playerPos;
    // console.log("moving player")
    if (this.state.gameState==="game") {
      switch (key) {
        case 37:
        case 65:
          playerPos.x--;
          break;
        case 39:
        case 68:
          playerPos.x++;
          break;
        case 40:
        case 83:
          playerPos.y++;
          break;
        case 38:
        case 87:
          playerPos.y--;
          break;
        default:
          break;
      }
      if (playerPos.x<0) {
        playerPos.x = 0;
      }
      if (playerPos.x>this.state.size.width-1) {
        playerPos.x = this.state.size.width-1;
      }
      if (playerPos.y<0) {
        playerPos.y = 0;
      }
      if (playerPos.y>this.state.size.height-1) {
        playerPos.y = this.state.size.height-1;
      }
    }
    this.setState({playerPos});
    this.updatePlayerMap(10,10);
  }
  renderScreen() {
    switch (this.state.gameState) {
      case "game":
        return <JsxParser 
        components={{Bomb,Cell,Finish,Player}} 
        jsx={this.state.boardRenderer===null
        ? this.boardRendering(this.state.playerPos.x,this.state.playerPos.y) : this.state.boardRenderer}/>
      case "gameOver":
        return <div>
          <h1>Game Over!</h1>
          <h4>You've stepped on a bomb!</h4>
          <button
          className="restartBtn"
          onMouseDown={()=>{
            window.location.reload(false);
          }}
          >Restart Game</button>
        </div>
      case "finished":
        return <div>
        <h1>Congratulations!</h1>
        <h4>You've made it!</h4>
        <button
        className="restartBtn"
        onMouseDown={()=>{
          window.location.reload(false);
        }}
        >Restart Game</button>
      </div>
      default:
        break;
    }
  }
  render() {
    return (
      <div className="App" onKeyDown={(e)=>{
        e.preventDefault();
        this.movePlayer(e.keyCode);
      }}>
        <header>
          <h1>Escape the bombfield!</h1>
          <h2>By PixelHyperCube</h2>
          <h3>A game made using ReactJS!</h3>
        </header>
        <main style={{outline:"none"
        ,display:"flex"
        ,justifyContent:"center"
      ,flexDirection:"column"}} tabIndex="0">
          <div id="info">
            <h3>The game may seem to be rather basic as this is a demo miniproject</h3>
            <h3>One of my first few attempts of using game development skills in React!</h3>
            <h3>Feel free to play!</h3>
          </div>
          <div id="instructions">
            <h2>Run to the finish cell as fast as possible!</h2>
            <h3>Avoid the bombs!</h3>
            <h3>Use the WASD / ←↑→↓ keys to move!</h3>
          </div>
          {this.renderScreen()}
        </main>
        <footer>
          &copy; 2020
        </footer>
      </div>
    );
  }
}

export default App;
