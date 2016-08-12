import unittest2

from scrabble import ScrabbleGame


def make_tiles(*tile_specs):
    """
    Helper to create an array of tile objects from an arglist of
    three-element arrays of the shape `[letter, row, col]`
    """
    return [
        { 'letter': spec[0], 'row': spec[1], 'col': spec[2] }
        for spec in tile_specs
    ]

class TestScrabble(unittest2.TestCase):

    def setUp(self):
        self.game = ScrabbleGame()

    def test_scores_a_word(self):
        tiles = make_tiles(
            ["b", 7, 7],
            ["u", 7, 8],
            ["t", 7, 9],
            ["t", 7, 10],
            ["o", 7, 11],
            ["n", 7, 12]
        )

        move = self.game.play_tiles(tiles)
        self.assertEqual(move, {'valid': True, 'score': 8})
        self.assertEqual(self.game.score, 8)


    def test_does_not_score_invalid_words(self):
        tiles = make_tiles(
            ["a", 7, 7],
            ["s", 7, 8],
            ["d", 7, 9],
            ["f", 7, 10]
        )

        move = self.game.play_tiles(tiles)
        self.assertEqual(move, {'valid': False, 'score': 0})
        self.assertEqual(self.game.score, 0)


    def test_requires_all_tiles_be_placed_on_the_board(self):
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

        move = self.game.play_tiles(tiles)
        self.assertEqual(move, {'valid': False, 'score': 0})
        self.assertEqual(self.game.score, 0)


    def test_requires_all_tiles_to_be_on_a_unique_space(self):
        tiles = make_tiles(
            ["b", 7, 7],
            ["u", 7, 8],
            ["t", 7, 9],
            ["t", 7, 10],
            ["o", 7, 10],
            ["n", 7, 11]
        )

        move = self.game.play_tiles(tiles)
        self.assertEqual(move, {'valid': False, 'score': 0})
        self.assertEqual(self.game.score, 0)


    def test_requires_all_tiles_to_be_placed_in_a_single_row_or_column(self):
        tiles = make_tiles(
            ["b", 7, 7],
            ["u", 7, 8],
            ["t", 7, 9],
            ["t", 7, 10],
            ["o", 7, 11],
            ["n", 8, 11]
        )

        move = self.game.play_tiles(tiles)
        self.assertEqual(move, {'valid': False, 'score': 0})
        self.assertEqual(self.game.score, 0)


    def test_requires_the_first_move_to_have_a_tile_on_7_7(self):
        tiles = make_tiles(
            ["b", 8, 7],
            ["u", 8, 8],
            ["t", 8, 9],
            ["t", 8, 10],
            ["o", 8, 11],
            ["n", 8, 12]
        )

        move = self.game.play_tiles(tiles)
        self.assertEqual(move, {'valid': False, 'score': 0})
        self.assertEqual(self.game.score, 0)


    def test_does_not_allow_replacing_or_overlapping_tiles(self):
        tiles1 = make_tiles(
            ["b", 7, 7],
            ["u", 7, 8],
            ["t", 7, 9],
            ["t", 7, 10],
            ["o", 7, 11],
            ["n", 7, 12]
        )
        self.game.play_tiles(tiles1)
        self.assertEqual(self.game.score, 8)

        tiles2 = make_tiles(
            ["h", 6, 11],
            ["o", 7, 11],
            ["m", 8, 11],
            ["e", 9, 11]
        )
        move = self.game.play_tiles(tiles2)
        self.assertEqual(move, {'valid': False, 'score': 0})
        self.assertEqual(self.game.score, 8)


    def test_requires_subsequent_words_to_share_at_least_one_tile_which_is_scored(self):
        tiles1 = make_tiles(
            ["b", 7, 7],
            ["u", 7, 8],
            ["t", 7, 9],
            ["t", 7, 10],
            ["o", 7, 11],
            ["n", 7, 12]
        )
        self.game.play_tiles(tiles1)
        self.assertEqual(self.game.score, 8)

        tiles2 = make_tiles(
            ["h", 9, 8],
            ["o", 9, 9],
            ["m", 9, 10],
            ["e", 9, 11]
        )
        bad_move = self.game.play_tiles(tiles2)
        self.assertEqual(bad_move, {'valid': False, 'score': 0})
        self.assertEqual(self.game.score, 8)

        tiles3 = make_tiles(
            ["h", 6, 11],
            ["m", 8, 11],
            ["e", 9, 11]
        )
        good_move = self.game.play_tiles(tiles3)
        self.assertEqual(good_move, {'valid': True, 'score': 9})
        self.assertEqual(self.game.score, 17)


    def test_allows_forming_a_new_word_by_adding_tiles_to_the_start_or_end_of_a_word(self):
        tiles1 = make_tiles(
            ["n", 7, 7],
            ["o", 7, 8]
        )

        move = self.game.play_tiles(tiles1)
        self.assertEqual(move, {'valid': True, 'score': 2})
        self.assertEqual(self.game.score, 2)

        tiles2 = make_tiles(
            ["s", 7, 6],
            ["w", 7, 9]
        )

        move = self.game.play_tiles(tiles2)
        self.assertEqual(move, {'valid': True, 'score': 7})
        self.assertEqual(self.game.score, 9)


    def test_only_allows_plays_in_which_all_newly_formed_words_are_valid(self):
        tiles1 = make_tiles(
            ["k", 7, 6],
            ["n", 7, 7],
            ["o", 7, 8],
            ["w", 7, 9]
        )

        move = self.game.play_tiles(tiles1)
        self.assertEqual(move, {'valid': True, 'score': 11})
        self.assertEqual(self.game.score, 11)

        tiles2 = make_tiles(
            ["s", 6, 7],
            ["n", 6, 8],
            ["o", 6, 9],
            ["t", 6, 10]
        )

        move = self.game.play_tiles(tiles2)
        self.assertEqual(move, {'valid': False, 'score': 0})
        self.assertEqual(self.game.score, 11)


    def test_correctly_scores_multiple_newly_formed_words(self):
        tiles1 = make_tiles(
            ["k", 7, 6],
            ["n", 7, 7],
            ["o", 7, 8],
            ["w", 7, 9]
        )

        move = self.game.play_tiles(tiles1)
        self.assertEqual(move, {'valid': True, 'score': 11})
        self.assertEqual(self.game.score, 11)

        tiles2 = make_tiles(
            ["n", 6, 8],
            ["o", 6, 9],
            ["t", 6, 10]
        )

        move = self.game.play_tiles(tiles2)
        self.assertEqual(move, {'valid': True, 'score': 10})
        self.assertEqual(self.game.score, 21)


if __name__ == '__main__':
    unittest2.main()

