BATCH_SIZE = 32


class Discriminator:
    def __init__(self, input_size, *args, **kwargs):
        self.input_size = input_size

    def forward(self, x):
        return x

    def train_discriminator(self):
        pass

    def add_to_training_data(self, current_message, feedback: int):
        pass

    def pick_best_response(self, current_message, responses: list):
        return responses[0]


if __name__ == '__main__':
    disc = Discriminator(1500)
    disc.add_to_training_data("Hello", 1)
    disc.add_to_training_data("Hi", 0)
    disc.train_discriminator()
