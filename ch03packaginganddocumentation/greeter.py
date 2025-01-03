#!/usr/bin/env python
from argparse import ArgumentParser

def greet(personal, family, title="", polite=False):
    greeting = "How do you do, " if polite else "Hey, "
    if title:
        greeting += f"{title} "

    greeting += f"{personal} {family}."
    return greeting

def process():
    parser = ArgumentParser(description="Generate appropriate greetings")

    parser.add_argument('--title', '-t')
    parser.add_argument('--polite', '-p', action="store_true")
    parser.add_argument('personal')
    parser.add_argument('family')

    arguments = parser.parse_args()

    print(greet(arguments.personal, arguments.family,
                arguments.title, arguments.polite))    

if __name__ == "__main__":
    process()
