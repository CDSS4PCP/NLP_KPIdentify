import os
import sys

class BaseExperiment:
    def __init__(self, name, config):
        self.name = name
        self.config = config

    def prepare_data(self):
        raise NotImplementedError

    def build_model(self):
        raise NotImplementedError

    def train(self):
        raise NotImplementedError

    def evaluate(self):
        raise NotImplementedError

    def run(self):
        self.prepare_data()
        self.build_model()
        self.train()
        self.evaluate()
