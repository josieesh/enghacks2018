/**
 * This file defines the routes used in your application
 * It requires the database module that we wrote previously.
 */

var db = require('./database'),
    dilemmas = db.dilemmas,
    users = db.users;

module.exports = function(app){

    // Homepage
    app.get('/', function(req, res){

        // Find all dilemmas
        dilemmas.find({}, function(err, all_dilemmas){

            // Find the current user
            users.find({ip: req.ip}, function(err, u){

                var voted_on = [];

                if(u.length == 1){
                    voted_on = u[0].votes;
                }

                // Find which dilemmas the user hasn't still voted on

                var not_voted_on = all_dilemmas.filter(function(dilemma){
                    return voted_on.indexOf(dilemma._id) == -1;
                });

                var dilemma_to_show = null;

                if(not_voted_on.length > 0){
                    // Choose a random dilemma from the array
                    dilemma_to_show = not_voted_on[Math.floor(Math.random()*not_voted_on.length)];
                }

                res.render('home', { dilemma: dilemma_to_show });

            });

        });

    });

    app.get('/standings', function(req, res){

        dilemmas.find({}, function(err, all_dilemmas){

            // Sort the dilemmas

            /*all_dilemmas.sort(function(p1, p2){
                return (p2.likes - p2.dislikes) - (p1.likes - p1.dislikes);
            });*/

            // Render the standings template and pass the dilemmas
            res.render('standings', { standings: all_dilemmas });

        });

    });

    // This is executed before the next two post requests
    app.post('*', function(req, res, next){

        // Register the user in the database by ip address

        users.insert({
            ip: req.ip,
            votes: []
        }, function(){
            // Continue with the other routes
            next();
        });

    });

    app.post('/a', vote);
    app.post('/b', vote)

    function vote(req, res){

        // Which field to increment, depending on the path

        var what = {
            '/a': {a:1},
            '/b': {b:1}
        };

        // Find the dilemma, increment the vote counter and mark that the user has voted on it.

        dilemmas.find({ name: req.body.dilemma }, function(err, found){

            if(found.length == 1){

                dilemmas.update(found[0], {$inc : what[req.path]});

                users.update({ip: req.ip}, { $addToSet: { votes: found[0]._id}}, function(){
                    res.redirect('../');
                });

            }
            else{
                res.redirect('../');
            }

        });
    }
  };
