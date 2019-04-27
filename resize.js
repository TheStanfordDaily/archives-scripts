const AWS = require('aws-sdk');
var gm = require('gm').subClass({imageMagick: true});

const s3 = new AWS.S3();
const INPUT_BUCKET = "stanforddailyarchive";
const DEST_BUCKET = "stanforddailyarchive-resized"

function gmToBuffer (data) {
    return new Promise((resolve, reject) => {
      data.stream((err, stdout, stderr) => {
        if (err) { return reject(err) }
        const chunks = []
        stdout.on('data', (chunk) => { chunks.push(chunk) })
        // these are 'once' because they can and do fire multiple times for multiple errors,
        // but this is a promise so you'll have to deal with them one at a time
        stdout.once('end', () => { resolve(Buffer.concat(chunks)) })
        stderr.once('data', (data) => { reject(String(data)) })
      })
    })
  }

async function processFile(key) {
    let params = {
        Bucket: INPUT_BUCKET,
        Key: key
    }
    let response = await s3.getObject(params).promise();
    let keyMatch = key.match(/.*\/(.*)?$/);
    let newKey = key;
    if (keyMatch && keyMatch.length >= 2) {
        newKey = keyMatch[1];
    }
    console.log(newKey);
    if (key.endsWith(".jp2")) {
        newKey = newKey.replace(".jp2", ".jpg");
        let result = gm(response.Body).quality(80).compress("jpeg");
        let buffer = await gmToBuffer(result);
        let params = {Bucket: DEST_BUCKET, Key: newKey, Body: buffer, ContentType: "image/jpeg"};
        await s3.putObject(params).promise();
    }
    else if (key.endsWith(".xml")) {
      let params = {Bucket: DEST_BUCKET, Key: newKey, Body: response.Body, ContentType: "text/xml"};
          await s3.putObject(params).promise();
    }
    else if (key.endsWith(".pdf")) {
        
    }
    return async () => await null;
}

async function listObjects(params) {
    let data = await s3.listObjectsV2(params).promise();
    let ContinuationToken = data["NextContinuationToken"];
    for (i in data.Contents) {
        await processFile(data.Contents[i].Key);
    }
    await listObjects(key, {...params});
}



async function main() {
   var params = {
        Bucket: INPUT_BUCKET
   }
   await listObjects(params);
}

main();