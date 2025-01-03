
# Greetings!

This is a very simple example package used as part of the UCL
[Research Software Engineering with Python](development.rc.ucl.ac.uk/training/engineering) course.

## Installation

```bash
pip install git+git://github.com/UCL-ARC-RSEing-with-Python/greeter
```

## Usage
    
Invoke the tool with `greet <FirstName> <Secondname>` or use it on your own library:

```python
from greeting import greeter

greeter.greet(user.name, user.lastname)
```
