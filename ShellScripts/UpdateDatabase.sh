cd ../

python3 VideoToDatabase.py >> "./Logs/VideoToDatabaseLogs.out" & nodejs UsersToDatabase.js >> "./Logs/UsersToDatabaseLogs.out"