while true; do
	python code/twitterStreaming.py e > data/tweets/tweets.txt 
	python code/sentimentAnalysis.py
	sleep 360
	# today=`date +%Y-%m-%d`
done