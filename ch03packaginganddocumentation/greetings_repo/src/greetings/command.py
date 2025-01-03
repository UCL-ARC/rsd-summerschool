
from argparse import ArgumentParser

from art import art

from .greeter import greet


def process():
    parser = ArgumentParser(description="Generate appropriate greetings")

    parser.add_argument('--title', '-t')
    parser.add_argument('--polite', '-p', action="store_true")
    parser.add_argument('personal')
    parser.add_argument('family')

    arguments = parser.parse_args()

    message = greet(arguments.personal, arguments.family,
                    arguments.title, arguments.polite)
    print(art("cute face"), message)


if __name__ == "__main__":
    process()
