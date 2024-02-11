class Discriminator:
    def __init__(self):
        pass

    def vectorize(self, current_message, responses: list):
        return responses

    def pick_best_response(self, current_message, responses: list):
        return responses[0]
