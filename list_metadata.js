const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const INPUT_BUCKET = "stanforddailyarchive"

var params = {
    Bucket: INPUT_BUCKET    
};

var metadata = {};
listAllKeys();
function listAllKeys() {
    s3.listObjectsV2(params, function (err, data) {
        if (err) {
            console.log(err, err.stack); // an error occurred
        } else {
            var contents = data.Contents;
            contents.forEach(function (content) {
                let match = content.Key.match(/(\d{4})\/(\d{2})\/(\d{2})_\d*\/.*?-METS\.xml$/);
                if (match) {
                    let year = match[1];
                    let month = match[2];
                    let day = match[3];
                    if (!metadata[year]) metadata[year] = {};
                    if (!metadata[year][month]) metadata[year][month] = {};
                    metadata[year][month][day] = content.Key;
                    console.log(year, month, day);
                }
            });

            if (data.IsTruncated) {
                params.ContinuationToken = data.NextContinuationToken;
                // console.log("get further list...");
                listAllKeys();
            } 
            else {
                params = {Bucket: INPUT_BUCKET, Key: "metadata.json", Body: JSON.stringify(metadata), ContentType: "application/json"};
                console.log("HI");
                s3.putObject(params, (err, data) => {
                    if (err) {
                        console.log(err, err.stack);
                    }
                    else {
                        console.log("upload of metadata.json is complete.");
                    }
                });
            }

        }
    });
}