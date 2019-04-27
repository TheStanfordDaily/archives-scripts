const AWS = require('aws-sdk');
var Promise = require('bluebird');
var gm = require('gm').subClass({imageMagick: true});
// Promise.promisifyAll(gm.prototype);
const {promisify} = require('util');
const stream = require('stream');
var fs = require("fs");

const s3 = new AWS.S3();
const INPUT_BUCKET = "stanforddailyarchive";
const DEST_BUCKET = "stanforddailyarchive-resized"

//  var params = {
//   Bucket: INPUT_BUCKET, 
//   Key: "data.2012-aug/data/stanford/1920/12/03_01/Stanford_Daily_19201203_0001.pdf"
//  };

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
        newKey = keyMatch[1].replace(".jp2", ".jpg");
    }
    if (key.endsWith(".jp2")) {
        await new Promise(async (resolve, reject) => {
            let result = gm(response.Body).compress("jpeg");
            let buffer = await gmToBuffer(result);
              var params = {Bucket: DEST_BUCKET, Key: newKey, Body: buffer, ContentType: "image/jpeg"};
                  s3.putObject(params, function(err, resp) {
                    if (err) reject(err);
                    else resolve(resp);
                  });
        });
        throw "";
    }
    else if (key.endsWith(".xml")) {
        
    }
    else if (key.endsWith(".pdf")) {
        
    }
    return async () => await null;
}

async function listObjects(params) {
    // try {
     let data = await s3.listObjectsV2(params).promise();
        let ContinuationToken = data["NextContinuationToken"];
        //   console.log(Object.keys(data));           // successful response
        for (i in data.Contents) {
            await processFile(data.Contents[i].Key);
        }
        // await listObjects({...params, ContinuationToken});
    // }
    // catch(err) {
    //   console.log(err); // an error occurred
    // }
 
}

var params = {
    Bucket: INPUT_BUCKET
}

listObjects(params);