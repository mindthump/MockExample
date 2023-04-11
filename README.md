# MockExample

## What is mocking?

Mocking is a technique that allows you to run tests that would otherwise
be impossible or at least inadvisable: perhaps it's overly complex,
non-deterministic, restricted, or prohibitively expensive n terms of
money, resources, time, etc. Mocking in this sense means to fake or
substitute a behavior or value, and is used to override the actual
behavior of running code in a fast, inexpensive, and predictable manner.

This article is focused on unit tests that a developer creates to test
the smallest units of functionality, but the concepts and techniques can
be applied at higher levels of testing as well. It is not intended to be
a deep technical study of Python mocking, but rather an introduction to
get you interested and maybe even excited (!) to use this facility. I
encourage you to read [the official documentation](https://docs.python.org/3/library/unittest.mock.html#module-unittest.mock) and the many, many other
articles about this subject.

## A Testing Scenario

Let's say you want to test a method that generates a formatted message
about availability for a given a part number. To do this, it has to
make a call to a service on an external system that takes a very long
time to execute.

Your test is intended to only verify the content and formatting of the
message -- you do not want to test the external system's behavior.
(That's a different test.) You want to check the message generated for
various values returned from the external system -- *without* actually
calling the external system or altering the original code just to
accommodate the test.

To accomplish this, you "mock out" (replace) the call to the external
system during the test and instead substitute known values that you can
use to verify the message content. In other words, you are not mocking
out the code under test itself; you are mocking out something the code
under test is using, at the exact moment it is being used.

Python mocks are amazing. I like to use a metaphor
that a mock is a sci-fi robot spy, with a cloaking device or the
super-realistic masks in 'Mission: Impossible'. It's a versatile
chameleon that will confidently answer any question asked of it as if
it were the real thing. The answer can be a programmed response, or it
can spawn other mocks as needed. Mocks can also give other kinds of
information such as how many times a mocked out function was called or
the specific values it returned to the caller. It can also generate
"side effects" [[INSERT DEFN]].


# How Do I Use Mocking?

There are three simple phases to a mock:

1. MAKE THE MOCK

A mock is usually created by instantiating the MagicMock() class
directly, or by patching the code. Patching is overriding existing code
at execution time using a decorator or context manager. A MagicMock can
"stand in" for nearly any kind of object: classes, objects, methods, and more.

Patch as small as you can; whenever possible only the specific behavior
that is actually _used_, such as a single method's return value.
However, there are times a resource class is expensive or impossible to
instantiate, and you may need to patch the whole class (see [[EXAMPLE]]
below).

1. ARM THE MOCK

You need to configure the mock before deployment. Often the mock either
has a payload to deliver as a `return_value` on a callable, or some
other behavior as a `side_effect()`.

1. FIRE THE MOCK

You trigger the behavior exactly like you would if you were using the
real resource: the code under test doesn't change at all. Once it is set
up, when the original code is called the mock runs instead. How cool is
that?

## The Example Code

The [example code](https://github.com/mindthump/MockExample)
is a silly application that prints name badges for a
sponsored meet-up. The badges use different formats depending on various
attributes of the people, and you need to validate the badge text.

This code is not intended to be hardy or safe or efficient, or show
good design -- it's just for the examples.

I am not going to go into deep detail of the example application; I will
only cover as much as needed to understand how the mocking is applied, so you 
can start using it yourself. If you are interested, please look at the GitHub repository.
If you are motivated give it a star, or even send me a pull request.

These are simple, straightforward examples of mocking in Python unit
tests. What I'm after is pragmatic heuristics to get you started, not an
in-depth discussion about namespaces and bindings. (I originally created
the sample code shown here to watch the mocking occur live in PyCharm's
debugger.) I use `pytest`, but it could be adapted for any unit test
framework.

We will start with a fake data source, `people_data.py`. This is a very
light wrapper around an in-memory `sqlite3` database filled with some
data. The `PeopleData` class represents an expensive or unavailable
resource.

Next we will look at `student.py`, `employee.py`, and `volunteer.py` in
that order. These are the subjects of our example tests, in particular
their `get_badge_text()` methods which access the expensive database.
Each of these classes accesses the data source in a different way,
requiring different mocking techniques.

The `badges.py` application uses all the example classes to print the
badges. It's really stupid and inefficient, but the point is to be able
to see the functions we are testing running in a real (albeit contrived)
context.

Finally, we look at `test_mocking.py` to see the actual unit tests with
mocking in action. Each shows a different way that mocking or patching
can be applied.
