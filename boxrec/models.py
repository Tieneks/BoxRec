class Boxer(object):
    def __init__(
            self, id, name
    ):
        self.id = id
        self.name = name


class Fight(object):
    def __init__(
        self, event_id, fight_id,
        boxer_left_id, boxer_right_id,
        hist_rating_left, hist_rating_right,
        curr_rating_left, curr_rating_right,
        stance_left='unknown',stance_right='unknown',
        age_left='QQQ', age_right='QQQ',
        boxer_left=None, boxer_right=None,
        height_left='QQQ',height_right='QQQ',
        reach_left='QQQ',reach_right='QQQ',
        won_left='QQQ', won_right='QQQ',
        lost_left='QQQ', lost_right='QQQ',
        drawn_left='QQQ', drawn_right='QQQ',
        KO_left='QQQ', KO_right='QQQ',
        winner='left'
    ):
        self.event_id = event_id
        self.fight_id = fight_id
        self.boxer_left_id = boxer_left_id
        self.boxer_right_id = boxer_right_id
        self.boxer_right = boxer_right
        self.boxer_left = boxer_left
        self.hist_rating_left = hist_rating_left
        self.hist_rating_right = hist_rating_right
        self.curr_rating_left = curr_rating_left
        self.curr_rating_right = curr_rating_right
        self.stance_left = stance_left
        self.stance_right = stance_right
        self.age_left = age_left
        self.age_right = age_right
        self.height_left = height_left
        self.height_right = height_right
        self.reach_left = reach_left
        self.reach_right = reach_right
        self.won_left = won_left
        self.won_right = won_right
        self.drawn_left = drawn_left
        self.drawn_right = drawn_right
        self.lost_left = lost_left
        self.lost_right = lost_right
        self.KO_left = KO_left
        self.KO_right = KO_right
        self.winner = winner

    @property
    def boxer_left(self):
        if self._boxer_left is None:
            raise NameError('Boxer has not been set')
        return self._boxer_left

    @boxer_left.setter
    def boxer_left(self, val):
        self._boxer_left = val

    @property
    def boxer_right(self):
        if self._boxer_right is None:
            raise NameError('Boxer has not been set')
        return self._boxer_right

    @boxer_right.setter
    def boxer_right(self, val):
        self._boxer_right = val

    @property
    def winning_boxer(self):
        if self.winner == 'drawn':
            return None
        if self.winner == 'left':
            return self.boxer_left
        else:
            return self.boxer_right

