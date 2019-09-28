import React, { useState, useEffect } from 'react';
import Setup from './components/Setup.js';
import Main from './components/Main.js';
import Process from './components/Process.js';

import './style/App.css';

function App() {
    const [stage, setStage] = useState(0);

    useEffect(() => {
        const header = {
            method: "GET",
            mode: "cors",
            dataType: "application/json"
        };
        fetch('http://127.0.0.1:5000/api/data/src', header)
        .then(r => {
            if (r.status === 404) {
                setStage(1);
                return;
            }
            setStage(3);
        })
        .catch(error => {
            debugger;
            console.log(error)
        })
    }, []);

    function completeStage() {
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
