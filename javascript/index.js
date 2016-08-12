var _ = require("lodash");

// https://github.com/BinaryMuse/trie-hard
var dictionary = require("./dictionary");

function isWordValid(word) {
  return dictionary.isMatch(word);
}

var letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'];
var scores  = [ 1,  3,  3,  2,  1,  4,  2,  4,  1,  8,  5,  1,  3,  1,  1,  3,  10, 1,  1,  1,  1,  4,  4,  8,  4,  10]
var scoresByLetter = _.zipObject(letters, scores); // { 'a': 1, 'b': 3, ... }

function ScrabbleGame() {
  this.score = 0;
}

/**
 * @param tiles - Array<{ letter: String, row: Int, col: Int }>
 *
 *  an array of objects; each object contains a `letter` (the letter
 *  of the tile to play), a `row` (the row to play the tile in) and
 *  a `col` (the column to play the tile in).
 *
 * @return score - { valid: Boolean, score: Int }
 *
 *  `valid` is whether or not the set of tiles represent a valid game
 *  move. If so, `score` is the value of the play to be added to the
 *  score, and if not, `score` is 0.
 */
ScrabbleGame.prototype.playTiles = function(tiles) {
  // TODO: implement me!
};


module.exports = ScrabbleGame;
