import collections
import itertools
import nltk.classify.util, nltk.metrics
from nltk.classify import MaxentClassifier
from nltk.metrics import precision, recall, f_measure
from nltk.corpus import movie_reviews



def word_feats(words):
	return dict([(word, True) for word in words])

for i in range(9):
	i=i+1
	negids = movie_reviews.fileids('neg')
	posids = movie_reviews.fileids('pos')

	negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
	posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

	negcutoff = int(len(negfeats)*i/10.0)
	poscutoff = int(len(posfeats)*i/10.0)
	# print(negcutoff)
	trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
	testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

	print('train on %d instances, test on %d instances - Maximum Entropy' % (len(trainfeats), len(testfeats)))

	classifier = MaxentClassifier.train(trainfeats, 'GIS', trace=0, encoding=None, labels=None, gaussian_prior_sigma=0, max_iter = 1)

	refsets = collections.defaultdict(set)
	testsets = collections.defaultdict(set)
	
	for i, (feats, label) in enumerate(testfeats):
		refsets[label].add(i)
		# print(feats)
		# print(label)
		observed = classifier.classify(feats)
		
		testsets[observed].add(i)
		print(testsets)
		print(len(testsets))
	
	accuracy = nltk.classify.util.accuracy(classifier, testfeats)
	print(classifier.show_most_informative_features())


	pos_precision = precision(refsets['pos'], testsets['pos'])
	pos_recall = recall(refsets['pos'], testsets['pos'])
	pos_fmeasure = f_measure(refsets['pos'], testsets['pos'])
	neg_precision = precision(refsets['neg'], testsets['neg'])
	neg_recall = recall(refsets['neg'], testsets['neg'])
	neg_fmeasure =  f_measure(refsets['neg'], testsets['neg'])

	print ('Maximum Entropy Markov Model')
	print ('accuracy:', accuracy)
	print ('precision', (pos_precision + neg_precision) / 2)
	print ('recall', (pos_recall + neg_recall) / 2)
	print ('f-measure', (pos_fmeasure + neg_fmeasure) / 2)

	outfile='./outfile.csv'
	out=open(outfile,'a+')
	out.write(str(len(trainfeats)))
	out.write(',')
	out.write(str(accuracy))
	out.write(',')
	out.write(str((pos_fmeasure + neg_fmeasure) / 2))
	out.write('\n')
	out.close()

