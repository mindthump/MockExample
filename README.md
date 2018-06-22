# MockExample

These are intended to be simple, straightforward examples of mocking in
unit tests in Python, which allow us to examine the values and effects
of things like imports on how objects in need of mocking are named down
where they are used. See Mock (2.7) or mock (3.x+) docs for details. I
use py.test but they could be adapted for any unit test framework.

What I'm after is pragmatic heuristics to get you started, not an
in-depth discussion about namespaces and bindings.

To efficiently examine this code, start with the fake data source
_people_data.py_. This is a very light wrapper around an in-memory
sqlite3 database filled with some data. The class represents an
expensive or unavailable resource.

Next look at _student.py_, _employee.py_, and _volunteer.py_ in that
order. These are the subjects of our example tests, in particular their
**get_xxxx_by_id()** methods. Each of these classes accesses the data
source in a different way, requiring different mocking techniques.
Maybe these classes help print name badges for a sponsored meet-up or
something :)

The 'badges.py' application uses all the example classes. It's really
stupid and inefficient, but the point is to be able to see the functions
we are testing running in a real (albeit contrived) context.

Finally, look at _test_mocking.py_ to see the actual unit tests.
Each shows a different way that mocking or patching can be applied.
_test_mocking_template.py_ has the code without all the profuse
comments, easier to copy and paste.

BTW, this code is not intended to be hardy or safe or efficient, or show
good design -- it's just for the examples.

