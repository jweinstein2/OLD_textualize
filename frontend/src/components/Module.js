import React, { useState, useEffect } from 'react';
import Typography from '@material-ui/core/Typography';
import LineChart from './LineChart.js';

function Module(props) {
    const endpoint = 'http://127.0.0.1:5000/api/' + props.endpoint;
    const title = props.title;
    //const type = {
    //    LINE: 'line',
    //    BAR: 'bar',
    //    MISSING: 'missing'
    //}

    const [error, setError] = useState(null);
    const [data, setData] = useState(null);

    useEffect(() => {
        console.log(endpoint);
        const header = {
            method: "GET",
            mode: "cors",
            dataType: "application/json"
        };
        fetch(endpoint, header)
            .then(r => r.json())
            .then(result => setData(result))
            .catch(error => setError(error));
    }, [endpoint]);


    if (error) {
        return (
            <h1> Error </h1>
        );
    }

    if (!data) {
        return <h1> MISSING DATA </h1>
    }

    return (
        <div className="Module">
            <Typography variant='h6'> {title} </Typography>
            <LineChart data={data} />
        </div>

    );
}

export default Module;
