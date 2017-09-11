from nltk.corpus import wordnet as wn

"""
    stores synonym groups and on which 2 second interval each word was added
    example: {'foo': [10, {0:3, 1:2, 2:4, 3:1}], 'bar': [3, {1:1, 3:2}]}
    here 'foo' is seen 3 times in the seconds 0-2, 2 times in 2-4, 4 in 4-6, and 1 in 6-8
    'bar' is see once in 2-4 and twice in 6-8
    the first value is the total and when old entries get deleted because its been over
    a minute the total also gets updated accordingly
"""
class Synset():


    def __init__(self, word, counter):
        self.synonyms = set(map(self.get_word, wn.synsets(word)))
        if self.synonyms: # if synset is empty then don't do any work, it'll get filtered out
            self.word_val = {} # dictionary that will hold the word/value mapping
            self.total = 1 # total number in this synset
            self.synonyms.add(word)
            for synonym in self.synonyms:
                self.word_val[synonym] = [0, {counter:0}]
            self.word_val[word] = [1, {counter:1}]

    def __len__(self):
        return len(self.synonyms)

    # returns the word from a given synset
    def get_word(self, synset):
        return synset.name().split('.')[0]

    def overlap(self, words):
        for word in words:
            if word in self.words:
                return True
        return False

    # increments the total of the word and also the counter that it is on
    def add(self, word, counter):
        self.word_val[word][0] += 1
        if counter in self.word_val[word][1]:
            self.word_val[word][1][counter] += 1
        else:
            self.word_val[word][1][counter] = 1
        self.total += 1

    def get_val(self, word):
        return self.word_val[word]

    def get_total(self):
        return self.total

    # removes all values that are over 60 seconds old by looking at counter passed in
    def remove_old(self, cur_counter):
        for word in self.word_val.values():
            val = word[1].get(cur_counter-30)
            # if value exists that is 30 increments old, delete it and decrement totals accordingly
            if val:
                word[0] -= val
                self.total -= val
                del word[1][cur_counter-30]

    def __contains__(self, word):
        return word in self.word_val

    def __eq__(self, synset):
        for word in self.word_val:
            if not synset.get_val(word) == self.word_val[word]:
                return False
        return True

    def __repr__(self):
        to_print = 'Total: %s ' % self.total
        for k, v in self.word_val.iteritems():
            to_print += '%s: %s ' % (k, v[0])
        return to_print[:-1]
