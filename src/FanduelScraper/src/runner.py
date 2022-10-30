class Runner:
    def __init__(self, details):
        self.runner_name = details.get('runnerName')
        self.selection_id = details.get('selectionId')
        self.handicap = details.get('handicap')
        self.runner_status = details.get('runnerStatus')
        self.runner_result_type = details.get('result', {}).get('type')
        self.sort_priority = details.get('sortPriority')
        self.odds_american = details.get('winRunnerOdds', {}).get('americanDisplayOdds',{}).get('americanOdds')
        self.odds_true_odds = details.get('winRunnerOdds', {}).get('trueOdds')

    def to_list(self):
        return [
            self.runner_name,
            self.selection_id,
            self.handicap,
            self.runner_result_type,
            self.odds_american
        ]

    def to_dict(self):
        return {
            "runner_name": self.runner_name,
            "selection_id": self.selection_id,
            "runner_result_type": self.runner_result_type,
            "handicap": self.handicap,
            "odds": self.odds_american
        }
    def __str__(self):
        return "{self.selection_id} - {self.runner_name}".format(self=self)