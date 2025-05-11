class TrieNode:
    def __init__(self):
        self.children = {}
        self.top_words = []

    def insert(self, word, frequency):
        # If word is already in top_words, update its frequency
        for i, (freq, wrd) in enumerate(self.top_words):
            if wrd == word:
                self.top_words[i] = (frequency, word)
                self.top_words.sort(key=lambda x: (-x[0], x[1]))
                if len(self.top_words) > 5:
                    self.top_words = self.top_words[:5]
                return

        # If word is not in top_words, add it
        self.top_words.append((frequency, word))
        self.top_words.sort(key=lambda x: (-x[0], x[1]))
        if len(self.top_words) > 5:
            self.top_words = self.top_words[:5]


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, freq):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.insert(word, freq)

    def suggestions(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return [word for _, word in node.top_words]

trie = Trie()
trie.insert('apple', 5)
trie.insert('ape', 3)
trie.insert('apricot', 2)
trie.insert('banana', 6)
trie.insert('bandana', 1)
trie.insert('ban', 4)
trie.insert('app', 7)
trie.insert('application',5)
trie.insert('applaud',1)

print(trie.suggestions('ap'))  # ['app', 'apple', 'application', 'ape', 'apricot'] # applaud will not be shown as less frequency
print(trie.suggestions('ban'))  # ['banana', 'ban', 'bandana']