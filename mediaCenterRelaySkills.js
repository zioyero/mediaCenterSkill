/**
 * This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
 * For additional samples, visit the Alexa Skills Kit developer documentation at
 * https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/getting-started-guide
 */

var http = require('http');
var queryString = require('querystring');



// Route the incoming request based on type (LaunchRequest, IntentRequest,
// etc.) The JSON body of the request is provided in the event parameter.
exports.handler = function (event, context) {
    try {
        console.log("event.session.application.applicationId=" + event.session.application.applicationId);

        /**
         * Uncomment this if statement and populate with your skill's application ID to
         * prevent someone else from configuring a skill that sends requests to this function.
         */
        /*
        if (event.session.application.applicationId !== "amzn1.echo-sdk-ams.app.[unique-value-here]") {
             context.fail("Invalid Application ID");
         }
        */

        if (event.session.new) {
            onSessionStarted({requestId: event.request.requestId}, event.session);
        }

        if (event.request.type === "LaunchRequest") {
            onLaunch(event.request,
                     event.session,
                     function callback(sessionAttributes, speechletResponse) {
                        context.succeed(buildResponse(sessionAttributes, speechletResponse));
                     });
        }  else if (event.request.type === "IntentRequest") {
            onIntent(event.request,
                     event.session,
                     function callback(sessionAttributes, speechletResponse) {
                        console.log("Intent handled callback here");
                        context.succeed(buildResponse(sessionAttributes, speechletResponse));
                     });
        } else if (event.request.type === "SessionEndedRequest") {
            onSessionEnded(event.request, event.session);
            context.succeed();
        }
    } catch (e) {
        context.fail("Exception: " + e);
    }
};

/**
 * Called when the session starts.
 */
function onSessionStarted(sessionStartedRequest, session) {
    console.log("onSessionStarted requestId=" + sessionStartedRequest.requestId
                + ", sessionId=" + session.sessionId);
}

/**
 * Called when the user launches the skill without specifying what they want.
 */
function onLaunch(launchRequest, session, callback) {
    console.log("onLaunch requestId=" + launchRequest.requestId
                + ", sessionId=" + session.sessionId);

    // Dispatch to your skill's launch.
    getWelcomeResponse(callback);
}

/**
 * Called when the user specifies an intent for this skill.
 */
function onIntent(intentRequest, session, callback) {
    console.log("onIntent requestId=" + intentRequest.requestId
                + ", sessionId=" + session.sessionId);

    var intent = intentRequest.intent,
        intentName = intentRequest.intent.name;

    // Dispatch to your skill's intent handlers
    if ("RelayIntent" === intentName) {
        relayMedia(intent, session, callback)
    } else if ("PandoraIntent" === intentName){
        startPandora(intent, session, callback);
    } else if("StopIntent" === intentName){
        stopIntent(intent, session, callback)
    } else if ("ResumeIntent" === intentName){
        resumeIntent(intent, session, callback)
    } else if ("FullscreenIntent" === intentName){
        fullscreenIntent(intent, session, callback)
    } else if ("PlaylistIntent" === intentName){
        youtubePlaylistIntent(intent, session, callback)
    } else if ("NextIntent" === intentName){
        nextIntent(intent, session, callback);
    } else if ("PreviousIntent" === intentName){
        prevIntent(intent, session, callback);
    } else if ("LibraryIntent" === intentName){
        libraryIntent(intent, session, callback)
    } else if ("LibraryShuffleIntent" === intentName){
        libraryShuffleIntent(intent, session, callback)
    } else if ("LibraryLatestIntent" === intentName){
        libraryLatestIntent(intent, session, callback)
    } else if ("MovieIntent" === intentName){
        movieIntent(intent, session, callback)
    } else if ("FastForwardIntent" == intentName){
        fastForwardIntent(intent, session, callback)
    }
    else {
        throw "Invalid intent";
    }
}

/**
 * Called when the user ends the session.
 * Is not called when the skill returns shouldEndSession=true.
 */
function onSessionEnded(sessionEndedRequest, session) {
    console.log("onSessionEnded requestId=" + sessionEndedRequest.requestId
                + ", sessionId=" + session.sessionId);
    // Add cleanup logic here
}

// --------------- Functions that control the skill's behavior -----------------------

function relayMedia(intent, session, callFunc){
    console.log("Relaying media for intent: ")
    console.log(intent)
    var sessionAttributes = {}
    var songName = intent.slots.song.value
    var query = {
        youtube: songName
    };
    var speechResponse = "Sending "+songName+" to media center";
    sendToMediaCenter(query, speechResponse, callFunc)
}

function stopIntent(intent, session, callback){
    console.log("Relaying stop command for intent: ");
    console.log(intent);
    var query = {
        stop: true
    }
    var speechResponse = "Stopping";
    sendToMediaCenter(query, speechResponse, callback)
}

function resumeIntent(intent, session, callback){
    console.log("Relaying resume command for intent: ")
    console.log(intent);
    var query = {
        resume: true
    };
    var speechResponse = "Resuming";
    sendToMediaCenter(query, speechResponse, callback);
}

function fullscreenIntent(intent, session, callback){
    console.log("Relaying fullscreen command for intent: ")
    console.log(intent)
    var query = {
        fullscreen: true
    }
    var speechResponse = "Toggling fullscreen";
    sendToMediaCenter(query, speechResponse, callback)
}

function youtubePlaylistIntent(intent, session, callback){
    console.log("Relaying youtube playlist command for intent: ")
    console.log(intent)
    var playlistName = intent.slots.playlist.value;
    var query = {
        youtubePlaylist: playlistName
    }
    var speechResponse = "Sending the playlist "+playlistName+" to media center";
    sendToMediaCenter(query, speechResponse, callback)
}

function nextIntent(intent, session, callback){
    console.log("Relaying next command for intent: ");
    console.log(intent)
    var query = {
        next: true
    }
    var speechResponse = "Next";
    sendToMediaCenter(query, speechResponse, callback);
}

function prevIntent(intent, session, callback){
    console.log("Relaying next command for intent: ");
    console.log(intent)
    var query = {
        prev: true
    }
    var speechResponse = "Previous";
    sendToMediaCenter(query, speechResponse, callback);
}

function libraryIntent(intent, session, callback){
    console.log("Relaying library command for intent: ")
    console.log(intent)
    var searchQuery = intent.slots.query.value
    var season = intent.slots.season.value
    var episode = intent.slots.episode.value
    var query = {
        plex: searchQuery,
        seasonNum: season, 
        episodeNum: episode
    };
    var speechResponse = "Searching plex for " + searchQuery + " season " + season + " episode " + episode
    sendToMediaCenter(query, speechResponse, callback)
}

function libraryShuffleIntent(intent, session, callback){
    console.log("Relaying library command for intent: ")
    console.log(intent)
    var searchQuery = intent.slots.query.value
    var query = {
        plexShuffle: searchQuery,
    };
    var speechResponse = "Shuffling " + searchQuery;
    sendToMediaCenter(query, speechResponse, callback)
}

function libraryLatestIntent(intent, session, callback){
    console.log("Relaying library command for intent: ")
    console.log(intent)
    var searchQuery = intent.slots.query.value
    var query = {
        plexLatest: searchQuery,
    };
    var speechResponse = "Playing the latest episode of " + searchQuery;
    sendToMediaCenter(query, speechResponse, callback)
}

function movieIntent(intent, session, callback){
    console.log("Relaying library movie command for intent: ")
    console.log(intent)
    var searchQuery = intent.slots.query.value
    var query = {
        movie: searchQuery
    };
    var speechResponse = "Starting the movie "+ searchQuery;
    sendToMediaCenter(query, speechResponse, callback)
}

function fastForwardIntent(intent, session, callback){
    console.log("Relaying fast forward command for intent: ")
    console.log(intent)
    var seconds = intent.slots.seconds.value
    var query = {
        sec: seconds
    };
    var speechResponse = "Fast forwarding "+ seconds + " seconds";
    sendToMediaCenter(query, speechResponse, callback)
}


function getWelcomeResponse(callback){
    callback({}, buildSpeechletResponse("Insulting", "You have to say something, dumbass!", null, true))
}


// --------------- Helpers that send to media center

/**
 * Sends a query to the media center and instructs alexa to utter the given speech output.
 */
function sendToMediaCenter(query, speechOutput, callback){
    var httpQuery = queryString.stringify(query)
    var httpCallback = function(response){
        console.log('done');
        callback({}, buildSpeechletResponse("Relaying", speechOutput, null, true))
    }
    console.log("Making request to")
    var options = {
        host: "host",
        port: 1234,
        path: "?"+httpQuery
    }
    console.log(options)
    http.request(options, httpCallback).end();
}


// --------------- Helpers that build all of the responses -----------------------

function buildSpeechletResponse(title, output, repromptText, shouldEndSession) {
    return {
        outputSpeech: {
            type: "PlainText",
            text: output
        },
        card: {
            type: "Simple",
            title: "SessionSpeechlet - " + title,
            content: "SessionSpeechlet - " + output
        },
        reprompt: {
            outputSpeech: {
                type: "PlainText",
                text: "Sorry, I couldn't hear you. What do you want the media center to do?"
            }
        },
        shouldEndSession: shouldEndSession
    };
}

function buildResponse(sessionAttributes, speechletResponse) {
    return {
        version: "1.0",
        sessionAttributes: sessionAttributes,
        response: speechletResponse
    };
}