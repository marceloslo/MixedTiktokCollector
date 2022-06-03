# TiktokJs
 TikTok scrapper with javascript

 Javascript: necessário baixar puppeteer, puppeteer-extra,puppeteer-extra-plugin-stealth, csv
 npm install ...

# Scripts

- TrackUsers: collects daily user statistics and saves on userlogging
- UsersToDatabase: given manually collected videos on TikTokUsers.csv add they and their statistics to UserMetadata
- GetProfileVideos: get videos from profiles and saves their url on VideosTemp.
- VideoToDatabase: get videos from VideosTemp and saves their metadata on VideoMetadata
- VideoTracker: get daily video statistics and saves them on videologging
- CommentTracker: get all comments from videos in videometadata and saves on comments.json

# TikTokCollector

Python: necessário baixar pandas, selenium
 
 O salvamento de arquivos deve ser feito na forma json lines, ou seja, linhas de dicionários, busque retornar dicionários para todos métodos que isso fizer sentido.

Padronizar atributos: se um atributo ou estatística já existe em algum outro método, use o mesmo nome para facilitar comparações e merges.

O init da classe requer um driver como parametro, isso para evitar ter que usar vários drivers identicos nas diferentes classes.

## VideoStatisticsCollector

Coletor de estatísticas de um vídeo.

Métodos:
- setUrl(url : string): define a Url da qual se deseja coletar. Formato aceito de url: https://www.tiktok.com/@user/video/videoid

- getStatistics(): coleta estatísticas de um vídeo, retorna um dicionário da forma abaixo

{

Url : String

User : String

UserId : String

Description : String

LikeCount : String (número + multiplicador, ex: 25k)

CommentCount : String (número + multiplicador, ex: 25k)

SharesCount : String (número + multiplicador, ex: 25k)

PublicationDate : Datetime (YY-mm-dd)

CollectionDate : Datetime (YY-mm-dd)

Status : boolean (0 = offline, 1 = online)

}

- getStatisticsFromUrl(url : string) : mistura dos dois métodos acima

- getContent() : obtém a url do vídeo em si (pode ter utilidade para eventualmente baixar e analisar os vídeos).

## ProfileStatisticsCollector

Coletor de estatísticas de um usuário.

Métodos:
- setUrl(url : string): define a Url da qual se deseja coletar. Formato aceito de url: https://www.tiktok.com/@user

- getStatistics(): coleta estatísticas de um usuário, retorna um dicionário da forma abaixo

{

Url : String

User : String

UserId : String

ProfileBio : String

Followers : String (número + multiplicador, ex: 25k)

Following : String (número + multiplicador, ex: 25k)

LikeCount : String (número + multiplicador, ex: 25k)

CollectionDate : Datetime (YY-mm-dd)

Status : boolean (0 = offline, 1 = online)

}

- getStatisticsFromUrl(url : string) : mistura dos dois métodos acima

## CommentCollector

Métodos:

- getStatistics(): coleta todos comentários de um video, retorna uma lista de dicionários no formato:

{

Url : String

User : String

Content : String

LikeCount : String (número + multiplicador, ex: 25k)

RepliesCount : String (número + multiplicador, ex: 25k)

CollectionDate : Datetime (YY-mm-dd)

PublicationDate : Datetime (YY-mm-dd)

}

