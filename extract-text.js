/*
 * This script fetches all papers for a particular year, extracts the text,
 * and then puts them into the appropriate text file in the destination directory.
 * Usage: node extract-text.js 1892
 *
 */
const {fetchAllPapers} = require("@thestanforddaily/archives-web/lib/helpers/papers");
const fs = require("fs");

if (process.argv.length < 2) {
    throw "Please specify a year as a command-line argument.";
}
const year = parseInt(process.argv[2]);
const OUTPUT_DIR = "output";

main();

async function main() {
    let papers = await fetchAllPapers();
    for (let i in papers) {
        let paper = papers[i];
        if (paper.date.getFullYear() < parseInt(process.argv[2])) {
            continue;
        }
        console.log(paper.date);
        let pages = await paper.getPages();
        for (let i in pages) {
            let page = pages[i];
            await page.getAltoData();
            let month = page.date.getMonth() + 1;
            month = (month < 10) ? "0" + month : "" + month;
            let date = page.date.getDate();
            date = (date < 10) ? "0" + date : "" + date;
            let year = "" + page.date.getFullYear();
            let dir = `${OUTPUT_DIR}/${year}/${month}/${date}`;
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
                let text = [await page.getSectionText(section)]; 
                const process = e => e.replace(/\n/g, " ");
                if (!fs.existsSync(path)) {
                   text = ["# " + process(section.title), "## " + process(section.subtitle), "### " + process(section.author), ...text];
                }
                text = text.join("\n"); 
                await new Promise(function(resolve, reject) {
                    fs.appendFile(path, text, function(err) {
                        if (err) reject(err);
                        else resolve();
                    });
                });
            }
            pages[i] = null;
        }
        papers[i] = null;
    }
}
