var fs = require("fs");

var Trie = require("trie-hard");

var dictionary = new Trie();

var words = fs.readFileSync("../words.txt", "utf8");
words.split("\n").map(function(word) {
  return word.trim();
}).forEach(function(word) {
  if (word) {
    dictionary.add(word);
  }
});

module.exports = dictionary;
