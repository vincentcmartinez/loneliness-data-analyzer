class User:

    def __init__(self, uid):
        self.id = uid
        self.pre_survey_score = None
        self.post_survey_score = None
        self.home = None
        self.avg_time_at_home = None

    def set_pre_score(self, score: int):
        self.pre_survey_score = score

    def set_post_score(self, score: int):
        self.post_survey_score = score

    def data_complete(self):
        return None not in [self.id, self.pre_survey_score, self.post_survey_score, self.home, self.avg_time_at_home]
