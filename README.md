# MockExample

## Project Intention
These are simple, straightforward examples of mocking in Python unit
tests. What I'm after is pragmatic heuristics to get you started, not an
in-depth discussion about namespaces and bindings.

I created the project originally so I could watch the mocking occur live in the debugger.

See Mock (2.7) or unittest.mock (3.x+) documentation for details.

I use py.test, but they could be adapted for any unit test framework.

## The Code

To efficiently examine this code, start with the fake data source
_people_data.py_. This is a very light wrapper around an in-memory
sqlite3 database filled with some data. The class represents an
expensive or unavailable resource.

Next look at _student.py_, _employee.py_, and _volunteer.py_ in that
order. These are the subjects of our example tests, in particular their
**get_badge_text()** methods. Each of these classes accesses the data
source in a different way, requiring different mocking techniques.
Maybe these classes help print name badges for a sponsored meet-up or
something :)

The _badges.py_ application uses all the example classes. It's really
stupid and inefficient, but the point is to be able to see the functions
we are testing running in a real (albeit contrived) context.

Finally, look at _test_mocking.py_ to see the actual unit tests.
Each shows a different way that mocking or patching can be applied.

BTW, this code is not intended to be hardy or safe or efficient, or show
good design -- it's just for the examples.
