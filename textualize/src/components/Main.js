import React, { Component } from 'react';

// import { makeStyles, useTheme } from '@material-ui/core/styles';
//
// import Drawer from '@material-ui/core/Drawer';
// import AppBar from '@material-ui/core/AppBar';
// import Toolbar from '@material-ui/core/Toolbar';
// import List from '@material-ui/core/List';
// import CssBaseline from '@material-ui/core/CssBaseline';
// import Typography from '@material-ui/core/Typography';
// import Divider from '@material-ui/core/Divider';
// import IconButton from '@material-ui/core/IconButton';
// import MenuIcon from '@material-ui/icons/Menu';
// import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
// import ChevronRightIcon from '@material-ui/icons/ChevronRight';
// import ListItem from '@material-ui/core/ListItem';
// import ListItemIcon from '@material-ui/core/ListItemIcon';
// import ListItemText from '@material-ui/core/ListItemText';
//
// import PersonIcon from '@material-ui/icons/Person';
// import HomeIcon from '@material-ui/icons/Home';
// import StarsIcon from '@material-ui/icons/Stars';
// import SettingsIcon from '@material-ui/icons/Settings';


class Main extends Component {
    classes = useStyles();
    theme = useTheme();

    handleDrawerOpen() {
        this.setState({ open: true });
    }

    handleDrawerClose() {
        this.setState({ open: false });
    }

    constructor(props) {
        super(props);

        this.state = {
            open: true
        };
    }

    componentDidMount() {

    }

    componentWillUnmount() {

    }

    render() {
        return (
            <div className={this.classes.root}>
              <CssBaseline />
              <AppBar
                position="fixed"
                className={clsx(this.classes.appBar, {
                  [this.classes.appBarShift]: this.state.open,
                })}>
              </AppBar>

            </div>

        );
        //return (
        //    <div className={this.classes.root}>
        //    <CssBaseline />
        //    <AppBar
        //    position="fixed"
        //    className={clsx(this.classes.appBar, {
        //        [this.classes.appBarShift]: this.state.open,
        //    })}
        //    >
        //    <Toolbar>
        //    <IconButton
        //    color="inherit"
        //    aria-label="open drawer"
        //    onClick={this.handleDrawerOpen}
        //    edge="start"
        //    className={clsx(this.classes.menuButton, {
        //        [this.classes.hide]: this.state.open,
        //    })}
        //    >
        //    <MenuIcon />
        //    </IconButton>
        //    <Typography variant="h6" noWrap>
        //    Textualize
        //    </Typography>
        //    </Toolbar>
        //    </AppBar>
        //    <Drawer
        //    variant="permanent"
        //    className={clsx(this.classes.drawer, {
        //        [this.classes.drawerOpen]: this.state.open,
        //        [this.classes.drawerClose]: !this.state.open,
        //    })}
        //    classes={{
        //        paper: clsx({
        //            [this.classes.drawerOpen]: this.state.open,
        //            [this.classes.drawerClose]: !this.state.open,
        //        }),
        //    }}
        //    open={this.state.open}
        //    >
        //    <div className={this.classes.toolbar}>
        //    <IconButton onClick={this.handleDrawerClose}>
        //    {this.theme.direction === 'rtl' ? <ChevronRightIcon /> : <ChevronLeftIcon />}
        //    </IconButton>
        //    </div>
        //    <Divider />
        //    <List>
        //    { menuItem( 'Home', <HomeIcon /> )}
        //    { menuItem( 'Contacts', <PersonIcon /> )}
        //    { menuItem( 'Advanced', <StarsIcon /> )}
        //    </List>
        //    <Divider />
        //    <List>
        //    { menuItem( 'Settings', <SettingsIcon /> )}
        //    </List>
        //    </Drawer>
        //    <main className={this.classes.content}>
        //    <div className={this.classes.toolbar} />
        //    <Typography paragraph>
        //    HELLO FUCKER
        //    </Typography>
        //    </main>
        //    </div>
        //);
    }
}

function menuItem(text, icon) {
    return(
        <List>
        <ListItem button key={text}>
        <ListItemIcon>{icon}</ListItemIcon>
        <ListItemText primary={text} />
        </ListItem>
        </List>
    );
}

const drawerWidth = 240;
const useStyles = makeStyles(theme => ({
    root: {
        display: 'flex',
    },
    appBar: {
        zIndex: theme.zIndex.drawer + 1,
        transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
    },
    appBarShift: {
        marginLeft: drawerWidth,
        width: `calc(100% - ${drawerWidth}px)`,
        transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
    },
    menuButton: {
        marginRight: 36,
    },
    hide: {
        display: 'none',
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
        [theme.breakpoints.up('sm')]: {
            width: theme.spacing(7) + 1,
        },
    },
    toolbar: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'flex-end',
        padding: '0 8px',
        ...theme.mixins.toolbar,
    },
    content: {
        flexGrow: 1,
        padding: theme.spacing(3),
    },
}));

export default Main
