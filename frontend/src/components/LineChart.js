import React from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Legend } from 'recharts';

function FrequencyChart(props) {
    const data = props.data;

    if (!data) {
        return (
            <LineChart width={900} height={300} data={null}
            margin={{top: 5, right: 50, left: 0, bottom: 5}}>
            <XAxis dataKey="Label" stroke="#248CF5" />
            <YAxis stroke="#248CF5" />
            </LineChart>
        );
    } else {
        return (
            <ResponsiveContainer width='100%' aspect={3.6/1.0}>
            <LineChart width={900} height={300} data={data}
            margin={{top: 5, right: 50, left: 0, bottom: 5}}>
            <XAxis dataKey="Label" stroke="#248CF5"/>
            <YAxis stroke="#248CF5" />
            <Tooltip/>
            <Legend />
            <Line type="monotone" dataKey="Sent" stroke="#248CF5" dot={false}/>
            <Line type="monotone" dataKey="Received" stroke="#82ca9d" dot={false}/>
            </LineChart>
            </ResponsiveContainer>
        );
    }
}

export default FrequencyChart;
