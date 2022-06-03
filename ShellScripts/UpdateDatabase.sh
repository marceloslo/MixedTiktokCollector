cd ../
while true
do
	nodejs GetProfileVideos.js >> "Logs/ProfileVideosLog.out"
	python3 VideoToDatabase.py >>"Logs/VideoToDatabase.out"
	sleep 7d
done
