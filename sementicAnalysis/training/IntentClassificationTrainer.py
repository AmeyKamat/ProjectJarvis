#!/usr/bin/env python
# coding: utf8
"""Train a multi-label convolutional neural network text classifier on the
IMDB dataset, using the TextCategorizer component. The dataset will be loaded
automatically via Thinc's built-in dataset loader. The model is added to
spacy.pipeline, and predictions are available via `doc.cats`. For more details,
see the documentation:
* Training: https://spacy.io/usage/training
Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function
import random
from pathlib import Path
import sys, os

import spacy
from spacy.util import minibatch, compounding, decaying


def train(model=None, output_dir=None, n_iter=20, n_texts=2000, categories=[], train_texts=[], train_cats=[], dev_texts=[], dev_cats=[]):
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    # add the text classifier to the pipeline if it doesn't exist
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'textcat' not in nlp.pipe_names:
        textcat = nlp.create_pipe('textcat')
        nlp.add_pipe(textcat, last=True)
    # otherwise, get it, so we can add labels to it
    else:
        textcat = nlp.get_pipe('textcat')

    # add label to text classifier
    #categories = ['greet', 'time', 'direction', 'self-location', 'location', 'search-general', 
    #'search-restaurants', 'affirmation', 'negation', 'launch', 'news', 'shut-down',
    #'compliment', 'search-wikipedia']

    for category in categories:
        textcat.add_label(category)

    # load the IMDB dataset
    print("Loading categorisation data...")
    #(train_texts, train_cats), (dev_texts, dev_cats) = load_data(categories, limit=n_texts)


    print("Using {} examples ({} training, {} evaluation)"
          .format(n_texts, len(train_texts), len(dev_texts)))
    train_data = list(zip(train_texts,
                          [{'cats': cats} for cats in train_cats]))

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'textcat']
    with nlp.disable_pipes(*other_pipes):  # only train textcat
        optimizer = nlp.begin_training()
        print("Training the model...")
        print('{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('Iter #', 'LOSS', 'P', 'R', 'F'))
        for i in range(n_iter):
            losses = {}
            # batch up the examples using spaCy's minibatch
            #batches = get_batches(train_data, 'textcat')
            batches = minibatch(train_data, size=compounding(4., 32., 1.001))
            dropout = decaying(0.6, 0.2, 1e-4)
            for batch in batches:
                texts, annotations = zip(*batch)

                nlp.update(texts, annotations, sgd=optimizer, drop=0.2,
                           losses=losses)
            with textcat.model.use_params(optimizer.averages):
                # evaluate on the dev data split off in load_data()
                scores = evaluate(nlp.tokenizer, textcat, dev_texts, dev_cats)
            print('{0}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t{4:.3f}'  # print a simple table
                  .format(i, losses['textcat'], scores['textcat_p'],
                          scores['textcat_r'], scores['textcat_f']))

    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

def get_batches(train_data, model_type):
    max_batch_sizes = {'tagger': 32, 'parser': 16, 'ner': 16, 'textcat': 64}
    max_batch_size = max_batch_sizes[model_type]
    if len(train_data) < 1000:
        max_batch_size /= 2
    if len(train_data) < 500:
        max_batch_size /= 2
    batch_size = compounding(1, max_batch_size, 1.001)
    batches = minibatch(train_data, size=batch_size)
    return batches


def load_data(categories, limit=0, split=0.8):
    """Load data from the IMDB dataset."""
    # Partition off part of the train data for evaluation
    test_file = open('test_data.txt', "r")
    texts = []
    labels = []
    lines = []
    cats=[]
    for line in test_file:
        lines.append(line)
    random.shuffle(lines)
    print(limit)
    lines = lines[-limit:]
    
    for line in lines:
        test_sentence, intent = line.split('|');
        texts.append(test_sentence.strip())
        labels.append(intent.strip())

    category_counter  = {}
    for category in categories:
        category_counter[category] = 0

    for label in labels:
        category_counter[label] = category_counter[label] + 1
    
    print("Total training data set: ")
    print(category_counter)

    for label in labels:
        catsForRecord = {}
        for category in categories:
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
            print(str(catsForRecord), " ", str(label))
            
    test_file.close()
    split = int(len(texts) * split)
    return (texts[:split], cats[:split]), (texts[split:], cats[split:])


def evaluate(tokenizer, textcat, texts, cats):
    docs = (tokenizer(text) for text in texts)
    tp = 1e-8  # True positives
    fp = 1e-8  # False positives
    fn = 1e-8  # False negatives
    tn = 1e-8  # True negatives
    for i, doc in enumerate(textcat.pipe(docs)):
        gold = cats[i]
        for label, score in doc.cats.items():
            if label not in gold:
                continue
            if score >= 0.5 and gold[label] >= 0.5:
                tp += 1.
            elif score >= 0.5 and gold[label] < 0.5:
                fp += 1.
            elif score < 0.5 and gold[label] < 0.5:
                tn += 1
            elif score < 0.5 and gold[label] >= 0.5:
                fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f_score = 2 * (precision * recall) / (precision + recall)
    return {'textcat_p': precision, 'textcat_r': recall, 'textcat_f': f_score}