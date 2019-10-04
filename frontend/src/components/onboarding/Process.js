/* eslint-disable */
import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import LinearProgress from '@material-ui/core/LinearProgress';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles(theme => ({
    progress: {
        flexGrow: 1,
    },
}));

function Process(props) {
    const finished = props.callback;
    const classes = useStyles();
    const [progress, setProgress] = useState(0);
    const [error, setError] = useState(null);
    const [complete, setComplete] = useState(false);

    useEffect(() => {
        function beginProcess() {
            const header = {
                method: "POST",
                mode: "cors",
            };
            fetch('http://127.0.0.1:5000/api/data/setup', header)
            .then(r => {
                if (r.status !== 201) {
                    return
                }
                console.log("STARTED")
            })
            .catch(error => {
                console.log(error)
            })
        }

        function poll() {
            const header = {
                method: "GET",
            };
            fetch('http://127.0.0.1:5000/api/data/setup', header)
            .then(r => r.json())
            .then(r => {
                switch(r['status']) {
                    case "unstarted":
                        console.log("BEGIN PROCESS");
                        beginProcess();
                        break;
                    case "in_progress":
                        console.log("UPDATE PROCESS");
                        setProgress(r['message']);
                        break;
                    case "error":
                        console.log("SET ERROR");
                        setError(r['message']);
                        break;
                    case "completed":
                        console.log("SET COMPLETE");
                        setComplete(true)
                        break;
                    default:
                        setError("improperly handled json response");
                }
            })
            .catch(error => {
                console.log(error)
            })
        }

        const timer = setInterval(poll, 500);
        return () => {
            clearInterval(timer);
        };
    }, [setError, setComplete, setProgress]);


    if (error) {
        return (
            <div>
                Error
            </div>
        );
    }

    if (complete) {
        return (
            <Button variant="contained" color="primary" onClick={finished} className={classes.button}>
                Continue
            </Button>
        );

    }

    return (
        <div>
            <LinearProgress className={classes.progress}
                            variant="determinate"
                            value={progress} />
        </div>
    );
}

export default Process;
