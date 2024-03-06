import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

BATCH_SIZE = 32


class Discriminator(nn.Module):
    def __init__(self, input_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fc1 = nn.Linear(input_size, 512)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(512, 1)
        self.sigmoid = nn.Sigmoid()

        self.vectorizer = CountVectorizer()
        self.latest_training_data = []

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.sigmoid(x)
        return x

    def train_discriminator(self):
        X = [x[0] for x in self.latest_training_data]
        y = [x[1] for x in self.latest_training_data]
        X = self.vectorizer.fit_transform(X).toarray()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        train_dataset = list(zip(X_train, y_train))
        test_dataset = list(zip(X_test, y_test))

    def add_to_training_data(self, current_message, feedback: int):
        self.latest_training_data.append((current_message, feedback))
        if len(self.latest_training_data) >= BATCH_SIZE:
            self.train_discriminator()

    def pick_best_response(self, current_message, responses: list):
        return responses[0]


if __name__ == '__main__':
    disc = Discriminator(1500)
    disc.add_to_training_data("Hello", 1)
    disc.add_to_training_data("Hi", 0)
    disc.train_discriminator()
