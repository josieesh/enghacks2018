/**
 * This is the main file of the application. Run it with the
 * `node server.js` command from your terminal
 *
 * Remember to run `npm install` in the project folder, so
 * all the required libraries are downloaded and installed.
 */

var express = require('express');

// Create a new express.js web app:

var app = express();

// Configure express with the settings found in
// our config.js file

require('./config')(app);

// Add the routes that the app will react to,
// as defined in our routes.js file

require('./routes')(app);

var port = process.env.PORT || 3000;
app.use(express.static(__dirname + '/public'));

// This file has been called directly with
// `node index.js`. Start the server!

app.listen(port);
console.log('Your application is running on ' +port);


/*const express = require('express')
const app = express()

app.get('/', (req, res) => res.send('Hello World!'))

app.listen(3000, () => console.log('Example app listening on port 3000!'))*/
