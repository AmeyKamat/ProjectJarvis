#!/usr/bin/env python

from IntentClassificationTrainer import train as trainForIntent;
from EntityExtractionTrainer import train as trainForEntity;
import random
from pathlib import Path

import spacy

CATEGORIES = ['greet', 'time', 'direction', 'self-location', 'location', 'search-general', 
    'search-restaurants', 'affirmation', 'negation', 'launch', 'news', 'shut-down',
    'compliment', 'search-wikipedia', 'question', 'response', 'reminder', "bookcab"]

ENTITY_TYPES= ["LOCATION", "TOLOCATION", "FROMLOCATION", "QUERY", "DATE", "NEWSCATEGORY",
    "CUISINE", "SOFTWARE", "REMINDERTEXT", "TIME"]

INTENT_SPLIT = 0.8
INTENT_LIMIT = 2000


def train(train_data_location, model_location, model_name):
    output_dir = Path(model_location)
    if model_location is not None and output_dir.exists():
         nlp = spacy.load(model_location)  # load existing spaCy model
         print("Loaded model '%s'" % model_location)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    if model_location is not None:
        output_dir = Path(model_location)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.meta['name'] = model_name
        nlp.to_disk(model_location)
        print("Saved model to " + model_location)


    for i in range(10):
        print("Main Iteration: " + str(i))
        print("Starting Data Load")
        train_data = load_data(train_data_location)
        print("Data load complete")
        print("Training for Intent")
        trainForIntent(model_location, model_location, 20, INTENT_LIMIT, CATEGORIES, train_data["intent_data"][0], train_data["intent_data"][1], train_data["intent_data"][2], train_data["intent_data"][3])
        print("Training for Intent is complete")
        print("Training for Entity")
        trainForEntity(model_location, model_location, 20, ENTITY_TYPES, train_data["entity_data"])
        print("Training for Entity complete")

def load_data(train_data_location):
    train_data = {};
    lines = []

    test_file = open(train_data_location, "r")
    for line in test_file:
        lines.append(unicode(line, "utf-8"))
    test_file.close()
    random.shuffle(lines)
    lines = lines[-INTENT_LIMIT:]
    train_data["intent_data"] = get_intent_training_data(lines);
    train_data["entity_data"] = get_entity_training_data(lines);
            
    return train_data
    

def get_intent_training_data(lines):
    texts = []
    labels = []
    cats = []
    category_counter  = {}

    for line in lines:
        test_sentence = line.split('|')[0];
        intent = line.split('|')[1];
        texts.append(test_sentence.strip())
        labels.append(intent.strip())

    for category in CATEGORIES:
        category_counter[category] = 0

    for label in labels:
        category_counter[label] = category_counter[label] + 1
    
    print("Total training data set: ")
    print(category_counter)

    for label in labels:
        catsForRecord = {}
        for category in CATEGORIES:
            if category == label:
                catsForRecord[category] = 1.0
            else:
                catsForRecord[category] = 0.0
        cats.append(catsForRecord)

        flag = 0;
        for key, value in catsForRecord.items():
            if(value == 1):
                flag = 1
        if(flag==0):
            print("Failed Record: ")
            print(str(catsForRecord), " ", str(label))
    
    split = int(len(texts) * INTENT_SPLIT)
    return [texts[:split], cats[:split], texts[split:], cats[split:]]

def get_entity_training_data(lines):
    data = []
    for line in lines:
        record = line.split('|')
        test_sentence = record[0];
        entity_list = []
        if(len(record)>2):
            for i in range(2, len(record)):
                entity = record[i]
                entity_record = entity.split(',')
                entity_type = entity_record[0].strip()
                entity_start = int(entity_record[1].strip())
                entity_end = int(entity_record[2].strip())
                entity_list.append((entity_start, entity_end, entity_type))
        data.append((test_sentence, {"entities": entity_list}))

    return data

def test():
    command = input("Enter Command: ")
    print("Loading from", "../model")
    nlp2 = spacy.load("../model")
    doc2 = nlp2(command)
    print(sorted(doc2.cats, key=doc2.cats.get, reverse=True))
    for ent in doc2.ents:
        print(ent.label_, ent.text)

#test()
train("./train_data.txt", "../model", "en.assistant.model")