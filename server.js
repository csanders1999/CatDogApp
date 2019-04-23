// Based on:
// https://stackoverflow.com/questions/39845526/how-to-serve-an-angular2-app-in-a-node-js-server
// https://www.npmjs.com/package/python-shell
/*
Put content of angular2 build into 'public' folder.
Host index.html of angular project on localhost:4000
*/
const html = './catdog-app/dist/catdog-app';

const path = require('path');
const {PythonShell} = require('python-shell')

const hostname = '127.0.0.1';
const port = 4000;

// Express
const compression = require('compression');
const express = require('express');
var app = express();

app
    .use(compression())
    .use(express.json())
    // Static content
    .use(express.static(html))
    // When a username is posted to the app, run python files on it for analysis and send back
    // analysis data to be displayed on frontend
    .use('/user', function (req, res) {
      // Get user and prepare constant for analysis object
      const user = req.body.user
    
      // Run pyton file(s) with the username
      // Create child process for python script
      let pyshell = new PythonShell('analysis.py', {args: [JSON.stringify({username: user})]})
      let dataString = '';

      // When python prints the analysis dictionary, save that to return in response body
      pyshell.stdout.on('data', function(data){
        dataString += data;
      });
      // Allow the script to end
      pyshell.end(function(err, code, signal) {
        if (err) throw err;
        console.log('The exit code was: ' + code);
        console.log('finished');
      });
      
      // Send back dictionary of analysis, allowing time for script to run
      res.set('Content-Type', 'application/json');
      setTimeout(() => res.send(dataString), 500)
    })
    // Default route
    .use(function(req, res) {
      res.sendFile(path.join(__dirname, './catdog-app/dist/catdog-app', 'index.html'));
    })
    // Start server
    .listen(port, hostname, function () {
        console.log('Port: ' + port);
        console.log('Html: ' + html);
    });

// continue with api code below ...