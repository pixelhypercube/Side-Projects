import React from 'react';
import '../App.css';

class Bomb extends React.Component {
    render() {
        return (
            <div
            style={{
                width:this.props.width+"px",
                height:this.props.height+"px"
            }}
            class="gameCell bomb">
                <img
                alt="bombImg"
                class="cellImg" src={require("../assets/img/mine.png")}/>
            </div>
        )
    }
}

export default Bomb;