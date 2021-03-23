import React from 'react';
import '../App.css';

class Finish extends React.Component {
    render() {
        return (
            <div
            style={{
                width:this.props.width+"px",
                height:this.props.height+"px"
            }}
            class="gameCell finish">
                <img
                alt="finishImg"
                class="cellImg"
                src={require("../assets/img/finish.png")}/>
            </div>
        )
    }
}

export default Finish;