import React, { Component } from 'react';
import ReactTable from 'react-table';
import 'react-table/react-table.css'

class Table extends Component {
    constructor(props) {
        super(props);

		this.cols = [
            {
              Header: "Name",
              accessor: "name"
            },
//            {
//                Header: "Number",
//                accessor: "number"
//            },
            {
                Header: "Sent",
                accessor: "n_sent"
            },
            {
                Header: "Received",
                accessor: "n_recieved"
            },
            {
                Header: "Your Avg Response Time",
                accessor: "your_response_time"
            },
            {
                Header: "Their Avg Response Time",
                accessor: "their_response_time"
            },
            {
                Header: "Ignored (%)",
                accessor: "ignored"
            },
            {
                Header: "Convos Started (%)",
                accessor: "convos started"
            },
            {
                Header: "Convos Ended (%)",
                accessor: "convos ended"
            },
        ];

        this.cols2 = [
            {
              Header: "Name",
              accessor: "name"
            },
            {
                Header: "Your Avg Word Length",
                accessor: "avg_wordlen_sent"
            },
            {
                Header: "Their Avg Word Length",
                accessor: "avg_wordlen_recieved"
            },
            {
                Header: "Unique Words Received",
                accessor: "vocab_recieved"
            },
            {
                Header: "Unique Words Sent",
                accessor: "vocab_sent"
            },
        ];

        this.state = {
            data: []
        };
    }

    componentDidMount() {
        fetch("http://127.0.0.1:5000/api/convos/summary", {
            method: "GET",
            mode:"cors",
            dataType: "application/json"
        })
        .then(r => r.json())
        .then(data => {
            this.setState({
                data: data.data
            });
        })
    }

    componentWillUnmount() {
        //TODO: cancel fetch
    }

    render() {
        if (this.state.data.length === 0) {
            return (
                <div>Loading...</div>);
        }

        return (
            <div>
            <ReactTable
            data={this.state.data} columns={this.cols}
            defaultPageSize={10}
            style={{height: 400}}
            filterable={true}
            className="-striped -highlight"/>

            <div className="Page-header">
            Text Analysis
            </div>

            <ReactTable
            data={this.state.data} columns={this.cols2}
            defaultPageSize={10}
            style={{height: 400}}
            filterable={true}
            className="-striped -highlight"/>
            </div>);
    }
}

export default Table
