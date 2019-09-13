import React, { Component } from 'react';
import Main from './components/Main.js';
import './style/App.css';

class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            stage: 0
        };
    }

    componentDidMount() {
        fetch('http://127.0.0.1:5000/api/data/src', {
            method: 'GET',
            mode: 'cors',
            dataType: 'application/json'
        })
        .then(r => r.json())
        .then(data => {
            if (data['success'] === false) {
                this.setState({stage: 1});
            } else {
                this.setState({stage: 3});
            }
        });
    }

    render() {
        switch(this.state.stage) {
            case 0:
                // unset display empty screen
                return this.empty();
            case 1:
                // guide user through selecting source
                return this.setup();
            case 2:
                // display graphics as data is processed
                return this.loading();
            case 3:
                // display full app
                return (
                    <Main>
                    </Main>
                );
            default:
                // unexpected case
                debugger;
                return (
                    <div className="app">
                    <h1> Error </h1>
                    <h3> Unexpected state. </h3>
                    </div>
                );
        }
    }

    empty() {
        return (
            <div className="app">
            </div>
        );
    }

    setup() {
        return (
            <div className="app">
            <h1> Setup </h1>
            <h3> This is cool </h3>
            </div>
        );

    }

    loading() {
        return (
            <div className="app">
            <h1> Loading </h1>
            <h3> Please wait while we provide cool graphics </h3>
            </div>
        );
    }

    app() {
        return (
            <div className="app">
            <h1> Main App </h1>
            <h3> Whoa </h3>
            </div>
        );
    }
}

export default App;
