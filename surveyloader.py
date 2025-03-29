import csv

from userfactory import UserFactory


def get_rows(file_path: str) -> list[list[str]]:
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = [list(row) for row in reader]
    return data


class SurveyLoader:
    # questions where a 'often' or 'sometimes' response would indicate less loneliness
    positive_items = [0, 3, 4, 5, 8, 9, 14, 15, 18, 19]
    response_vals = {
        "Never": 1,
        "Rarely": 2,
        "Sometimes": 3,
        "Often": 4,
    }

    def __init__(self, userbase: UserFactory):
        self.userbase = userbase

    def set_scores(self, file_path: str):
        rows = get_rows(file_path)
        for i in range(1, len(rows)):
            row = rows[i]
            uid = int(row[0][1:])
            user = self.userbase.get_user(uid)
            if row[1] == "pre":
                user.set_pre_score(self.calculate_score(row))
            else:
                user.set_post_score(self.calculate_score(row))
        return

    def calculate_score(self, row: list[str]) -> int:
        score = 0
        for i in range(2, len(row)):
            question_idx = i - 2
            response_value = self.response_vals[row[i]]
            if question_idx in self.positive_items:
                score += 5 - response_value
            else:
                score += response_value

        return score
