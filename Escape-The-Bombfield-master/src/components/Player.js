import React from 'react';
import '../App.css';

class Player extends React.Component {
    render() {
        return (
            <div
            style={{
                width:this.props.width+"px",
                height:this.props.height+"px"
            }}
            class="gameCell player">
                <img
                alt="playerImg"
                src={require("../assets/img/player.png")}
                 class="cellImg"/>
            </div>
        )
    }
}

export default Player;