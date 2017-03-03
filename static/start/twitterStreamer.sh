while true; do
	rm data/tweets/positive.txt
	rm data/tweets/negative.txt
<<<<<<< HEAD
	python code/twitterStreaming.py e > data/tweets/tweets.txt 
	python code/sentimentAnalysis.py
=======
	python static/start/twitterStreaming.py e > data/tweets/tweets.txt
	sleep 360 
	python sentimentAnalysis.py
>>>>>>> bb2e335f5ca2c332fe21569e6e5365b327411ff2
	sleep 360
	cp data/tweets/positive.txt data/tweets/positive_backup.txt
	cp data/tweets/negative.txt data/tweets/negative_backup.txt
done