var fs = require('fs'); 
const readline = require('readline');
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

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
async function getMetadata(page,xp){
  await page.waitForXPath(xp,{timeout: 10000});
  let [info] = await page.$x(xp);
  const result = await page.evaluate(name => name.innerText, info);
  return result;
}
async function getProfileName(page){
  const res = await getMetadata(page,'/html/body/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/h1');
  return res;
}
async function getProfileBio(page){
  const res = await getMetadata(page,'/html/body/div[2]/div[2]/div[2]/div/div[1]/h2[2]');
  return res;
}
async function getProfileFollowers(page){
  const res = await getMetadata(page,'/html/body/div[2]/div[2]/div[2]/div/div[1]/h2[1]/div[2]/strong');
  return res;
}
async function getProfileLikeCount(page){
  const res = await getMetadata(page,'/html/body/div[2]/div[2]/div[2]/div/div[1]/h2[1]/div[3]/strong');
  return res;
}
async function getProfileFollowing(page){
  const res = await getMetadata(page,'/html/body/div[2]/div[2]/div[2]/div/div[1]/h2[1]/div[1]/strong');
  return res;
}
async function getProfileId(page){
  const res = await getMetadata(page,'/html/body/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/h2');
  return res;
}
async function getCollectionDate(){
  return new Date().toISOString().replace('T', ' ').substring(0, 10);
}

async function getRemovalMessage(page){
    const res = await getMetadata(page,'/html/body/div[2]/div[2]/div[2]/div/main/div/p[1]');
    return res;
}
async function ProfileExists(page){
  try{
    const res = await getMetadata(page,'/html/body/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/h1');
    return 1;
  }
  catch(err){
    return 0;
  }
}
async function getAndFormat(url,page){
  var exists = await ProfileExists(page);
  if(exists){
    var stats = {};
    stats["Url"]=url;
    stats['User']= await getProfileName(page);
    stats["UserId"]=await getProfileId(page);
    stats["Description"] = await getProfileBio(page);
    stats["LikeCount"] = await getProfileLikeCount(page);
    stats["Followers"] = await getProfileFollowers(page);
    stats["Following"] = await getProfileFollowing(page);
    stats["CollectionDate"] = await getCollectionDate();
    stats["Status"]= 1;
    return stats;
  }
  else{
    var stats = {"Url":url,'User':"","UserId":"","ProfileBio":"","Followers":"","Following":"","LikeCount":"","Status":0}
    stats["CollectionDate"] = await getCollectionDate();
	stats["Description"] = await getRemovalMessage(page);
    return stats;
  }
}
async function TrackUsers(){
  const browser = await puppeteer.launch({headless:true,defaultViewport:{
        width:1024,
        height:768
      }});
  const page = await browser.newPage();
  const urls = await readJson('Data/UserMetadata.json');
  results=[];
  for(var url of urls)
  {
    console.log(url);
    await page.goto(url);
    var result = await getAndFormat(url,page);
	results.push(result);
  }
  console.log("saving new results\n");
  for(var result of results)
  {
    var content = JSON.stringify(result);
    fs.appendFile('Data/UserLogging.json',content+'\n',function (err) {
      if (err) {
	  throw err;
	  }
    });
  }
  await browser.close()
}
TrackUsers(); 