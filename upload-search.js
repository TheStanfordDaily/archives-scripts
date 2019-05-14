const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const INPUT_BUCKET = "stanforddailyarchive";
const {fetchAllPapers} = require("@thestanforddaily/archives-web/lib/helpers/papers");
const fs = require("fs");

main();

async function main() {
    // let params = {Bucket: INPUT_BUCKET, Key: "metadata.json"};
    // let response = await s3.getObject(params).promise();
    // let metadata = JSON.parse(response.Body.toString());
    // for (let year in metadata) {
    //     console.log(year);
    // }
    let papers = await fetchAllPapers();
    for (let i in papers) {
        let paper = papers[i];
        if (paper.date.getFullYear() < 1921) {
            console.log("skipping paper", paper.date);
            continue;
        }
        let pages = await paper.getPages();
        for (let page of pages) {
            await page.getAltoData();
            let dir = `text/${page.date.getFullYear()}/${page.date.getMonth() + 1}/${page.date.getDate()}`;
            await new Promise(function(resolve, reject) {
                fs.mkdir(dir, { recursive: true }, (err) => {
                  if (err) reject(err);
                  else resolve();
                });
            });
            for (let section of page.sections) {
                //   PageSection {
                //     type: 'ARTICLE',
                //     title: 'Young Republicans.',
                //     sectionID: 'MODSMD_ARTICLE4',
                //     areaIDs: [ 'P1_TB00014', 'P1_TB00015' ] },
                let path = `${dir}/${section.sectionID}.txt`;
                if (fs.existsSync(path)) {
                    console.log("skipping", path);
                    continue;   
                }
                console.log(path, section.title);
                let text = await page.getSectionText(section);
                await new Promise(function(resolve, reject) {
                    fs.writeFile(path, text, function(err) {
                        if (err) reject(err);
                        else resolve();
                    });
                });
                // break;
            }
            // break;
        }
        papers[i] = null;
        // break;
    }
}