import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';

import Header from './Header.js';

const useStyles = makeStyles(theme => ({
  button: {
    margin: theme.spacing(1),
  },
  input: {
    display: 'none',
  },
}));

function Setting() {
    const classes = useStyles();

    function reset() {
        const header = {
            method: "DELETE",
            mode: "cors",
        };
        fetch('http://127.0.0.1:5000/api/data/src', header)
        .catch(error => {
            console.log(error)
        })
    };

    return (
        <div>
            <Header title="Settings"></Header>
            <Button variant="contained" color="secondary" onClick={reset} className={classes.button}>
                Reset
            </Button>
        </div>
    );
}

export default Setting


