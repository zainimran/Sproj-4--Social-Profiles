var datum = require('C:\\Users\\shehrozsaghir\\Desktop\\Sproj\\Sproj-4--Social-Profiles\\Text Analytics\\node-datumbox').factory("c5a80c5cd1f7b44f121971da0ddc9497");
var data = "The Lahore University of Management Sciences (LUMS) is a national university, established by sponsors belonging to the country’s leading private and public sector corporations. The goal of the sponsors is to develop an institution, which would provide rigorous academic and intellectual training and a viable alternative to education comparable to leading universities across the world."

datum.sentimentAnalysis("I like it.", function(err, data) {
    if ( err )
        return console.log(err);

    console.log(data);  // Remarks here.
});

datum.sentimentAnalysis("What the fuck.", function(err, data) {
    if ( err )
        return console.log(err);

    console.log(data);  // Remarks here.
});

datum.topicClassification(data, function(err, data) {
    if ( err )
        return console.log(err);

    console.log(data);  // Remarks here.
});