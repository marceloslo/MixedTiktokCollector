cd ../
while true
do
	python3 VideoTracker.py >> "./Logs/VideoTrackerLogs.out" & nodejs TrackUsers.js >> "./Logs/TrackUsersLogs.out" & sleep 1d
done
