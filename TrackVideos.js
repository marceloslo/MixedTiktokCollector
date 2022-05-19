var fs = require('fs'); 
const readline = require('readline');
const puppeteer = require('puppeteer')

//reads the usermetadata json and stores its urls
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

//gets data of xp(X-Path) of a given page
async function getMetadata(page,xp){
  await page.waitForXPath(xp);
  let [info] = await page.$x(xp);
  const result = await page.evaluate(name => name.innerText, info);
  return result;
}

async function getvideoLikeCount(page){
  const res = await getMetadata(page,'/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[3]/button[1]/strong');
  return res;
}
async function getvideoCommentCount(page){
    const res = await getMetadata(page,'/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[3]/button[2]/strong');
    return res;
  }
  async function getvideoSharesCount(page){
    const res = await getMetadata(page,'/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[3]/button[3]/strong');
    return res;
  }
async function getprofileId(page){
  const res = await getMetadata(page,'/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div/a[2]/span[1]');
  return res;
}
async function getvideoDescription(page){
    const res = await getMetadata(page,'/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/span');
    return res;
  }

async function getvideoPublicationDate(page){
    await page.waitForXPath('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div/a[2]/span[2]/span[2]');
    let [info] = await page.$x('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div/a[2]/span[2]/span[2]');
    const PublicationDate = await page.evaluate(name => name.innerText, info);
    var actualDate=PublicationDate;
    if (PublicationDate.indexOf("d")>-1){
        var days = parseInt(PublicationDate.replace( /^\D+/g, ''));
        actualDate = new Date(new Date().getTime() - (days * 24 * 60 * 60 * 1000))
        actualDate = actualDate.toISOString().replace('T', ' ').substring(0, 10);
    }
    else if(PublicationDate.indexOf("w")>-1){
        var weeks = parseInt(PublicationDate.replace( /^\D+/g, ''));
        actualDate = new Date(new Date().getTime() - (weeks * 7 * 24 * 60 * 60 * 1000))
        actualDate = actualDate.toISOString().replace('T', ' ').substring(0, 10);
    }
    else if(!(PublicationDate.indexOf("202")>-1)){
        var currentYear = (new Date().getFullYear()).toString();
        actualDate=currentYear+"-"+PublicationDate;
    }
    return actualDate;
  }

//gets date in format YYYY-MM-DD
async function getCollectionDate(){
  return new Date().toISOString().replace('T', ' ').substring(0, 10);
}

//checks if video exists(True or False)
async function videoExists(page){
  try{
    //this xpath corresponds to removed video
    const res = await getMetadata(page,'/html/body/div[2]/div[2]/div[2]/div[1]/div/p[1]');
    return 0;
  }
  catch(err){
    return 1;
  }
}

//gets metadata in json format
async function getAndFormat(url,page){
  var exists = videoExists(page);
  if(exists){
    var stats = {};
    stats["Url"]=url;
    stats["UserId"]=await getprofileId(page);
    stats["Description"] = await getvideoDescription(page);
    stats["LikeCount"] = await getvideoLikeCount(page);
    stats['SharesCount'] = await getvideoSharesCount(page);
    stats['CommentCount'] = await getvideoCommentCount(page);
    stats['PublicationDate'] = await getvideoPublicationDate(page);
    stats["CollectionDate"] = await getCollectionDate();
    stats["Status"]= 1;
    return stats;
  }
  else{
    var stats = {"Url":self.url,"UserId":"","Description":"","LikeCount":"","CommentCount":"","SharesCount":"","PublicationDate":"","Status":0}
    stats["CollectionDate"] = await getCollectionDate();
    return stats;
  }
}

//Add all videos' metadata in the csv file to the json file
async function trackVideos(){
  const browser = await puppeteer.launch({ headless: true,args: [
    '--window-size=1920,1080']});
  const page = await browser.newPage();
  const urls = await readJson('Data/VideoMetadata.json');
  results=[];
  for(var url of urls)
  {
    console.log(url);
    await page.goto(url);
    var result = await getAndFormat(url,page);
    results.push(result);
  }
  for(var result of results)
  {
    var content = JSON.stringify(result);
    fs.appendFile('Data/VideoLogging.json',content+'\n',function (err) {
      if (err) throw err;
    });
  }
  await browser.close()
}

trackVideos();