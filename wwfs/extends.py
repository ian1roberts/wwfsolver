"""Compute word extensions."""
from collections import Counter
from wwfs.word import Word, WordExtension


def get_word_extensions(word, dictionary, rack=None):
    """Return all words longer than word containing word.
    If given rack, subset for playable words (extra letters in rack).
    """
    playable = set()
    key_letters = Counter(word.word)
    matches = [s for s in dictionary
               if word.word in s and len(s) > len(word)]
    # check that letter differences exist in rack
    if rack:
        for longerword in matches:
            word_letters = Counter(longerword)
            letter_diffs = word_letters - key_letters
            if rack.has_enough_letters(letter_diffs):
                playable.add(longerword)
    else:
        playable = set(matches)
    return playable


def get_letter_overhangs(word, candidate):
    """Return the front / back letter overhangs of word in candidate."""
    index = candidate.find(word.word)
    if index < 0:
        return (False, False)
    front_overhang = candidate[0: index]
    back_overhang = candidate[index + len(word): len(candidate)]
    if front_overhang == word.word or front_overhang == "":
        front_overhang = False
    if back_overhang == word.word or back_overhang == "":
        back_overhang = False
    return (front_overhang, back_overhang)


def move_extends_front_back(side, x, y, direction, board, label, candidate):
    """Check move is valid at front, up or back, down of a played word.
    Computes bonus words in validation of move.
    """
    bonus_words = []
    tmp_word = Word(side, coord=(x, y), direction=direction)
    tmp_squares = board.get_square_xy(tmp_word, x, y, tmp_word.direction)
    if tmp_squares is False:
        return (False, [])  # Can't add to front, doesn't fit Board
    for side_letter, side_sq in zip(side, tmp_squares):
        if side_sq.free:
            # Playable free square, but are neighbour Squares collisions
            # Get that possible collision squares we need to test
            collision_squares = board.check_collisions(
                                                    side_sq, direction, label)
            if collision_squares:
                for (ori, square_collides) in collision_squares:
                    collision_word = square_collides.collision_word(
                                        ori, candidate, tmp_word.direction,
                                        side_letter)
                    #  If collision_word is False .. collision detected
                    if not collision_word:
                        return (False, [])
                    else:
                        bonus_words += collision_word
        elif side_sq.tile_letter == side_letter:
            continue
        else:
            return (False, [])
    return (True, bonus_words)


def is_valid_move_extention(board, word, candidate, tilebag):
    """Candidate word can be legally played on top of word on board."""
    #  get letter / square overhangs
    need_front, need_back = get_letter_overhangs(word, candidate)
    if not (need_front or need_back):
        return False
    candidate_word_extension = WordExtension(candidate,
                                             parent=word, front=need_front,
                                             back=need_back)
    #  test overhangs are playable
    bonus_words = []
    if word.direction == 0:
        candidate_word_extension.direction = 0
        x = word.x
        if need_front:
            y = word.y - len(need_front)
            if y < 0:
                return (False, [])
            candidate_word_extension.front_part_xy = (x, y)
            validmove, bonus_word = move_extends_front_back(
                        need_front, x, y, 0, board, "front", candidate)
            if not validmove:
                return (False, [])
            if bonus_word:
                bonus_words += bonus_word
        if need_back:
            y = word.y + len(word)
            if y + len(need_back) > board.width:
                return (False, [])
            candidate_word_extension.back_part_xy = (x, y)
            validmove, bonus_word = move_extends_front_back(
                        need_back, x, y, 0, board, "back", candidate)
            if not validmove:
                return (False, [])
            if bonus_word:
                bonus_words += bonus_word
    else:
        candidate_word_extension.direction = 1
        y = word.y
        if need_front:
            x = word.x - len(need_front)
            if x < 0:
                return (False, [])
            candidate_word_extension.front_part_xy = (x, y)
            validmove, bonus_word = move_extends_front_back(
                        need_front, x, y, 1, board, "front", candidate)
            if not validmove:
                return (False, [])
            if bonus_word:
                bonus_words += bonus_word
        if need_back:
            x = word.x + len(word)
            if x + len(need_back) > board.width:
                return (False, [])
            candidate_word_extension.back_part_xy = (x, y)
            validmove, bonus_word = move_extends_front_back(
                        need_back, x, y, 1, board, "back", candidate)
            if not validmove:
                return (False, [])
            if bonus_word:
                bonus_words += bonus_word

    candidate_word_extension.squares = board.get_square_xy(
                candidate_word_extension.word,
                candidate_word_extension.x, candidate_word_extension.y,
                candidate_word_extension.direction)

    candidate_word_extension.compute_word_score(
                candidate_word_extension.squares, tilebag)
    if bonus_words:
        for bwd in bonus_words:
            bwd.compute_word_score(tilebag)

    return (candidate_word_extension, bonus_words)
