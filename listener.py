import tweepy
import time
from operator import attrgetter
from synset import Synset

"""
    Stream listener extending tweepy's listener
"""
class CustomStreamListener(tweepy.StreamListener):

    start_time = time.time() # used to measure every 2-second interval
    synonym_groups = [] # holds all the synonym groups
    counter = 0 # counts how many 2-second intervals have passed
    # just some common words that I wanted to ignore to get more intereseting results
    common_words = ['a', 'the', 'i', 'but', '.', 'to', 'rt', 'be', 'is', 'are', 'in', 'have', 'of', 'on', 'at']

    def __init__(self, N):
        super(CustomStreamListener, self).__init__()
        self.N = N # show top N synonym groups

    # this runs on every tweet read in the stream, all the work is done here
    def on_status(self, status):
        self.check_time()
        self.add_to_group(status.text)

    """
        checks time to see if 2 seconds has passed, if 2 seconds has passed
        it removes old data from synonym groups, sorts them and prints them out
    """
    def check_time(self):
        cur_time = time.time()
        if cur_time - self.start_time >= 2:
            self.counter += 1
            map(lambda p: Synset.remove_old(p, self.counter), self.synonym_groups)
            self.synonym_groups = sorted(self.synonym_groups, key=attrgetter('total'))
            for group in self.synonym_groups[self.N*-1:]:
                print group
            print '\n'
            self.start_time = cur_time

    # parses text and adds it to synonym groups
    def add_to_group(self, text):
        for word in text.split(' '):
            word = word.lower()
            if word not in self.common_words:
                added = False
                for group in self.synonym_groups:
                    if word in group:
                        group.add(word, self.counter)
                        added = True
                if not added:
                    synset = Synset(word, self.counter)
                    if len(synset): # if no synset exists for the word don't add it
                        self.synonym_groups.append(synset)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

    def get_synonym_groups(self):
        return self.synonym_groups
