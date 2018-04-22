
import spacy


class SementicAnalyser(object):
	
	def __init__(self):
		super(SementicAnalyser, self).__init__()
		
	def analyse(self, text):
		nlp2 = spacy.load("./sementicAnalysis/model")
		doc2 = nlp2(text)

		intent = sorted(doc2.cats, key=doc2.cats.get, reverse=True)[0]
		confidence = doc2.cats[intent]

		entities = {}
		for ent in doc2.ents:
			entities[ent.label_] = ent.text

		print("Intent: " + intent + " Confidence: " + str(confidence) + " Entities: " + str(entities))

		return intent, confidence, entities