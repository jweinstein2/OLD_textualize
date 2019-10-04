import React, { useState, useEffect } from 'react';
import Setup from './components/onboarding/Setup.js';
import Main from './components/Main.js';
import Process from './components/onboarding/Process.js';

import './style/App.css';

function App() {
    const [stage, setStage] = useState(0);

    useEffect(() => {
        const header = {
            method: "GET",
            mode: "cors",
            dataType: "application/json"
        };
        fetch('http://127.0.0.1:5000/api/data/state', header)
        .then(r => r.json(), e => setStage(4))
        .then(json => setStage(json['state']))
        .catch(error => {
            debugger;
            console.log(error)
        })
    }, []);

    function completeStage() {
        console.log("COMPLETE STAGE");
        setStage(stage + 1)
    }

    switch(stage) {
        case 0:
            // unset display empty screen
            return <div></div>;
        case 1:
            // guide user through selecting source
            return <Setup callback={completeStage} />;
        case 2:
            // display graphics as data is processed
            return <Process callback={completeStage} />;
        case 3:
            // display full app
            return <Main />;
        case 4:
            return <div>
                        Something Went Wrong?
                    </div>
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

export default App
