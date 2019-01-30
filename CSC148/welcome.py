"""CSC148 - Welcome file

Welcome to CSC148! This is a sample Python file that you should be able to
run after you have completed the steps in the Software Guide
(www.teach.cs.toronto.edu/~csc148h/fall/software/index.html).

To run this file in PyCharm, go to Run -> Run...
and select 'welcome' in the popup menu.
After you've run this program for the first time, you'll be able to
re-run it easily by pressing the green arrow in the toolbar,
or right-clicking on the filename and selecting "Run 'welcome'".
"""
# TODO: fill in the string with your name, and then delete this TODO comment.
MY_NAME = 'MY_NAME_HERE'


def greet(name: str) -> str:
    """Return a welcome message for the given person.

    >>> greet('David')
    'Hello, David! Welcome to CSC148. Hope you have a great time this term. :)'
    """
    # Note: we're using a new style of string formatting that's only available
    # on Python 3.6. This is a good check to make sure you're using the
    # latest version of Python!
    return (f'Hello, {name}! Welcome to CSC148. ' +
            'Hope you have a great time this term. :)')


if __name__ == '__main__':
    print(greet(MY_NAME))

    # This will run our code checking tool, python_ta.
    # You should have downloaded and installed this library in PyCharm
    # as part of following the Software Guide.

    # import python_ta
    # python_ta.check_all()
