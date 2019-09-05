import React, { Component } from 'react';
import SideNav, { Toggle, Nav, NavItem, NavIcon, NavText } from '@trendmicro/react-sidenav';

import '@trendmicro/react-sidenav/dist/react-sidenav.css';
import './stylesheets/App.css';

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUser, faTable, faCog, faHome } from '@fortawesome/free-solid-svg-icons'

import Onboard from './components/setup/Onboard'
import Main from './components/stats/Main'
import Contact from './components/stats/Contact'
import Table from './components/stats/Table'

library.add(faUser)
library.add(faTable)
library.add(faCog)
library.add(faHome)

class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            setup: false,
            preprocessed: false,
            contacts: [],
            selected: "Home",
            name: "Home"
        };

        this.display_page = this.display_page.bind(this);
        this.display_name = this.display_name.bind(this);
        this.callback = this.callback.bind(this);
    }

    componentDidMount() {
        fetch("http://127.0.0.1:5000/api/data/src", {
            method: "GET",
            mode:"cors",
            dataType: "application/json"
        })
        .then(r => r.json())
        .then(data => {
            if ( !(data === "")) {
                this.callback()
            }
        });
    }

    callback() {
        this.setState({ setup: true });
        fetch("http://127.0.0.1:5000/api/data/setup", {
            method: "POST",
            mode:"cors",
            dataType: "application/json"
        })
        .then(r => r.json())
        .then(data => {

            fetch("http://127.0.0.1:5000/api/convos", {
                method: "GET",
                mode:"cors",
                dataType: "application/json"
            })
            .then(r => r.json())
            .then(data => {
                this.setState({ preprocessed: true,
                                contacts: data });
            });
        });
    }

    setup() {
        return (
        <div className="App">
            <Onboard callback={this.callback}/>
        </div>);
    }

    loading() {
        return (
        <div className="App">
            <div className="Page-header">
            We're Working On It
            </div>
            <h3> This can take up to a minute to complete</h3>
        </div>);
    }

    render() {
        if (!this.state.setup) {
            return this.setup();
        }

        if (!this.state.preprocessed) {
            return this.loading();
        }

        return (
                <div className="App">
                    <SideNav onSelect={(selected) => {
                        this.setState({ selected: selected });
                    }}>
                        <Toggle />
                        <Nav defaultSelected={this.state.selected}>
                        <NavItem eventKey="Home">
                        <NavIcon>
                        <FontAwesomeIcon icon="home" />
                        </NavIcon>
                        <NavText>
                        Home
                        </NavText>
                        </NavItem>
                        <NavItem eventKey="Contacts">
                        <NavIcon>
                        <FontAwesomeIcon icon="user" />
                        </NavIcon>
                        <NavText>
                        Contacts
                        </NavText>
                        { this.contacts(this.state.contacts) }
                        </NavItem>
                        <NavItem eventKey="Table">
                        <NavIcon>
                        <FontAwesomeIcon icon="table" />
                        </NavIcon>
                        <NavText>
                        Table
                        </NavText>
                        </NavItem>
                        <NavItem eventKey="Settings">
                        <NavIcon>
                        <FontAwesomeIcon icon="cog" />
                        </NavIcon>
                        <NavText>
                        Settings
                        </NavText>
                        </NavItem>
                        </Nav>
                    </SideNav>
                    <div className="App-body">
                    <div className="Page-header">
                        {this.display_name(this.state.selected)}
                    </div>
                    { this.display_page(this.state.selected) }
                    </div>
                </div>);
    }

    contacts(contacts) {
        if (!contacts) {
            return ({});
        }
        debugger;
        console.log('fucker');

        const contact_elements = contacts.map((val, index) => {
            return (
                <NavItem key={val.number} eventKey={ "Contacts/" + index }>
                <NavText>
                { val.name }
                </NavText>
                </NavItem>
            )});

        return (contact_elements);
    }

    display_page(selected) {
        if (selected === "Home") {
            return (<Main/>);
        }

        if (selected === "Table") {
            return (<Table/>);
        }

        if (selected.indexOf("Contacts/") === 0) {
            const index = parseInt(selected.replace("Contacts/", ""));
            const num = this.state.contacts[index].number;
            return (<Contact cache key={num} number={num}/>);
        }

        return <h1>Missing Page</h1>
    }

    display_name(selected) {
        if (selected.indexOf("Contacts/") === 0) {
            const index = parseInt(selected.replace("Contacts/", ""));
            return this.state.contacts[index].name;
        }

        return selected;
    }
}

export default App;
