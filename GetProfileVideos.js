const puppeteer = require('puppeteer-extra');
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
var fs = require('fs');
const readline = require('readline');
puppeteer.use(StealthPlugin());

async function getLinks(url){
	console.log('Collecting links from ' + url)

    const browser = await puppeteer.launch({
        headless: true,
        args: ['--disable-dev-shm-usage']
    });
    const page = await browser.newPage();
	await page.setRequestInterception(true);
    page.on('request', (req) => {
        if(req.resourceType() == 'stylesheet' || req.resourceType() == 'font' || req.resourceType() == 'image'){
        req.abort();
        }
        else {
        req.continue();
        }
    });	

    await page.setViewport({
        width: 1200,
        height: 800
    });
	await page.goto(url);

    await autoScroll(page);

    //get all links
	const hrefs = await page.$$eval('a', as => as.map(a => a.href));

	function starts(item){
		return item.startsWith(url);
	}	
	const results = hrefs.filter(starts);

	console.log('Saving links from ' + url)

	for (var result of results){
		var dict = {};
		dict['Url'] = result;
		var content = JSON.stringify(dict);
		fs.appendFile('Data/VideosTemp.json',content+'\n',function (err) {
			if (err) throw err;
		});
	}
	await browser.close();

}

async function autoScroll(page){
    await page.evaluate(async () => {
	@@ -50,4 +69,31 @@ async function autoScroll(page){
            }, 100);
        });
    });
}


async function readJson(file){
  const fileStream = fs.createReadStream(file);

  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });
  // Note: we use the crlfDelay option to recognize all instances of CR LF
  // ('\r\n') in input.txt as a single line break.
  var dataframe = [];
  for await (const line of rl) {
    var obj=JSON.parse(line);
    dataframe.push(obj['Url']);
  }
  return dataframe;
}

async function run(){
	urls = await readJson('Data/UserMetadata.json');
	for (var url of urls){
		await getLinks(url);
	}
}

run();