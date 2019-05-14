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
        if (process.argv.length > 2 && !isNaN(process.argv[2]) && paper.date.getFullYear() < parseInt(process.argv[2])) {
            console.log("skipping paper", paper.date);
            continue;
        }
        console.log("processing paper", paper.date);
        let pages = await paper.getPages();
        for (let page of pages) {
            await page.getAltoData();
            let month = page.date.getMonth() + 1;
            month = (month < 10) ? "0" + month : "" + month;
            let date = page.date.getDate();
            date = (date < 10) ? "0" + date : "" + date;
            let year = "" + page.date.getFullYear();
            let yearx = year.slice(0, 3) + "x";
            let yearxx = year.slice(0, 2) + "xx";
            let dir = `text3/${yearxx}/${yearx}/${year}/${month}m/${date}d`;
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
                let path = `${dir}/${section.sectionID}.${section.type.toLowerCase()}.txt`;
                if (fs.existsSync(path)) {
                    console.log("skipping", path);
                    continue;   
                }
                // console.log(path, section.title, section.subtitle, section.author);
                let text = ["# " + section.title, "## " + section.subtitle, "### " + section.author, await page.getSectionText(section)].join("\n");
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