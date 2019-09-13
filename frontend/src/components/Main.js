import React from 'react';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import CssBaseline from '@material-ui/core/CssBaseline';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';

import HomeIcon from '@material-ui/icons/Home';
import PersonIcon from '@material-ui/icons/Person';
import StarIcon from '@material-ui/icons/Star';
import SettingsIcon from '@material-ui/icons/Settings';
import ViewListIcon from '@material-ui/icons/ViewList';
import HelpIcon from '@material-ui/icons/Help';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';

import Summary from './Summary.js';

const drawerWidth = 200;

const useStyles = makeStyles(theme => ({
    root: {
        display: 'flex',
    },
    drawer: {
        width: drawerWidth,
        flexShrink: 0,
        whiteSpace: 'nowrap',
    },
    drawerOpen: {
        width: drawerWidth,
        transition: theme.transitions.create('width', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
    },
    drawerClose: {
        transition: theme.transitions.create('width', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
        overflowX: 'hidden',
        width: theme.spacing(7) + 1,
    },
    toolbar: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'flex-end',
        padding: theme.spacing(0, .5),
        ...theme.mixins.toolbar,
    },
    content: {
        flexGrow: 1,
        padding: theme.spacing(3),
    },
}));

export default function Main() {
    const classes = useStyles();
    const [open, setOpen] = React.useState(false);
    const [selected, setSelected] = React.useState("Summary")

    return (
        <div className={classes.root}>
            <CssBaseline />
            <Drawer
                variant="permanent"
                className={clsx(classes.drawer, {
                    [classes.drawerOpen]: open,
                    [classes.drawerClose]: !open,
                })}
                classes={{
                    paper: clsx({
                        [classes.drawerOpen]: open,
                        [classes.drawerClose]: !open,
                    }),
                }}
                open={open}
            >
            <div className={classes.toolbar}>
                <IconButton onClick={() => setOpen(!open)}>
                {open ? <ChevronLeftIcon /> : <ChevronRightIcon />}
                </IconButton>
            </div>
            <Divider />
            <List>
                {menuItem("Summary", <HomeIcon />, setSelected)}
                {menuItem("Contacts", <PersonIcon />, setSelected)}
                {menuItem("Table", <ViewListIcon />, setSelected)}
                {menuItem("Advanced", <StarIcon />, setSelected)}
            </List>
            <Divider />
            <List>
                {menuItem("Settings", <SettingsIcon />, setSelected)}
                {menuItem("About", <HelpIcon />, setSelected)}
            </List>
            </Drawer>
            <main className={classes.content}>
            { getContent(selected) }
            </main>
        </div>
    );
}

function getContent(selected) {
    switch (selected) {
        case "Summary":
            return <Summary />;
        case "Contacts":
            return (
                <h1> Contacts Not Implemented </h1>
            );
        case "Table":
            return (
                <h1> Table Not Implemented </h1>
            );
        case "Advanced":
            return (
                <h1> Advanced Not Implemented </h1>
            );
        case "Settings":
            return (
                <h1> Settings Not Implemented </h1>
            );
        case "About":
            return (
                <h1> About Not Implemented </h1>
            );
        default:
            debugger;
            return (
                <h1> Unhandled Menu Item </h1>
            );
    }

}

function menuItem(text, icon, callback) {
    return(
        <ListItem button key={text} onClick={() => callback(text)}>
        <ListItemIcon>{icon}</ListItemIcon>
        <ListItemText primary={text} />
        </ListItem>
    );
}
