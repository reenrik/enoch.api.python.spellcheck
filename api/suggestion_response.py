
class SuggestionResponse(object):
    correct = False
    suggestions = []

    def __init__(self):
            return super(SuggestionResponse, self).__init__()
    
    def __init__(self, correct, suggestions):
        self.correct = correct
        self.suggestions = suggestions
