// Require the nedb module
var Datastore = require('nedb'),
    fs = require('fs');

// Initialize two nedb databases. Notice the autoload parameter.
var dilemmas = new Datastore({ filename: __dirname + '/data/dilemmas', autoload: true }),
    users = new Datastore({ filename: __dirname + '/data/users', autoload: true });

// Create a "unique" index for the photo name and user ip
dilemmas.ensureIndex({fieldName: 'name', unique: true});
users.ensureIndex({fieldName: 'ip', unique: true});

// Load all images from the public/photos folder in the database
var dilemmas_on_disk = fs.readdirSync(__dirname + '/public/dilemmas');

// Insert the photos in the database. This is executed on every
// start up of your application, but because there is a unique
// constraint on the name field, subsequent writes will fail
// and you will still have only one record per image:

dilemmas_on_disk.forEach(function(dilemma){
    dilemmas.insert({
        name: dilemma,
        a: 0,
        b: 0
    });
});

// Make the photos and users data sets available to the code
// that uses require() on this module:

module.exports = {
    dilemmas: dilemmas,
    users: users
};
