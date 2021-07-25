import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import CssBaseline from '@material-ui/core/CssBaseline';
import { makeStyles } from '@material-ui/core/styles';
import { render } from 'react-dom';

const useStyles = makeStyles((theme) => ({
    appBar: {
        borderBottom: `1px solid ${theme.palette.divider}`,
        alignItems: 'center',
    },
}))

function Header() {
    const classes = useStyles();
    return (
        <React.Fragment>
            <CssBaseline></CssBaseline>
            <AppBar
                position="static"
                color="#FFFFFF"
                elevation={0}
                className={classes.appBar}
            >
                <Toolbar>
                    <Typography align="center" variant="subtitle1" color="inherit" noWrap>Made By Hamed</Typography>
                </Toolbar>
            </AppBar>
        </React.Fragment>
    );
}

export default Header;