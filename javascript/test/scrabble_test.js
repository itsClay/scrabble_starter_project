var expect = require("chai").expect;

var ScrabbleGame = require("../index.js");

// Helper to create an array of tile objects from an arglist of
// three-element arrays of the shape `[letter, row, col]`
function makeTiles() {
  var array = Array.prototype.slice.call(arguments);
  return array.map(function(tile) {
    return {
      letter: tile[0],
      row: tile[1],
      col: tile[2]
    };
  });
}

describe("Scrabble", function() {
  var game, move;

  beforeEach(function() {
    game = new ScrabbleGame();
  });

  it("scores a word", function() {
    var tiles = makeTiles(
      ["b", 7, 7],
      ["u", 7, 8],
      ["t", 7, 9],
      ["t", 7, 10],
      ["o", 7, 11],
      ["n", 7, 12]
    );

    move = game.playTiles(tiles);
    expect(move).to.eql({valid: true, score: 8});
    expect(game.score).to.eql(8);
  });

  it("doesn't score invalid words", function() {
    var tiles = makeTiles(
      ["a", 7, 7],
      ["s", 7, 8],
      ["d", 7, 9],
      ["f", 7, 10]
    );

    move = game.playTiles(tiles);
    expect(move).to.eql({valid: false, score: 0});
    expect(game.score).to.eql(0);
  });

  it("requires all tiles be placed on the board", function() {
    var tiles = makeTiles(
      ["q", 7, 7],
      ["u", 7, 8],
      ["i", 7, 9],
      ["z", 7, 10],
      ["z", 7, 11],
      ["i", 7, 12],
      ["c", 7, 13],
      ["a", 7, 14],
      ["l", 7, 15]
    );

    move = game.playTiles(tiles);
    expect(move).to.eql({valid: false, score: 0});
    expect(game.score).to.eql(0);
  });

  it("requires all tiles to be on a unique space", function() {
    var tiles = makeTiles(
      ["b", 7, 7],
      ["u", 7, 8],
      ["t", 7, 9],
      ["t", 7, 10],
      ["o", 7, 10],
      ["n", 7, 11]
    );

    var move = game.playTiles(tiles);
    expect(move).to.eql({valid: false, score: 0});
    expect(game.score).to.eql(0);
  });

  it("requires all tiles to be placed in a single row or column", function() {
    var tiles = makeTiles(
      ["b", 7, 7],
      ["u", 7, 8],
      ["t", 7, 9],
      ["t", 7, 10],
      ["o", 7, 11],
      ["n", 8, 11]
    );

    move = game.playTiles(tiles);
    expect(move).to.eql({valid: false, score: 0});
    expect(game.score).to.eql(0);
  });

  it("requires the first move to have a tile on 7,7", function() {
    var tiles = makeTiles(
      ["b", 8, 7],
      ["u", 8, 8],
      ["t", 8, 9],
      ["t", 8, 10],
      ["o", 8, 11],
      ["n", 8, 12]
    );

    move = game.playTiles(tiles);
    expect(move).to.eql({valid: false, score: 0});
    expect(game.score).to.eql(0);
  });

  it("doesn't allow replacing or overlapping tiles", function() {
    var tiles1 = makeTiles(
      ["b", 7, 7],
      ["u", 7, 8],
      ["t", 7, 9],
      ["t", 7, 10],
      ["o", 7, 11],
      ["n", 7, 12]
    );
    game.playTiles(tiles1);
    expect(game.score).to.eql(8);

    var tiles2 = makeTiles(
      ["h", 6, 11],
      ["o", 7, 11],
      ["m", 8, 11],
      ["e", 9, 11]
    );
    var move = game.playTiles(tiles2);
    expect(move).to.eql({valid: false, score: 0});
    expect(game.score).to.eql(8);
  });

  it("requires subsequent words to share at least one tile, which is scored", function() {
    var tiles1 = makeTiles(
      ["b", 7, 7],
      ["u", 7, 8],
      ["t", 7, 9],
      ["t", 7, 10],
      ["o", 7, 11],
      ["n", 7, 12]
    );
    game.playTiles(tiles1);
    expect(game.score).to.eql(8);

    var tiles2 = makeTiles(
      ["h", 9, 8],
      ["o", 9, 9],
      ["m", 9, 10],
      ["e", 9, 11]
    );
    var badMove = game.playTiles(tiles2);
    expect(badMove).to.eql({valid: false, score: 0});
    expect(game.score).to.eql(8);

    var tiles3 = makeTiles(
      ["h", 6, 11],
      ["m", 8, 11],
      ["e", 9, 11]
    );
    var goodMove = game.playTiles(tiles3);
    expect(goodMove).to.eql({valid: true, score: 9});
    expect(game.score).to.eql(17);
  });

  it("allows forming a new word by adding tiles to the start/end of a word", function() {
    var tiles1 = makeTiles(
      ["n", 7, 7],
      ["o", 7, 8]
    );

    move = game.playTiles(tiles1);
    expect(move).to.eql({valid: true, score: 2});
    expect(game.score).to.eql(2);

    var tiles2 = makeTiles(
      ["s", 7, 6],
      ["w", 7, 9]
    );

    move = game.playTiles(tiles2);
    expect(move).to.eql({valid: true, score: 7});
    expect(game.score).to.eql(9);
  });

  it("only allows plays in which all newly formed words are valid", function() {
    var tiles1 = makeTiles(
      ["k", 7, 6],
      ["n", 7, 7],
      ["o", 7, 8],
      ["w", 7, 9]
    );

    move = game.playTiles(tiles1);
    expect(move).to.eql({valid: true, score: 11});
    expect(game.score).to.eql(11);

    var tiles2 = makeTiles(
      ["s", 6, 7],
      ["n", 6, 8],
      ["o", 6, 9],
      ["t", 6, 10]
    );

    move = game.playTiles(tiles2);
    expect(move).to.eql({valid: false, score: 0});
    expect(game.score).to.eql(15);
  });

  it("correctly scores multiple newly formed words", function() {
    var tiles1 = makeTiles(
      ["k", 7, 6],
      ["n", 7, 7],
      ["o", 7, 8],
      ["w", 7, 9]
    );

    move = game.playTiles(tiles1);
    expect(move).to.eql({valid: true, score: 11});
    expect(game.score).to.eql(11);

    var tiles2 = makeTiles(
      ["n", 6, 8],
      ["o", 6, 9],
      ["t", 6, 10]
    );

    move = game.playTiles(tiles2);
    expect(move).to.eql({valid: true, score: 10});
    expect(game.score).to.eql(21);
  });
});
