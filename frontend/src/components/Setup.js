import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles(theme => ({
    root: {
        marginTop: theme.spacing(5)
    },
    backButton: {
        marginRight: theme.spacing(1),
    },
    nextButton: {

    },
    instructions: {
        marginTop: theme.spacing(1),
        marginBottom: theme.spacing(1),
    },
}));

function getStepContent(stepIndex) {

    switch (stepIndex) {
        case 0:
            return (
                <div>
                    <Typography variant='h6'> Please Note </Typography>
                    <ul>
                        <li> All data is processed locally to guarantee your security </li>
                        <li> Currently only macOS and iOS are supported.</li>
                        <li>Made with love by Jared Weinstein. 2019 </li>
                    </ul>
                </div>
            );
        case 1:
            return (
                <div>
                    <Typography variant='h6'> Grant Necessary File Access </Typography>
                    <Typography variant='body1'>Comprehensive Analysis of your text messages. This software is currently supported only for iOS and MacOS</Typography>
                </div>
            );
        case 2:
            return (
                <div>
                    <Typography variant='h6'> Create iPhone backup </Typography>
                    <Typography variant='body1'>Comprehensive Analysis of your text messages. This software is currently supported only for iOS and MacOS</Typography>
                </div>
            );
        case 3:


            return (
                <div>
                    <Typography variant='h6'> Select Source </Typography>
                    <Typography variant='body1'>Comprehensive Analysis of your text messages. This software is currently supported only for iOS and MacOS</Typography>
                </div>
            );
        case 4:
            return (
                <div>
                    <Typography variant='h6'> Process </Typography>
                    <Typography variant='body1'> For larger backup files this can take up to 20 minutes. </Typography>
                </div>
            );
        default:
            debugger;
            return 'Unknown stepIndex';
    }
}

function Setup(props) {
    const finished = props.callback;
    const classes = useStyles();
    const [activeStep, setActiveStep] = React.useState(0);
    const steps = ['About', 'Permissions', 'Backup', 'Select', 'Process'];

    const handleNext = () => {
        if (activeStep === steps.length - 1) {
            finished()
        }
        setActiveStep(activeStep => activeStep + 1);
    };

    const handleBack = () => {
        setActiveStep(prevActiveStep => prevActiveStep - 1);
    };


    return (
        <div className={classes.root}>
        <Container maxWidth='sm'>
        <Stepper activeStep={activeStep} alternativeLabel>
        {steps.map(label => (
            <Step key={label}>
            <StepLabel>{label}</StepLabel>
            </Step>
        ))}
        </Stepper>
        <div>
        {activeStep === steps.length ? (
            <div>
            <Typography className={classes.instructions}>All steps completed</Typography>
            </div>
        ) : (
            <div>
            {getStepContent(activeStep)}
            <div>
            <Button
            disabled={activeStep === 0}
            onClick={handleBack}
            className={classes.backButton}
            >
            Back
            </Button>
            <Button variant="contained" color="primary" onClick={handleNext}>
            {activeStep === steps.length - 1 ? 'Analyze!' : 'Next'}
            </Button>
            </div>
            </div>
        )}
        </div>
        </Container>
        </div>
    );
}

export default Setup;
