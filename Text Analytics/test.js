var datum = require('C:\\Users\\shehrozsaghir\\Desktop\\Sproj\\Sproj-4--Social-Profiles\\Text Analytics\\node-datumbox').factory("c5a80c5cd1f7b44f121971da0ddc9497");
var data = "The Lahore University of Management Sciences (LUMS) is a national university, established by sponsors belonging to the country’s leading private and public sector corporations. The goal of the sponsors is to develop an institution, which would provide rigorous academic and intellectual training and a viable alternative to education comparable to leading universities across the world."
var data2 = "The National University of Sciences and Technology (NUST) aims to emerge as a leading research intensive university of Pakistan, comparable to the top universities of the world within the next 10 years. It will be a comprehensive, residential university, responsive to technological change, dedicated to excellence and committed to international education perspective. The University will fulfill its responsibility of graduating culturally enlightened, technologically knowledgeable, and academically competent and research-oriented productive citizens who are prepared to lead, to inspire, and to serve humanity. The University commits itself and all its resources to this trust and responsibility."

datum.documentSimilarity(data, data2, function(err, data) {
    if ( err )
        return console.log(err);

    console.log("Document Similarity: ", data);  // Remarks here.
});

datum.sentimentAnalysis("I like it.", function(err, data) {
    if ( err )
        return console.log(err);

    console.log("Sentiment Analysis: ", data);  // Remarks here.
});

datum.sentimentAnalysis("I am a man.", function(err, data) {
    if ( err )
        return console.log(err);

    console.log("Sentiment Analysis: ", data);  // Remarks here.
});

datum.twitterSentimentAnalysis("What the fuck.", function(err, data) {
    if ( err )
        return console.log(err);

    console.log("Twitter Sentiment Analysis: ", data);  // Remarks here.
});

datum.topicClassification(data, function(err, data) {
    if ( err )
        return console.log(err);

    console.log("Topic Classification: ", data);  // Remarks here.
});

datum.topicClassification(data2, function(err, data) {
    if ( err )
        return console.log(err);

    console.log("Topic Classification: ", data);  // Remarks here.
});

datum.educationalDetection(data, function(err, data) {
    if ( err )
        return console.log(err);

    console.log("Educational Detection: ", data);  // Remarks here.
});

datum.keywordExtraction(data, 2, function(err, data) {
    if ( err )
        return console.log(err);

    console.log("KeyWord Extraction:\n", data);  // Remarks here.
});