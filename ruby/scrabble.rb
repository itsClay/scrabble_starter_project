require "./dictionary.rb"

LETTERS = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z' ]
SCORES  = [ 1,   3,   3,   2,   1,   4,   2,   4,   1,   8,   5,   1,
            3,   1,   1,   3,   10,  1,   1,   1,   1,   4,   4,   8,   4,   10 ]
SCORES_BY_LETTER = Hash[LETTERS.zip(SCORES)] # { 'a': 1, 'b': 3, ... }

def is_valid_word(word)
  DICTIONARY.has_key? word
end

class Scrabble
  attr_accessor :score

  def initialize
    @score = 0
  end

  # tiles - Array<{ letter: String, row: Int, col: Int }>
  #
  #  an array of hashes; each hash contains a `:letter` (the letter
  #  of the tile to play), a `:row` (the row to play the tile in) and
  #  a `:col` (the column to play the tile in).
  #
  # score - { valid: Boolean, score: Int }
  #
  #  `:valid` is whether or not the set of tiles represent a valid game
  #  move. If so, `:score` is the value of the play to be added to the
  #  score, and if not, `:score` is 0.
  #
  def play_tiles(tiles)
    # TODO: implement me!
  end
end
