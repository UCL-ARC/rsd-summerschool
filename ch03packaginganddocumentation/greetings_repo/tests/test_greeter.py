
from pathlib import Path

import pytest
import yaml

from greetings.greeter import greet

def read_fixture():
    with open(Path(__file__).parent / 'fixtures' / 'samples.yaml') as fixtures_file:
        fixtures = yaml.safe_load(fixtures_file)
    return fixtures

@pytest.mark.parametrize("fixture", read_fixture())
def test_greeter(fixture):
    answer = fixture.pop('answer')
    assert greet(**fixture) == answer
