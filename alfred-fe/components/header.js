import React, { Component } from 'react';
import moment from 'moment';

class Header extends Component {
    state = {}

    tick = () => {
        let now = moment();
        this.setState(
            {
                time: now.format('h:mm'),
                ampm: now.format('a'),
                date: now.format('dddd, Do MMMM')
            }
        );
    }

    componentDidMount() {
        this.tick();
        this.interval = setInterval(() => this.tick(), 5000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    render() {
        return (
            <div id="header">
                <div className="datetime">
                    <h1 className="time">{ this.state.time }<span>{ this.state.ampm }</span></h1>
                    <h2 className="date">{ this.state.date }</h2>
                </div>
            </div>
        )
    }
}

export default Header
