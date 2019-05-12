const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const INPUT_BUCKET = "stanforddailyarchive";
const {fetchAllPapers} = require("@thestanforddaily/archives-web/lib/helpers/papers");


main();

async function main() {
    // let params = {Bucket: INPUT_BUCKET, Key: "metadata.json"};
    // let response = await s3.getObject(params).promise();
    // let metadata = JSON.parse(response.Body.toString());
    // for (let year in metadata) {
    //     console.log(year);
    // }
    let papers = await fetchAllPapers();
    return papers;
}