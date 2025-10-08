from faker import Faker

from src.standard.built_in.Static import Static

Faker.seed(1090)


class AppTestFaker(Static):
    fake = Faker()
