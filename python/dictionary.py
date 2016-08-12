import datrie
import string


class StringTrie(datrie.Trie):

    def __init__(self, *args, **kwargs):
        return super(StringTrie, self).__init__(string.ascii_letters, *args, **kwargs)

    def contains(self, string_):
        """Check if a word exists in the dictionary."""
        return unicode(string_) in self

    def add(self, string_):
        """Add a word to the dictionary."""
        self[unicode(string_)] = ''

dictionary = StringTrie()

with open("../words.txt", "r") as words:
    for word in words.read().splitlines():
        if word:
            dictionary.add(word)
