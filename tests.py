from synset import Synset
from listener import CustomStreamListener

# and returns an empty synset from WordNet
def test_empty_synset():
    empty = Synset('and', 0)
    assert len(empty) == 0
    return True

# test stale data gets deleted
def test_delete_old():
    syn = Synset('dog', 0)
    syn.add('dog', 0)
    syn.add('dog', 0)
    assert syn.get_total() == 3
    assert syn.get_val('dog')[0] == 3
    syn.add('dog', 1)
    assert syn.get_total() == 4
    assert syn.get_val('dog')[0] == 4
    syn.remove_old(30)
    assert syn.get_total() == 1
    assert syn.get_val('dog')[0] == 1
    syn.remove_old(31)
    assert syn.get_total() == 0
    assert syn.get_val('dog')[0] == 0
    return True

# test synonym count goes toward total and works properly
def test_synonym_add():
    try:
        syn = Synset('happy', 0)
        syn.add('happy', 0)
        syn.add('glad', 0)
        syn.add('felicitous', 0)
        assert syn.get_total() == 4
        assert syn.get_val('happy')[0] == 2
        assert syn.get_val('glad')[0] == 1
        assert syn.get_val('felicitous')[0] == 1
        assert 'happy' in syn
        assert 'glad' in syn
        assert 'felicitous' in syn
        return True
    except:
        return False


# test listener's ability to add text correctly to synonym groups
def test_listener_add_to_group():
    try:
        listener = CustomStreamListener(3)
        listener.add_to_group('happy dog felicitous')
        syn_groups =listener.get_synonym_groups()
        syn_happy = Synset('happy', 0)
        syn_dog = Synset('dog', 0)
        syn_happy.add('felicitous', 0)
        """
            order of groups will be based on order of text so 0 for happy and 1 for dog
            counter will be 0 in listener because just started
        """
        assert syn_groups[0] == syn_happy
        assert syn_groups[1] == syn_dog
        return True
    except:
        return False

print "Testing empty set: Passed = %s" % test_empty_synset()
print "Testing deleting old data: Passed = %s" % test_delete_old()
print "Testing adding synonyms: Passed = %s" % test_synonym_add()
print "Testing adding text to listener: Passed = %s" %test_listener_add_to_group()
