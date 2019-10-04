import React, {useEffect, useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Header from './Header';
import { LoadModule, Module } from './data_modules/Module';

function Contact({ match }) {
    const id = match.params.id;
    const API = 'http://127.0.0.1:5000/api/';
    const [name, setName] = useState('');
    const [langData, setLangData] = useState({});

    const classes = makeStyles(theme => ({
      root: {
        flexGrow: 1,
      },
    }))

    useEffect(() => {
        const src = API + id.toString() + '/info';
        const header = {
            method: "GET",
            mode: "cors",
            dataType: "application/json"
        };
        fetch(src, header)
        .then(r => r.json())
        .then(result => setName(result['name']))
        .catch(error => {
            console.error(error);
            debugger
        })
    }, [id, setName]);

    useEffect(() => {
        const src = API + 'stats/' + id.toString() + '/language';
        const header = {
            method: "GET",
            mode: "cors",
            dataType: "application/json"
        };
        fetch(src, header)
        .then(r => r.json())
        .then(result => setLangData(result))
        .catch(error => {
            console.error(error);
        })
    }, [id]);

    const crumbs = [{'url': '/contacts', 'label': 'Contacts'}];
    return (
        <div className={classes.root}>
            <Header title={name} crumbs={crumbs} />
            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <LoadModule title="Frequency"
                    endpoint={'stats/' + id.toString() + '/frequency'}
                    type="line"/>
                </Grid>
            </Grid>
            <Header title="Emoji" />
            <Header title="Language" />
            <Grid container spacing={3}>
                <Grid item xs={3}>
                    <Module title="Average Wordlength Sent"
                    data={langData ? langData['sent_avg_wordlen'] : {}}
                    type="simple"/>
                </Grid>
                <Grid item xs={3}>
                    <Module title="Average Word Length R"
                    data={langData ? langData['received_avg_wordlen'] : {}}
                    type="simple"/>
                </Grid>
                <Grid item xs={3}>
                    <Module title="English Words (sent)"
                    data={langData ? langData['sent_perc_proper'] : {}}
                    type="simple"/>
                </Grid>
                <Grid item xs={3}>
                    <Module title="English Words (received)"
                    data={langData ? langData['received_perc_proper'] : {}}
                    type="simple"/>
                </Grid>
                <Grid item xs={3}>
                    <Module title="Readability (s)"
                    data={langData ? langData['sent_readability'] : {}}
                    type="simple"/>
                </Grid>
                <Grid item xs={3}>
                    <Module title="Readability (r)"
                    data={langData ? langData['received_readability'] : {}}
                    type="simple"/>
                </Grid>
                <Grid item xs={12}>
                    <Module title="Wordcloud"
                    data={langData ? langData['received_readability'] : {}}
                    type="word_cloud"/>
                </Grid>
            </Grid>
            <Header title="Sentiment" />
        </div>
    );
}

export default Contact
