const AWS = require('aws-sdk');
var Promise = require('bluebird');
var gm = require('gm').subClass({imageMagick: true});

const s3 = new AWS.S3();
const BUCKET = "stanforddailyarchive-resized"

let keys = [];
async function listObjects(params) {
    let data = await s3.listObjectsV2(params).promise();
    let ContinuationToken = data["NextContinuationToken"];
    for (i in data.Contents) {
        let key = data.Contents[i].Key;
        if (key !== "metadata.json") {
            console.log(key);
            keys.push(key);   
        }
    }
}

async function main() {
    let params = {
        Bucket: INPUT_BUCKET
    }
    
    await listObjects(params);
    let metadata = {
        "keys": keys,
        "metadata_generation_date": new Date()
    }
    params = {Bucket: BUCKET, Key: "metadata.json", Body: JSON.stringify(metadata), ContentType: "image/jpeg"};
    await s3.putObject(params).promise();
}