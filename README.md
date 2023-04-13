# MockExample

## What is mocking?

Mocking is a technique that allows you to run tests that would otherwise
be impossible or at least inadvisable: perhaps it's overly complex,
non-deterministic, restricted, or prohibitively expensive in terms
of money, resources, time, etc. Mocking in this sense means to fake
or substitute some piece of code, and is used to override the actual
behavior of running code in a fast, inexpensive, and predictable manner.
(The code that is overridden or replaced is said to be _mocked out_.)

Python mocks are amazing. I like to use a metaphor that a mock is
a sci-fi robot spy, with a cloaking device (or the super-realistic
masks in 'Mission: Impossible'). It's a versatile chameleon that will
confidently answer any question asked of it as if it were the real
thing. The answer can be a static or computed response (the return
value), a change of state, or a back-and-forth 'conversation'. Mocks can
automatically spawn other mocks as needed. They can also give other kinds
of information such as how many times a mocked out function was called
(or if it was called at all) or the specific values it returned to the
caller. It can also generate "side effects": a function can be executed,
or one value from an iterator can be returned each time it is called, or an
exception can be raised.

This article is focused on unit tests that a developer creates to test
the smallest units of functionality, but the concepts and techniques can
be applied at higher levels of testing as well. It is not intended to be
a deep technical study of Python mocking, but rather an introduction to
get you interested and maybe even excited (!) to use this facility.

The [example code](https://github.com/mindthump/MockExample) that
accompanies this article is a working application, but only so far as to
illustrate the features and functionality of the subject. I put together
the application as an aid to my own investigation of mocking in python,
to watch the mocking occur live in a debugger (I prefer PyCharm); I
suggest you do the same. It is not intended to be hardy or safe or
efficient, or show good design, and there is no error checking at all --
it's just an example. You wouldn't necessarily want implement anything
this way, but it serves its purpose.

I encourage you to read
[the official documentation](https://docs.python.org/3/library/unittest.mock.html)
and the many, many other articles about this subject. In fact, this is a
terrific Medium article on this same subject:
[Python Mocking, You Are A Tricksy Beast](https://medium.com/python-pandemonium/python-mocking-you-are-a-tricksy-beast-6c4a1f8d19b2).

## Important Warnings

Mocking without further testing can be dangerous! Should the code you
have mocked out undergo significant change without your knowledge, your
test would not be aware of it and could give you a "false passing"
evaluation. At some point during the testing process (like feature tests
or acceptance tests) you *must* test against the actual code, or risk
critical failures later. Be careful what and where you are mocking.

Good mocking relies on good unit testing practices in general, which
in turn rely on good software design practices. Take a look at Dave
Farley's YouTube videos for
[some terrific advice](https://www.youtube.com/watch?v=v6hP2MXoVrI)
(about many things!).

## A Testing Scenario

Let's say you want to test a method that formats an email based on the
address returned from an external system that takes a very long time to
return.

You want to check your code against various values returned from the
external system -- *without* actually calling the external system, or
altering the original code just to accommodate the test. (Yes, I have
seen production code with `if TEST_MODE return True`.)

Your test in this scenario is intended only to verify the email is
formatted correctly -- you're not testing the external system here.
(That's a different set of tests.) Mock out the parts of *your* code
that _use_ the external code but not the external code directly. For
example, don't create a monster mock that acts like an entire DBMS. In
the unit test, mock out your method that fetches a user's email address
from the database so it returns specific addresses. (You _did_ wrap that
functionality into a small single-purpose method, didn't you?) Then, in
feature or acceptance tests, check that the database really returns the
expected rows so your code returns the correct email addresses.

# How Do I Use Mocking?

There are three simple phases to a mock:

1. MAKE THE MOCK

A mock is usually created by instantiating the `MagicMock()` class
directly, or by patching the code. Patching is overriding existing code
at execution time using a decorator or context manager. A mock can
"stand in" for nearly any kind of object: classes, objects, methods, and more.

Craft the patch as small as you can; whenever possible only the specific behavior
that is actually _used_, such as a single method's return value.
However, there are times a resource class is expensive or impossible to
instantiate, and you may need to patch the whole class (see [[EXAMPLE]]
below). See the documentation
("[Where to Patch](https://docs.python.org/3/library/unittest.mock.html#where-to-patch)")
for details.

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
is a silly application that prints name badges for a sponsored meet-up.
The badges use different formats depending on various attributes of the
people, and you need to validate the badge text.

I am not going to go into deep detail of the example application; I will
only cover as much as needed to understand how the mocking is applied,
so you can start using it yourself. If you are interested, please look
at the GitHub repository. If you are so motivated give it a star, or even
send me a pull request.

These are simple, straightforward examples of mocking in Python unit
tests. What I'm after is pragmatic heuristics to get you started, not an
in-depth discussion about namespaces and bindings.
I use `pytest`, but it could be adapted for any unit test
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
