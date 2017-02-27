while true; do
	rm data/tweets/positive.txt
	rm data/tweets/negative.txt
	for i in 1 2 3 4 5 6 7 8 9 10
	do
		python static/start/twitterStreaming.py e > data/tweets/$i.txt
		sleep 360 
	done
	python sentimentAnalysis.py
	sleep 3600
	cp data/tweets/positive.txt data/tweets/positive_backup.txt
	cp data/tweets/negative.txt data/tweets/negative_backup.txt
done

