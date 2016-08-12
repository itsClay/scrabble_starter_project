from dictionary import dictionary

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
scores = [1,   3,   3,   2,   1,   4,   2,   4,   1,   8,   5,   1,
            3,   1,   1,   3,   10,  1,   1,   1,   1,   4,   4,   8,   4,   10]
scores_by_letter = dict(zip(letters, scores)) # { 'a': 1, 'b': 3, ... }


def make_tiles(*tile_specs):
    """helper function to create list of tile objects from and their coordinates"""
    return [
        {'letter': spec[0], 'row': spec[1], 'col': spec[2]}
        for spec in tile_specs
    ]


class ScrabbleGame(object):
    def __init__(self):
        self.score = 0
        self.first_turn = True
        self.used_tiles = []

    # tiles - List<{ 'letter': String, 'row': Int, 'col': Int }>
    #
    #  an array of objects; each object contains a `letter` (the letter
    #  of the tile to play), a `row` (the row to play the tile in) and
    #  a `col` (the column to play the tile in).
    #
    # score - { 'valid': Boolean, 'score': Int }
    #
    #  `valid` is whether or not the set of tiles represent a valid game
    #  move. If so, `score` is the value of the play to be added to the
    #  score, and if not, `score` is 0.
    #
    def play_tiles(self, tiles):
        has_7_7 = self._has_7_7(tiles)
        is_on_the_board = self._is_on_the_board(tiles)
        is_unique_space = self._is_unique_space(tiles, self.used_tiles)
        has_connecting_tile = self._has_connecting_tile(tiles, self.used_tiles)
        horizontal = self._is_horizontal_move(tiles)
        vertical = self._is_vertical_move(tiles)
        words_in_play = self._word_maker(tiles)
        validated_words = self._word_validator(words_in_play)
        bad_move = {'valid': False, 'score': 0}

        if not horizontal and not vertical:
            return bad_move

        if not is_on_the_board:
            return bad_move

        if not is_unique_space:
            return bad_move

        if not has_connecting_tile and not self.first_turn:
            return bad_move

        if self.first_turn:
            if not has_7_7:
                return bad_move
            else:
                self.first_turn = False

        if validated_words:
            count = self._scores_a_word(words_in_play)
            self.score += count
            self._append_used_tiles(tiles)
            return {'valid': True, 'score': count}
        else:
            return bad_move

    def _scores_a_word(self, word):
        """
        Returns score for our move. assumptions are that all letters are lowercase
        :param word: Unicode encoded string
        :return: Int
        """
        count = 0
        decoded_word = ''.join(map(str, word))
        for letter in decoded_word:
            count += scores_by_letter[letter]
        return count

    def _word_validator(self, word_list):
        """
        Determines if all the words given exist in our dictionary.
        Assumes no string in the word list will be one letter.
        :param word_list: list of unicode strings
        :return: Boolean whether move is valid
        """
        for word in word_list:
            if word not in dictionary:
                return False
        return True

    def _is_on_the_board(self, tiles):
        """
        See if proposed move is within our game board parameters (14x14).
        :param tiles: list of dicts with keys of 'letter', 'row', 'col'
        :return: Bool whether move is valid
        """
        for tile in tiles:
            if tile['row'] > 14 or tile['row'] < 0:
                return False
            elif tile['col'] > 14 or tile['col'] < 0:
                return False
        return True

    def _is_unique_space(self, tiles, tile_list):
        """
        Determines if proposed move has not already been occupied by other tiles.
        :param tiles: list of dicts with keys of 'letter', 'row', 'col'
        :param tile_list: list of dicts with keys of 'letter', 'row', 'col'
        :return: Bool whether move is valid
        """
        for tile in tiles:
            if tile in tile_list:
                return False
        return True

    def _is_horizontal_move(self, tiles):
        """
        If the proposed move is horizontal, return True.
        :param tiles: list of dicts with keys of 'letter', 'row', 'col'
        :return: Bool whether move is valid
        """
        row = tiles[0]['row']
        for tile in tiles:
            if tile['row'] != row:
                return False
        return True

    def _is_vertical_move(self, tiles):
        """
        If the proposed move is vertical, return True
        :param tiles: list of dicts with keys of 'letter', 'row', 'col'
        :return: Bool whether move is valid
        """
        col = tiles[0]['col']
        for tile in tiles:
            if tile['col'] != col:
                return False
        return True

    def _is_single_row_or_column(self, tiles):
        """
        Determines if proposed move has all tiles placed in a single column OR a single row.
        NO SPACES return True
        :param tiles: list of dicts with keys of 'letter', 'row', 'col'
        :return: Bool whether move is valid
        """
        horizontal = self._is_horizontal_move(tiles)
        vertical = self._is_vertical_move(tiles)

        if horizontal:
            current_col = tiles[0]['col']
            for tile in tiles[1:]:
                if tile['col'] == current_col + 1:
                    current_col = tile['col']
                else:
                    return False
            return True
        elif vertical:
            current_row = tiles[0]['row']
            for tile in tiles[1:]:
                if tile['row'] == current_row + 1:
                    current_row = tile['row']
                else:
                    return False
            return True

    def _has_7_7(self, move):
        """
        Given that this is our first turn, return True if our move has a tile that is placed
        at row = 7 and col = 7.
        :param move: list of dicts with keys of 'letter', 'row', 'col'
        :return: Boolean whether move contains a 7,7 play
        """
        if self.first_turn:
            for tile in move:
                if tile['col'] == 7 & tile['row'] == 7:
                    return True
        return False

    def _has_left(self, tile, tile_list):
        """
        Given a current tile, return the connecting tile object if it connects with the column
        to the LEFT.
        :param tile: dict with keys of 'letter', 'row', 'col'
        :param tile_list: list of dicts with keys of 'letter', 'row', 'col'
        :return: tile object
        """
        for current_tile in tile_list:
            if tile['col'] - 1 == current_tile['col'] and tile['row'] == current_tile['row']:
                return current_tile

    def _has_right(self, tile, tile_list):
        """
        Given a current tile, return the connecting tile object if it connects with the column
        to the RIGHT.
        :param tile: dict with keys of 'letter', 'row', 'col'
        :param tile_list: list of dicts with keys of 'letter', 'row', 'col'
        :return: tile object
        """
        for current_tile in tile_list:
            if tile['col'] + 1 == current_tile['col'] and tile['row'] == current_tile['row']:
                return current_tile

    def _has_up(self, tile, tile_list):
        """
        Given a current tile, return the connecting tile object if it connects with the row ABOVE.
        :param tile: dict with keys of 'letter', 'row', 'col'
        :param tile_list: list of dicts with keys of 'letter', 'row', 'col'
        :return: tile object
        """
        for current_tile in tile_list:
            if tile['row'] - 1 == current_tile['row'] and tile['col'] == current_tile['col']:
                return current_tile

    def _has_down(self, tile, tile_list):
        """
        Given a current tile, return the connecting tile object if it connects with the row BELOW.
        :param tile: dict with keys of 'letter', 'row', 'col'
        :param tile_list: list of dicts with keys of 'letter', 'row', 'col'
        :return: tile object
        """
        for current_tile in tile_list:
            if tile['row'] + 1 == current_tile['row'] and tile['col'] == current_tile['col']:
                return current_tile

    def _has_connecting_tile(self, tiles, tile_list):
        """
        Determine if any tile has a connecting tile.
        :param tiles: dict with keys of 'letter', 'row', 'col'
        :param tile_list: list of dicts with keys of 'letter', 'row', 'col'
        :return: Boolean
        """
        for tile in tiles:
            left = self._has_left(tile, tile_list)
            right = self._has_right(tile, tile_list)
            down = self._has_down(tile, tile_list)
            up = self._has_up(tile, tile_list)

            if left or right or down or up:
                return True
        return False

    def _insert_left(self, tile, list, tile_list):
        left = self._has_left(tile, tile_list)

        if left:
            list.insert(0, left)
            self._insert_left(left, list, tile_list)

    def _insert_right(self, tile, list, tile_list):
        right = self._has_right(tile, tile_list)

        if right:
            list.append(right)
            self._insert_right(right, list, tile_list)

    def _insert_down(self, tile, list, tile_list):
        down = self._has_down(tile, tile_list)

        if down:
            list.append(down)
            self._insert_down(down, list, tile_list)

    def _insert_up(self, tile, list, tile_list):
        up = self._has_up(tile, tile_list)

        if up:
            list.insert(0, up)
            self._insert_up(up, list, tile_list)

    def _word_maker(self, tiles):
        """
        Construct a word list from a given tile including a vertical and horizontal play.
        :param tiles: list of dicts with keys of 'letter', 'row', 'col'
        :return: List
        """
        all_usable_letters = tiles + self.used_tiles
        word_list = []

        for tile in tiles:
            vertical_word = self._vertical_word_maker(tile, all_usable_letters)
            horizontal_word = self._horizontal_word_maker(tile, all_usable_letters)

            if len(vertical_word) > 1:
                if vertical_word not in word_list:
                    word_list.append(vertical_word)

            if len(horizontal_word) > 1:
                if horizontal_word not in word_list:
                    word_list.append(horizontal_word)

        return word_list

    def _vertical_word_maker(self, tile, tile_list):
        word_list = [tile]
        col = tile['col']
        word = []

        self._insert_up(tile, word_list, tile_list)
        self._insert_down(tile, word_list, tile_list)

        for current_tile in word_list:
            if current_tile['col'] == col:
                word.append(current_tile['letter'])

        word = u"{}".format(''.join(word))
        return word

    def _horizontal_word_maker(self, tile, tile_list):
        word_list = [tile]
        row = tile['row']
        word = []

        self._insert_left(tile, word_list, tile_list)
        self._insert_right(tile, word_list, tile_list)

        for tile in word_list:
            if tile['row'] == row:
                word.append(tile['letter'])

        word = u"{}".format(''.join(word))
        return word

    def _append_used_tiles(self, tiles):
        for word in tiles:
            self.used_tiles.append(word)