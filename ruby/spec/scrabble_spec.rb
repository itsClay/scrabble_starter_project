require './scrabble.rb'


# Helper to create an array of tile objects from a splat of
# three-element arrays of the shape `[letter, row, col]`
def make_tiles(*tile_specs)
  tile_specs.map do |spec|
    { letter: spec[0], row: spec[1], col: spec[2] }
  end
end

RSpec.describe Scrabble do
  let(:game) { Scrabble.new }

  it "scores a word" do
    tiles = make_tiles(
      ["b", 7, 7],
      ["u", 7, 8],
      ["t", 7, 9],
      ["t", 7, 10],
      ["o", 7, 11],
      ["n", 7, 12]
    )

    move = game.play_tiles(tiles)
    expect(move).to eq(valid: true, score: 8)
    expect(game.score).to eq(8)
  end

  it "does not score invalid words" do
    tiles = make_tiles(
      ["a", 7, 7],
      ["s", 7, 8],
      ["d", 7, 9],
      ["f", 7, 10]
    )

    move = game.play_tiles(tiles)
    expect(move).to eq(valid: false, score: 0)
    expect(game.score).to eq(0)
  end

  it "requires all tiles be placed on the board" do
    tiles = make_tiles(
      ["q", 7, 7],
      ["u", 7, 8],
      ["i", 7, 9],
      ["z", 7, 10],
      ["z", 7, 11],
      ["i", 7, 12],
      ["c", 7, 13],
      ["a", 7, 14],
      ["l", 7, 15]
    )

    move = game.play_tiles(tiles)
    expect(move).to eq(valid: false, score: 0)
    expect(game.score).to eq(0)
  end

  it "requires all tiles to be on a unique space" do
    tiles = make_tiles(
      ["b", 7, 7],
      ["u", 7, 8],
      ["t", 7, 9],
      ["t", 7, 10],
      ["o", 7, 10],
      ["n", 7, 11]
    )

    move = game.play_tiles(tiles)
    expect(move).to eq(valid: false, score: 0)
    expect(game.score).to eq(0)
  end

  it "requires all tiles to be placed in a single row or column" do
    tiles = make_tiles(
      ["b", 7, 7],
      ["u", 7, 8],
      ["t", 7, 9],
      ["t", 7, 10],
      ["o", 7, 11],
      ["n", 8, 11]
    )

    move = game.play_tiles(tiles)
    expect(move).to eq(valid: false, score: 0)
    expect(game.score).to eq(0)
  end

  it "requires the first move to have a tile on 7, 7" do
    tiles = make_tiles(
      ["b", 8, 7],
      ["u", 8, 8],
      ["t", 8, 9],
      ["t", 8, 10],
      ["o", 8, 11],
      ["n", 8, 12]
    )

    move = game.play_tiles(tiles)
    expect(move).to eq(valid: false, score: 0)
    expect(game.score).to eq(0)
  end

  it "does not allow replacing or overlapping tiles" do
    tiles1 = make_tiles(
      ["b", 7, 7],
      ["u", 7, 8],
      ["t", 7, 9],
      ["t", 7, 10],
      ["o", 7, 11],
      ["n", 7, 12]
    )
    game.play_tiles(tiles1)
    expect(game.score).to eq(8)

    tiles2 = make_tiles(
      ["h", 6, 11],
      ["o", 7, 11],
      ["m", 8, 11],
      ["e", 9, 11]
    )
    move = game.play_tiles(tiles2)
    expect(move).to eq(valid: false, score: 0)
    expect(game.score).to eq(8)
  end

  it "requires subsequent words to share at least one tile, which is scored" do
    tiles1 = make_tiles(
      ["b", 7, 7],
      ["u", 7, 8],
      ["t", 7, 9],
      ["t", 7, 10],
      ["o", 7, 11],
      ["n", 7, 12]
    )
    game.play_tiles(tiles1)
    expect(game.score).to eq(8)

    tiles2 = make_tiles(
      ["h", 9, 8],
      ["o", 9, 9],
      ["m", 9, 10],
      ["e", 9, 11]
    )
    bad_move = game.play_tiles(tiles2)
    expect(bad_move).to eq(valid: false, score: 0)
    expect(game.score).to eq(8)

    tiles3 = make_tiles(
      ["h", 6, 11],
      ["m", 8, 11],
      ["e", 9, 11]
    )
    good_move = game.play_tiles(tiles3)
    expect(good_move).to eq(valid: true, score: 9)
    expect(game.score).to eq(17)
  end

  it "allows forming a new word by adding tiles to the start or end of a word" do
    tiles1 = make_tiles(
      ["n", 7, 7],
      ["o", 7, 8]
    )

    move = game.play_tiles(tiles1)
    expect(move).to eq(valid: true, score: 2)
    expect(game.score).to eq(2)

    tiles2 = make_tiles(
      ["s", 7, 6],
      ["w", 7, 9]
    )

    move = game.play_tiles(tiles2)
    expect(move).to eq(valid: true, score: 7)
    expect(game.score).to eq(9)
  end

  it "only allows plays in which all newly formed words are valid" do
    tiles1 = make_tiles(
      ["k", 7, 6],
      ["n", 7, 7],
      ["o", 7, 8],
      ["w", 7, 9]
    )

    move = game.play_tiles(tiles1)
    expect(move).to eq(valid: true, score: 15)
    expect(game.score).to eq(15)

    tiles2 = make_tiles(
      ["s", 6, 7],
      ["n", 6, 8],
      ["o", 6, 9],
      ["t", 6, 10]
    )

    move = game.play_tiles(tiles2)
    expect(move).to eq(valid: false, score: 0)
    expect(game.score).to eq(15)
  end

  it "correctly scores multiple newly formed words" do
    tiles1 = make_tiles(
      ["k", 7, 6],
      ["n", 7, 7],
      ["o", 7, 8],
      ["w", 7, 9]
    )

    move = game.play_tiles(tiles1)
    expect(move).to eq(valid: true, score: 15)
    expect(game.score).to eq(15)

    tiles2 = make_tiles(
      ["n", 6, 8],
      ["o", 6, 9],
      ["t", 6, 10]
    )

    move = game.play_tiles(tiles2)
    expect(move).to eq(valid: true, score: 10)
    expect(game.score).to eq(25)
  end
end
