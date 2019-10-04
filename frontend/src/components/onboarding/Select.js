import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import SaveIcon from '@material-ui/icons/Save';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';

const { ipcRenderer } = window.require('electron');

const useStyles = makeStyles(theme => ({
    root: {
        marginTop: theme.spacing(5)
    },
    textField: {
        width: 'calc(100% - 64px - 6px)',
        'padding-right': '6px'
    },
    button: {
        display: 'flex',
        height: '45px',
        'margin-top': '16px'
    },
    holder: {
        display: 'flex'
    }
}));

function Select(props) {
    const example_guess = "/Users/johns/Library/ApplicationSupport/MobileSync/Backup"
    const classes = useStyles();
    const [path, setPath] = useState(props.guess ? props.guess:example_guess)
    const enableNext = props.enableNext;

    // Update source to see if valid
    useEffect(() => {
        const formData = new FormData();
        formData.append('value', path);
        const header = {
            method: "POST",
            mode: "cors",
            body: formData
        };
        fetch('http://127.0.0.1:5000/api/data/src', header)
        .then(r => {
            console.log(r.status);
            if (r.status === 400) {
                enableNext(false);
                return;
            }
            enableNext(true)
        })
        .catch(error => {
            enableNext(false)
            console.log(error)
        })
    }, [path, enableNext]);

    function showFileSelect() {
        ipcRenderer.on('async-file-reply', (event, arg) => {
            if (arg.cancelled === true) { return }

            setPath(arg.filePaths[0])
        })
        ipcRenderer.send('async-file-select', 'ping')
    }

    return (
        <div>
            <Typography variant='h6'> Select Source </Typography>
            <Typography variant='body1'>Comprehensive Analysis of your text messages. This software is currently supported only for iOS and MacOS</Typography>
            <div className={classes.holder}>
                <TextField className={classes.textField}
                    id="outlined-name"
                    label="Backup Source"
                    value={ path }
                    multiline={true}
                    margin="normal"
                    error={false}
                    autoFocus={true}
                    variant="outlined"
                    onChange={(v) => {setPath(v.target.value)}}
                />
                <Button className={classes.button}
                    variant="contained"
                    size="small"
                    onClick={showFileSelect}>
                <SaveIcon className={clsx(classes.leftIcon, classes.iconSmall)} />
              </Button>
          </div>
        </div>
    );
}

export default Select;
