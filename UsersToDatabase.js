var fs = require('fs'); 
var { parse } = require("csv-parse");
const readline = require('readline');
const puppeteer = require('puppeteer')

//reads csv file and returns its users
function readData(file)
{
  let urls=[]
  return new Promise((resolve,reject) =>{
    fs.createReadStream(file)
      .on('error',error => {
        reject(error);
      })
      .pipe(parse({delimiter: ',',from_line: 2}))
      .on('data', (row) => {
        urls.push(row[0]);
      })
      .on('end', () => {
        resolve(urls);
      });
  });
}

//gets csv data from TikTokUsers.csv
async function getData(){
  try { 
    const data = await readData('Data/TikTokUsers.csv');
    return data;
  } catch (error) {
      console.error("testGetData: An error occurred: ", error.message);
  }
}

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
  await page.waitForXPath(xp,{timeout: 1000});
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
//gets date in format YYYY-MM-DD
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

//gets metadata in json format
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

//Add all profiles' metadata in the csv file to the json file
async function UserToDatabase(){
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  const urls = await getData();
  const dataframe = await readJson('Data/UserMetadata.json');
  results=[];
  for(var url of urls)
  {
    if(!dataframe.includes(url)){
      console.log(url);
      await page.goto(url);
      var result = await getAndFormat(url,page);
      results.push(result);
    }
  }
  for(var result of results)
  {
    var content = JSON.stringify(result);
    fs.appendFile('Data/UserMetadata.json',content+'\n',function (err) {
      if (err) throw err;
    });
  }
  await browser.close()
}

UserToDatabase() 