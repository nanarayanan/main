Notes on Python from various sources on the web and from books.

# References

1. Data Science from Scratch, by Joel Grus. [Code examples in this
   book](https://github.com/joelgrus/data-science-from-scratch)

# Design Principles

Python's _Design Priniciples_ known as _The Zen of Python_ can be seen in the
interpreter itself with:
```python
import this
```
which in _Python 3.9_ displays the below:
```
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

# Editing

## Using tabs vs. spaces

Python considers _tabs_ and  _spaces_ as different indentation and we shouldn't
mix the two. The preferred approach is to _use spaces always_, and _never tabs_.

## %paste function in IPython

IPython has a magic function called _%paste_, which correctly pastes whatever
is on your clipboard, whitespace and all. This alone is a good reason to use
IPython.

# Strings

Strings in Python can be specified with _single quotes_ or _double quotes_. For
multiline strings, use _three double quotes_.
```python
tab_string = "\t"
len(tab_string)        # len is 1 as tab_string is a tab character

not_tab_string = r"\t" # a raw string
len(not_tab_string)    # len is 2
```

## String concatentation: using "+", string.format and f-string

first_name, last_name = "Joel", "Grus". To combine them into a single string, we
have three ways:
```python
full_name = first_name + " " + last_name       # String concatenation with "+"
full_name = "{0} {1}".format(first_name, last_name)    # string.format
full_name = f"{first name} {last name}"        # f-string
```

# Exceptions

```python
try:
    print(0 / 0)
except ZeroDivisionError:
    print("cannot divide by zero")
```

# Lists

A **list** is an ordered collection of elements. Elements need not be of the
same type. Lists are mutable in Python. Lists can be defined using `list()` or
`[]`.
```python
integer_list = [1, 2, 3]                # bracketed by []
another_integer_list = list([1,2,3])    # another way to create using list()
nested_integer_list = [[1,2], [2,3]]

mixed_elem_list = [1, "hello", 2.3, "[3,4]", [1, 3.14, "hi"]]

all_list = [integer_list, another_integer_list,
            nested_integer_list, mixed_elem_list]

three_dimen_array = [
                      [
                        [1, 2, 3],
                        [4, 5, 6]
                      ],
                      [
                        [10, 20, 30],
                        [40, 50, 60]
                      ]
                    ]
```

Elements can be retrieved through `[]` and they are 0-indexed. You can also use
square brackets to _slice lists_. The slice `i:j` means all elements from `i`
(inclusive) to `j` (not inclusive). If you leave off the start of the slice,
you'll slice from the beginning of the list, and if you leave of the end of the
slice, you'll slice until the end of the list.
```python
print(mixed_elem_list[4])       # prints [1, 3.14, 'hi']
print(mixed_elem_list[4][1])    # prints 3.14

# Print [[[1, 2, 3], [4, 5, 6]], [[10, 20, 30], [40, 50, 60]]]
print(three_dimen_array)

# Print the 2nd element, which is a 2D array
print(three_dimen_array[1])     # [[10, 20, 30], [40, 50, 60]]

# Prints 6
print(three_dimen_array[0][1][2])

# Prints 60
print(three_dimen_array[-1][-1][-1])

# Prints [10, 20]
print(three_dimen_array[1][0][0:2])
```

Modify elements by subscripting through `[]` and assign new values:
```python
# Change 40 to 400
three_dimen_array[1][1][0] = 400

# Change [20, 30] to [200, 300]
three_dimen_array[1][0][1:] = [200, 300]

# [[[1, 2, 3], [4, 5, 6]], [[10, 200, 300], [400, 50, 60]]]
print(three_dimen_array)
```

## Slices

Operation using slices:
```python
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

first_three = x[:3]                     # [0, 1, 2]
last_three = x[-3:]                     # [7, 8, 9]
one_to_four = x[1:5]                    # [1, 2, 3, 4]
three_to_end = x[3:]                    # [3, 4, 5, 6, 7, 8, 9]
without_first_and_last = x[1:-1]        # [1, 2, 3, 4, 5, 6, 7, 8]
```

A copy of a list can be taken using:
```python
copy_of_x = x[:]
```

A slice can take a third argument to indicate its stride, which can be negative:
```python
every_third = x[::3]                    # [0, 3, 6, 9]
five_to_three = x[5:2:-1]               # [5, 4, 3]
```

# Tuples

Tuples are lists' immutable cousins. Pretty much anything you can do to a list
that doesn't involve modifying it, you can do to a tuple. You specify a tuple by
using parentheses (or nothing) instead of square brackets:
```python
my_list = [1, 2]
my_tuple = (1, 2)
other_tuple = 3, 4
my_list[1] = 3          # my_list is now [1, 3]

try:
    my_tuple[1] = 3
except TypeError:
    print("cannot modify a tuple")
```

Tuples are a convenient way to return multiple values from functions.

# Dictionaries

A dictionary associates values with keys and allows you to quickly retrieve the
value corresponding to a given key:
```python
empty_dict = {}                     # Pythonic
empty_dict2 = dict()                # less Pythonic
grades = {"Joel": 80, "Tim": 95}    # dictionary literal

joels_grade = grades["Joel"]        # equals 80
```

We need to first check for the existence of a key before using that key for
accessing an element:
```python
try:
    kates_grade = grades["Kate"]
except KeyError:
    print("no grade for Kate!")
```

Existence of a key can be checked using `in`:
```python
joel_has_grade = "Joel" in grades       # True
kate_has_grade = "Kate" in grades       # False
```

Dictionaries have a get method that returns a default value (instead of raising
an exception) when you look up a key that isn't in the dictionary:
```python
joels_grade = grades.get("Joel", 0)   # equals 80
kates_grade = grades.get("Kate", 0)   # equals 0
no_ones_grade = grades.get("No One")  # default is None
```

You can assign key/value pairs using the same square brackets:
```python
grades["Tim"] = 99                    # replaces the old value
grades["Kate"] = 100                  # adds a third entry
num_students = len(grades)            # equals 3
```

Dictionary keys must be “hashable”; in particular, you cannot use lists as keys.

## defaultdict

`defaultdict` from module `collections` can be used to simplify coding by not
having to check for the existence of a key everytime in a `dict` and instead
produce a default value of the appropriate type. It is useful when we use
dictionaries to _collect_ results by some key and we don’t want to have to check
every time to see if the key exists yet.

Imagine that you're trying to count the words in a document. An obvious approach
is to create a dictionary in which the keys are words and the values are
counts. Given below are multiple approaches to get the job done, however the
preferred approaches are the ones using `defaultdict` or `Counter`.

Approach 1: Loop through words in a document and increment or assign as appropriate.
```python
word_counts = {}
for word in document:
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1
```

Approach 2: Use exception to handle the case of first assignment.
```python
word_counts = {}
for word in document:
    try:
        word_counts[word] += 1
    except KeyError:
        word_counts[word] = 1
```

Approach 3: Use `get` to assign a default value of 0, if first assignment.
```python
word_counts = {}
for word in document:
    previous_count = word_counts.get(word, 0)
    word_counts[word] = previous_count + 1
```

Approach 4: Use `defaultdict`. A defaultdict is like a regular dictionary,
except that when you try to look up a key it doesn't contain, it first adds a
value for it using a zero-argument function you provided when you created it.
```python
from collections import defaultdict

word_counts = defaultdict(int)  # int() produces 0
for word in document:
    word_counts[word] += 1
```

`defaultdict` can also be useful with `list` or `dict`, and even with your own
function.
```python
dd_list = defaultdict(list)             # list() produces an empty list
dd_list[2].append(1)                    # now dd_list contains {2: [1]}

dd_dict = defaultdict(dict)             # dict() produces an empty dict
dd_dict["Joel"]["City"] = "Seattle"     # {"Joel" : {"City": Seattle"}}

dd_pair = defaultdict(lambda: [0, 0])
dd_pair[2][1] = 1                       # now dd_pair contains {2: [0, 1]}
```

## Counters

A `Counter` turns a sequence of values into a `defaultdict(int)`--like object
mapping keys to counts:
```python
from collections import Counter

c = Counter([0, 1, 2, 0])       # c is (basically) {0: 2, 1: 1, 2: 1}
```

So we can use this to count how many times the words in a document appear if the
document is structured as a list of words.
```python
word_counts = Counter(document)
```

A `Counter` instance has a `most_common` method that is frequently useful:
```python
for word, count in word_counts.most_common(10):
    print(word, count)
```

# Iterables

```python
num2words = { 0: "zero", 1: "one", 2: "two", 3: "three" }
print(num2words.keys)           # .keys is the iterable for the Keys
print(num2words.values)         # .values is the iterable for the Values
print(num2words.items)          # .items is the iterable for (Key, Value) tuples
```

# Functions

```python another_double = lambda x: 2 * x # works, but not the preferred way

def another_double(x):                  # preferred way is to define with "def"
    """Do this instead"""
    return 2 * x
```
