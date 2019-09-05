import React, { Component } from 'react';

class Onboard extends Component {
    constructor(props) {
        super(props);
        this.callback = this.props.callback;

        this.state = {
            backup_path: '',
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
        fetch("http://127.0.0.1:5000/api/data/src/guess", {
            method: "GET",
            mode:"cors",
            dataType: "application/json"
        })
        .then(r => r.json())
            .then(data => {
                if (this.state.backup_path === '') {
                    this.setState({
                        backup_path: data,
                        submitting: false
                    });
                }
            })
    }

    render() {
        return (
            <div className="Setup">
                <form onSubmit={this.handleSubmit}>
                    <label> Backup Location:
                    <textarea value={this.state.backup_path} onChange={this.handleChange} />
                    </label>
                    <input type="submit" value="Submit" disabled={this.state.submitting}/>
                </form>
            </div>
           );
    }

    handleChange(event) {
        this.setState({backup_path: event.target.value});
    }

    handleSubmit(event) {
        this.setState({submitting: true});

        var data = new FormData();
        data.append("value", this.state.backup_path);

        event.preventDefault();
        fetch("http://127.0.0.1:5000/api/data/src/", {
            method: "POST",
            mode: "cors",
            body: data
        })
        .then(r => r.json())
            .then(data => {
                this.setState({submitting: false});
                if (data["success"] === true){
                    this.callback();
                    return;
                }
                console.log(data["success"])
            })
    }
}

export default Onboard
