import React from 'react';
import '../App.css';

class Cell extends React.Component {
    render() {
        return (
            <div
            style={{
                width:this.props.width+"px",
                height:this.props.height+"px"
            }}
            class="gameCell cell">
                {/* <img 
                alt="cellImg"
                class="cellImg"/> */}
            </div>
        )
    }
}

export default Cell;