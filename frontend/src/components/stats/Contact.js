import React, { Component } from 'react';
// import ReactTable from 'react-table';
import 'react-table/react-table.css'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Legend } from 'recharts';
// import Wordcloud from 'wordcloud';

class Contact extends Component {
    constructor(props) {
        super(props);

        this.state = {
            number: props.number,
            convo_summary: [],
        };
    }

    componentDidMount() {
        const url = "http://127.0.0.1:5000/api/convos/" + this.state.number + "/frequency";
        fetch(url, {
            method: "GET",
            mode:"cors",
            dataType: "application/json"
        })
        .then(r => r.json())
        .then(data => {
            this.setState({
                frequency: data
            });
        });
    }

    componentWillUnmount() {
        //TODO: cancel fetch
    }

    render() {
        return (
                <ResponsiveContainer width='100%' aspect={3.6/1.0}>
                <LineChart width={900} height={300} data={this.state.frequency}
                margin={{top: 5, right: 50, left: 0, bottom: 5}}>
                <XAxis dataKey="Label" stroke="#FFFFFF44"/>
                <YAxis stroke="#FFFFFF44" />
                <Tooltip/>
                <Legend />
                <Line type="monotone" dataKey="Sent" stroke="#8884d8" />
                <Line type="monotone" dataKey="Received" stroke="#82ca9d" />
                </LineChart>
                </ResponsiveContainer>
               );
    }
}

export default Contact
