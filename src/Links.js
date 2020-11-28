// https://github.com/mui-org/material-ui/tree/master/docs/src/pages/getting-started/templates/checkout
import React from "react";
import { Link as RouterLink } from "react-router-dom";
import {
  makeStyles,
  Typography,
  List,
  ListItem,
  ListItemSecondaryAction,
  Link,
  IconButton,
} from "@material-ui/core";
import HistoryIcon from "@material-ui/icons/History";
import SettingsIcon from "@material-ui/icons/Settings";

import Page from "./Page";
import * as server from "./server";

const useStyles = makeStyles((theme) => ({
  root: {
    "& a.MuiLink-root": {
      flex: 1,
    },
  },
  configure: {
    right: "50px",
  },
}));

export default function Links() {
  let classes = useStyles();
  let configs = server.get_configs();
  let user = server.get_user();

  return (
    <Page title="Choose Waiver" contentWidth={400} showUser showCopyright>
      {!user && <Typography variant="h3">Demo</Typography>}
      <List component="nav" className={classes.root}>
        {configs.map((config) => (
          <ListItem button key={config}>
            <Link component={RouterLink} to={`/${config}`}>
              {config}
            </Link>
            <ListItemSecondaryAction className={classes.configure}>
              <RouterLink to={`/${config}/configure`}>
                <IconButton edge="end" aria-label="configure">
                  <SettingsIcon />
                </IconButton>
              </RouterLink>
            </ListItemSecondaryAction>
            <ListItemSecondaryAction>
              <RouterLink to={`/${config}/submissions`}>
                <IconButton edge="end" aria-label="submissions" color="primary">
                  <HistoryIcon />
                </IconButton>
              </RouterLink>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
        {!configs.length && (
          <Typography align="center" color="textSecondary">
            No waivers setup for {user}
          </Typography>
        )}
      </List>
    </Page>
  );
}
