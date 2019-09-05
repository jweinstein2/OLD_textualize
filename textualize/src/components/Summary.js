import React, { Component } from 'react';
import RangePicker from './RangePicker';
// import Paper from '@material-ui/core/Paper';
// import Grid from '@material-ui/core/Grid';

import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Legend } from 'recharts';

// import { makeStyles } from '@material-ui/core/styles';
//
// const useStyles = makeStyles(theme => ({
//   root: {
//     flexGrow: 1,
//   },
//   paper: {
//     padding: theme.spacing(2),
//     textAlign: 'center',
//     color: theme.palette.text.secondary,
//   },
// }));

class Summary extends Component {
    constructor(props) {
        super(props);

        this.state = {
        };
    }

    componentDidMount() {
        const url = "http://127.0.0.1:5000/api/stats/frequency";
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

    }


    render() {
        return (
            <div>
                <RangePicker />
                <ResponsiveContainer width='100%' aspect={3.6/1.0}>
                <FrequencyChart data={this.state.frequency} />
                </ResponsiveContainer>
            </div>
        );
    }
    /*
    render() {
        // const classes = useStyles();
        return (
            <div>
            <RangePicker>
            </RangePicker>
            <div>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Paper >xs=12</Paper>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Paper >xs=12 sm=6</Paper>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Paper >xs=12 sm=6</Paper>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Paper >xs=6 sm=3</Paper>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Paper >xs=6 sm=3</Paper>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Paper >xs=6 sm=3</Paper>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Paper >xs=6 sm=3</Paper>
              </Grid>
            </Grid>
            </div>
          </div>
        );
    }
    */
    }

function FrequencyChart(props) {
    const data = props.data;
    console.log(data);
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
            <LineChart width={900} height={300} data={data}
            margin={{top: 5, right: 50, left: 0, bottom: 5}}>
            <XAxis dataKey="Label" stroke="#248CF5"/>
            <YAxis stroke="#248CF5" />
            <Tooltip/>
            <Legend />
            <Line type="monotone" dataKey="Sent" stroke="#248CF5" dot={false}/>
            <Line type="monotone" dataKey="Received" stroke="#82ca9d" dot={false}/>
            </LineChart>
        );
    }
}

export default Summary
