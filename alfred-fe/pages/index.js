import React, { Component } from 'react';
import moment from 'moment';
import Layout from '../components/layout.js'
import Header from '../components/header.js'
import CalendarDay from '../components/calendar_day.js'
import Link from 'next/link'
import fetch from 'isomorphic-unfetch'


class Index extends Component {
    state = {
        background: '',
        events: [],
        days: []
    }

    cachebust = false

    static async getInitialProps({ req }) {
        return {
            host: req.headers.host
        }
    }

    tick = async () => {
        // Get host
        console.log(`Fetching data...`)
        const res = await fetch(`http://${this.props.host}/static/feed.json`)
        const data = await res.json()

        console.log(`Received data (cachebust: ${data.cachebust})`)
        // Set initial cachebust value
        if (this.cachebust == '') {
            this.cachebust = data.cachebust;
        }

        // Check cachebust
        if (this.cachebust != data.cachebust) {
            console.log('Cache busted!');
            window.location.reload();
        }

        let now = moment();
        let events = data.events.map(ev => {
            let start = moment(ev[0]);
            let end = moment(ev[1]);

            // If this event ended before today (we might be getting stale data), don't show
            if (end.isBefore(now, 'day')) {
                return false;
            }

            return {
                start: start,
                end: end,
                description: ev[2],
                calendar: ev[3],
                id: ev[4]
            }
        });

        this.setState(
            {
                background: data.background,
                events: events,
                days: [
                    this.getDate(moment()),
                    this.getDate(moment().add(1, 'd')),
                    this.getDate(moment().add(2, 'd'))
                ]
            }
        );
    }

    getDate = (d) => d.format('Y-MM-DD')

    componentDidMount() {
        this.tick();
        this.interval = setInterval(() => this.tick(), 10000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    render() {
        return (
            <Layout background={ this.state.background }>
                <Header />
                <div id="calendar">
                    <CalendarDay events={ this.state.events } dayNo="1" day={ this.state.days[0] } />
                    <CalendarDay events={ this.state.events } dayNo="2" day={ this.state.days[1] } />
                    <CalendarDay events={ this.state.events } dayNo="3" day={ this.state.days[2] } />
                </div>
            </Layout>
        )
    }
}

export default Index
