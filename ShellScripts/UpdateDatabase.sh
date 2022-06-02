cd ../
while true
do
	nodejs GetProfileVideos.js >> "./Logs/ProfileVideosLog.out"
	nodejs UsersToDatabase.js >>"./Logs/UsersToDatabase.out"
	sleep 7d
done
