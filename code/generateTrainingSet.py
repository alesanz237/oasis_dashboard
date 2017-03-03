
def getTrainingSet():
	classified_sentences = []

	with open("data/sentiment_labelled_sentences/amazon_cells_labelled.txt") as f:
		# classified_sentence = ()
		content = f.readlines()
		for data in content:
			sentence = data.split("\t")[0]
			clase = int(data.split("\t")[1])
			if clase == 0:
				clase = 'negative'
			if clase == 1:
				clase = 'positive'
			classified_sentence= (sentence,clase)
			classified_sentences.append(classified_sentence)

	with open("data/sentiment_labelled_sentences/imdb_labelled.txt") as f:
		# classified_sentence = ()
		content = f.readlines()
		for data in content:
			sentence = data.split("\t")[0]
			clase = int(data.split("\t")[1])
			if clase == 0:
				clase = 'negative'
			if clase == 1:
				clase = 'positive'
			classified_sentence= (sentence,clase)
			classified_sentences.append(classified_sentence)

	with open("data/sentiment_labelled_sentences/yelp_labelled.txt") as f:
		# classified_sentence = ()
		content = f.readlines()
		for data in content:
			sentence = data.split("\t")[0]
			clase = int(data.split("\t")[1])
			if clase == 0:
				clase = 'negative'
			if clase == 1:
				clase = 'positive'
			classified_sentence= (sentence,clase)
			classified_sentences.append(classified_sentence)

	return classified_sentences
