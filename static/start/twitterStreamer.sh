while true; do
	python code/twitterStreaming.py e > data/tweets/tweets.txt 
	python code/sentimentAnalysis.py
	sleep 360
	cp data/tweets/positive.txt data/tweets/positive_backup.txt
	cp data/tweets/negative.txt data/tweets/negative_backup.txt
done