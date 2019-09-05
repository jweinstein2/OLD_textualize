import React, { Component } from 'react';
import ReactTable from 'react-table';
import 'react-table/react-table.css'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

class Main extends Component {
    constructor(props) {
        super(props);

:q
:q
        this.state = {
            convo_summary: [],
            columns: []
        };
    }

    componentDidMount() {
        fetch("http://127.0.0.1:5000/api/convos/frequency", {
            method: "GET",
            mode:"cors",
            dataType: "application/json"
        })
        .then(r => r.json())
            .then(data => {
                this.setState({
                    data: data
                });
            })
    }

    componentWillUnmount() {
        //TODO: cancel fetch
    }

    render() {
        return (
            <div className="Main">
                <ResponsiveContainer width='100%' aspect={3.6/1.0}>
                <LineChart width={900} height={300} data={this.state.data}
                margin={{top: 5, right: 100, left: 20, bottom: 5}}>
                <XAxis dataKey="Label" stroke="#FFFFFF44"/>
                <YAxis stroke="#FFFFFF44"/>
                <Tooltip/>
                <Legend />
                <Line type="monotone" dataKey="Sent" stroke="#8884d8" />
                <Line type="monotone" dataKey="Received" stroke="#82ca9d" />
                </LineChart>
                </ResponsiveContainer>
            </div>
           );
    }
}

export default Main
