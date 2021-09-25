Notes on Golang from various sources on the web and from books.

# References

1. **The Go Programming Language** book, by _Alan Donovan and Brian Kernighan_
2. Go standard library packages: https://pkg.go.dev/std
3. https://learning.oreilly.com/videos/learning-path-go/9781491958100/
4. Go playground: https://play.golang.org/
5. https://tour.golang.org/
6. https://groups.google.com/g/golang-nuts
7. https://go101.org/
8. https://github.com/golang/go/issues
9. https://research.swtch.com/
10. https://github.com/avelino/awesome-go

# Introduction

Developed by Robert Griesemer, Rob Pike, and Ken Thompson of Google and with
some concepts leveraged from multiple programming languages like Algol, Pascal,
Modula, Oberon, C, CSP, Squeak, Newsqueak, Alef, etc.

# Usage of semicolon

Go does not require semicolons at the end of statements or declarations, except
where two or more appear on the same line. In effect, newlines following certain
tokens are converted into semicolons, so where newlines are placed matters to
proper parsing of Go code. For instance, the opening brace `{` of the function
must be on the same line as the end of the `func` declaration, not on a line by
itself, and in the expression `x+y`, a newline is permitted after but not before
the `+` operator.

# for, if, switch statements

`for`, `if` and `switch` statements are similar to `C` language. In Go, there is
a _tagless switch_ version that doesn't need an operand; it is equivalent to
`switch true`.

`for`, `if` and `switch` statements may include an optional simple statement---a
short variable declaration, an increment or assignment statement, or a function
call---that can be used to set a value before it is tested.

Unlike `C`, `Go switch's` case statements don't need a `break`; their default
behavior is to break after executing a `case`. To fallthrough to the subsequent
`case` statement, there is a rarely used `fallthrough` statement. Go's switch
cases need not be constants, and the values involved need not be integers.

Similar to `C`, `Go` has `break` and `continue` statements.

# Keywords

Go has 25 keywords:
```go
break         default         func         interface         select
case          defer           go           map               struct
chan          else            goto         package           switch
const         fallthrough     if           range             type
continue      for             import       return            var
```

# Scope of Entities

In Go, we can use a pair of `{` and `}` to form a code block. A code block can
nest other code blocks. A variable or a named constant declared in an inner code
block will shadow the variables and constants declared with the same name in
outer code blocks.
```go
func main() {
    var i, j = 100, 200
    {
        /*
           The right-hand side i, j refer to the outer scope's i, j. So the
           snippet below declares two new vars i and j and that are initialized
           to 100 and 200 respectively. From here on, the "new" i and j vars
           mask the ones outside --- till we exit this code block.
         */
        var i, j = i, j
        i, j, z := 2*i, 3*j, 300        // modify the "inner" i and j; declare z
        fmt.Println(i, j, z)            // i = 200; j = 600; z = 300
    }
    fmt.Println(i, j)   // "inner" i and j are not in scope; i = 100; j = 200
    fmt.Println(z)      // compilation error as z is no longer in scope
}
```

If an entity is declared within a function, it is local to that function. If
declared outside of a function, however, it is visible in all files of the
package to which it belongs. _The case of the first letter of a name determines
its visibility across package boundaries_. If the name begins with an upper-case
letter, it is exported, which means that it is visible and accessible outside of
its own package and may be referred to by other parts of the program, as with
`Printf` in the fmt package. Package names themselves are always in lower case.

# Declarations and Assignments

There are four major kinds of declarations: `var`, `const`, `type`, and `func`.

## Variable `var` Declarations

```go
    // var name type = expression

    s := ""             // 1st form
    var s string        // 2nd form
    var s = ""          // 3rd form
    var s string = ""   // 4th form
```

The first form is known as **short variable declaration**. This form can be used
only within a function, and can't be used for package-level vars.

The second form depends on the default initialization of a string, which is "".

The third form is rarely used except when declaring multiple vars.

The fourth form is explicit about the variable's type, which is redundant when
it is the same as that of the initial value but necessary in other cases where
they are not of the same type.

*In practice, you should generally use one of the first two forms, with explicit
initialization to say that the initial value is important and implicit
initialization to say that the initial value doesn't matter.*

A var declaration tends to be reserved for local variables that need an explicit
type that differs from that of the initializer expression, or for when the
variable will be assigned a value later and its initial value is unimportant.

## Identifiers can be made up of non-ASCII letters

The declaration below is valid and `π` is a valid identifier. Go accepts
programs written in UTF-8.
```go
var π = 3.1416                          // a valid identifier
fmt.Printf("type(π) = %T\n", π)         // type(π) = float64
```

## No problem of Uninitialized Variables

**var name type = expression**

Either the type or the _= expression_ part may be omitted, but not both. If the
type is omitted, it is determined by the _initializer_ expression. If the
expression is omitted, the _initial value is the zero value for the type_, which
is `0` for numbers, `false` for booleans, `""` for strings, and `nil` for
interfaces and reference types (slice, pointer, map, channel, function).

The zero value of an aggregate type like an array or a struct has the zero value
of all of its elements or fields. The zero-value mechanism ensures that a
variable always holds a well-defined value of its type; **in Go there is no
such thing as an uninitialized variable**.

```go
var i, j, k int                 // int, int, int
var b, f, s = true, 2.3, "four" // bool, float64, string

m, n := 0, 1                    // declare and initialize short var declarations
```

## Unused variables are flagged as errors during compilation

Go expects variables declared are used; if not, the compiler flags an error. For
instance, build of the below fails with `i declared but not used`.
```go
func main() {
    i := 100
    fmt.Println("Hello, world");
}
```

However this restriction is not applicable to package level variables.

## short variables: declaration vs. assignment

1. A short variable declaration, the `var` keyword and the variable type must be
omitted.
2. The declaration sign must be `:=` instead of `=`.
3. A short variable declaration must declare at least one new variable,
4. All items to the left of `:=` shall be _pure identifiers_. This means some
   other items that can be assigned to can't appear to the left of `:=`; two
   such examples are _pointer dereferences_ and _struct field selectors_. _Pure
   assignments don't have any such restrictions_.

A short variable declaration does not necessarily declare all the variables on
its left-hand side. If some of them were already declared in the same lexical
block, then the short variable declaration acts like an assignment to those
variables.

```go
in, err := os.Open(infile)      // declare two short variables "in" and "err"
// ...
out, err := os.Create(outfile)  // declaration of "out" but assignment to "err"
```

## About the terminology "Assignment"

**Assignment** may mean a pure assignment, a short variable declaration, a
variable specification with an initial value in a standard variable declaration,
passing of arguments to a function, etc.

We say **x is assignable to y** if `y = x` is a legal statement (compiles
fine).

## Multiple variables can be declared together

If multiple variables are declared together and a type is given, the type is
applicable to all these vars; _a group declaration with an explicit type
**can't** have vars with differing types_.
```go
var lang, website string = "Go", "https://golang.org"
var compiled, dynamic bool = true, false
var announcedYear int = 2009
```

If multiple vars are declared together and without specifying an explicit type,
we have to specify their initial values; _a group declaration without an
explicit type **can** have vars with differing types_.
```go
var lang, dynamic = "Go", false                 // string, bool
var compiled, announcedYear = true, 2009        // bool, int
var website = "https://golang.org"              // string
```

Multiple variables declared together as a group --- see the example below:
```go
var (
    lang, bornYear, compiled = "Go", 2007, true
    announcedYear, releasedYear int = 2009, 2012        // int is redundant here
    createdBy, website string
)
```

## Variables declared at the Package level

Variables declared at the package level may be unused; unlike local variables,
compiler doesn't flag an error for unused package level vars.

Dependency relations of package level vars affect their initialization order.
```go
var x, y    = a+1, 5            // 8  5
var a, b, c = b+1, c+1, y       // 7  6  5
```
The initialization order of the package-level variables are `y = 5`, `c = y`, `b = c+1`, `a = b+1`, and `x =
a+1`.

## Constants

Constants can be character, string, boolean, or numeric values.

Constants cannot be declared using the `:=` syntax.

The _declaration order of two package-level constants isn't important_. In the
snippet below, the declaration order of `No` and `Yes` can be
exchanged. However, **order matters for local constants**, for instance, those
declared within a function.
```go
const Pi = 3.14
const Truth = true

// Declare multiple constants in a group.
const (
    No         = !Yes           // Order of No and Yes doesn't matter
    Yes        = true
    MaxDegrees = 360
    Unit       = "radian"
)

// However, for local constants, order matters.
func main() {
    const (
        Two = One + 1   // compilation error indicating One is undefined
        One = 1
    )
}
```

Numeric constants are high-precision values.
```go
const BigVal = 1 << 100

// compilation failure: constant 1267650600228229401496703205376 overflows int
fmt.Println(BigVal)

fmt.Println(float32(BigVal))    // 1.2676506e+30
fmt.Println(float64(BigVal))    // 1.2676506002282294e+30

const BiggerVal = 1 << 127
fmt.Println(float32(BiggerVal)) // 1.7014118e+38
fmt.Println(float64(BiggerVal)) // 1.7014118346046923e+38

fmt.Println(1e309)              // constant 1e+309 overflows float64

// Prints float64 1.7976931348623157e+308
fmt.Printf("%[1]T %[1]v\n", math.MaxFloat64)

// Prints complex128 (1.7976931348623157e+308+1.7976931348623157e+308i)
fmt.Printf("%[1]T %[1]v\n", complex(math.MaxFloat64, math.MaxFloat64))
```

## An untyped const value can overflow its default type

The following compiles fine without any error, however the results may not be
something expected, due to truncation, wrap-around etc.
```go
const N = 1 << 64       // overflows int, however no compilation error
```

The following don't even compile because a type is specified:
```go
const M int = 1 << 64       // type specified; overflows int; fails to compile
const Y = 128 - int8(1)     // error: 128 overflows int8
const Z = uint8(255) + 1    // error: 256 overflows uint8
```

## Autocomplete in const declarations

Consider the code `const` declaration below. `Y` and `Z` are filled with the
same value as of `X` and `C` is filled with the same value of `A`. Note the need
for a blank identifier as autocompletion requires the same number of identifiers
as the ones with their values declared explicitly.
```go
const (
    X float32 = 3.14
    Y                   // there must be one identifier
    Z                   // there must be one identifier

    A, B = "Go", "language"
    C, _                // requires a blank identifier
)
```

The above is same as
```go
const (
    X float32 = 3.14
    Y float32 = 3.14
    Z float32 = 3.14

    A, B = "Go", "language"
    C, _ = "Go", "language"
)
```

## iota in const declarations

The autocomplete feature plus the `iota` constant generator feature is a very
convenient feature. `iota` is a predeclared constant and it can be used only in
other const declarations. It is useful only in group-style const
declarations. Its initial value in a group is 0 and every succeeding usage
automatically increments the value by 1 at compile time. Consider the below
examples:
```go
const (
    Failed = iota - 1   // equivalent to (0 - 1) and so Failed equals -1
    Unknown             // now iota is 1 and so Unknown equals (1 - 1) = 0
    Succeeded           // now iota is 2 and so Succeeded = (2 - 1) = 1
)

const (
    Readable = 1 << iota        // 1 << 0 and so Readable is 1
    Writable                    // now iota is 1 and Writable = 1 << 1 = 2
    Executable                  // now iota is 2 and Executable = 1 << 2 = 4
)
```

Note that `iota` need not be explicitly specified at the first declaration.
```go
const (
    k = 3               // though iota is not specified, consider its value as 0

    m float32 = iota + .5 // now iota is 1; so m equals (1 + .5) = 1.5
    n                     // now iota is 2; so n equals (2 + .5) = 2.5

    p = 9                 // now iota is 3
    q = iota * 2          // now iota is 4; so q equals (4 * 2) = 8
    _                     // now iota is 5; so _ = (5 * 2)
    r                     // now iota is 6; so r equals (6 * 2) = 12
    s, t = iota, iota     // s, t = 7, 7
    u, v                  // u, v = 8, 8
    _, w                  // _, w = 9, 9
```

## Function `func` Declarations

A function declaration has a name, a list of parameters (the variables whose
values are provided by the function’s callers), an optional list of results, and
the function body, which contains the statements that define what the function
does. The result list is omitted if the function does not return anything.

```go
func incr(p *int) int {
    *p++                        // increments what p points to; does not change p
    return *p
}

v := 1
incr(&v)                        // side effect: v is now 2
fmt.Println(incr(&v))           // "3" (and v is 3)
```

# Tuple Assignments

Keep in mind that `:=` is a declaration, whereas `=` is an assignment.

All of the right-hand side expressions are evaluated before any of the variables
are updated, making this form most useful when some of the variables appear on
both sides of the assignment, as happens, for example, when swapping the values
of two variables:
```go
i, j = j, i                     // swap values of i and j
```

A function can return a tuple, in which case, we need to have as many variables
on the left-hand side as there are elements in the return.
```go
f, err = os.Open("foo.txt")     // function call returns two values
```

The operators _map lookup_, _type assertion_ and _channel receive_ also need a
tuple assignment as each of these operators produce an additional boolean
result.
```go
v, ok = m[key]                  // map lookup
v, ok = x.(T)                   // type assertion
v, ok = <-ch                    // channel receive
```

As with variable declaration, we can assign unwanted values to `_ (the blank identifier)`.
```go
_, err = io.Copy(dst, src)      // discard byte count
_, ok = x.(T)                   // check type but discard result
```

If the element to be discarded is the right-most one, we don't even need to
assign it to `_` and can be left out. For instance, in the snippet below, while
assigning using `range`, as we are interested in only the index `ind` and not
the actual element from `words`, we just assign it to `ind` instead of using the
tuple `ind, _`.
```go
func myPrint() {
    words := []string{"One", "Two", "Three", "Four"}
    for ind := range words {    // same as ind, _
        fmt.Println(ind)
    }
}
```

# Lifetime of Variables, Garbage Collection

The lifetime of a variable is the interval of time during which it exists as the
program executes. The lifetime of a package-level variable is the entire
execution of the program.

The basic idea of _garbage collection_ is that every package-level variable, and
every local variable of each currently active function, can potentially be the
start or root of a path to the variable in question, following pointers and
other kinds of references that ultimately lead to the variable. If no such path
exists, the variable has become unreachable, so it can no longer affect the rest
of the computation.

Because the lifetime of a variable is determined only by whether or not it is
reachable, a local variable may outlive a single iteration of the enclosing
loop. It may continue to exist even after its enclosing function has returned.

**A compiler may choose to allocate local variables on the heap or on the stack
but, perhaps surprisingly, this choice is not determined by whether `var` or
`new` was used to declare the variable.**
```go
var global *int

func f() {                                              func g() {
    var x                                                   int y := new(int)
    x=1                                                     *y = 1
    global = &x                                         }
}
```

Here, `x` must be _heap-allocated_ because it is still reachable from the
variable `global` after `f` has returned, despite being declared as a local
variable; we say `x` escapes from `f`. Conversely, when `g` returns, the
variable `*y` becomes unreachable and can be recycled. Since `*y` does not
escape from `g`, it's safe for the compiler to allocate `*y` on the stack, even
though it was allocated with `new`. In any case, the notion of escaping is not
something that you need to worry about in order to write correct code, though
it's good to keep in mind during performance optimization, since each variable
that escapes requires an extra memory allocation.

## Automatic GC and its Implications

Garbage collection is a tremendous help in writing correct programs, but it does
not relieve you of the burden of thinking about memory. You don't need to
explicitly allocate and free memory, but to write efficient programs you still
need to be aware of the lifetime of variables.  For example, keeping unnecessary
pointers to short-lived objects within long-lived objects, especially global
variables, will prevent the garbage collector from reclaiming the short-lived
objects.

# Basic types

```
bool

string

int  int8  int16  int32  int64
uint uint8 uint16 uint32 uint64 uintptr

byte // alias for uint8

rune // alias for int32
     // represents a Unicode code point

float32 float64

complex64 complex128
```

# Variable declarations can be factored into blocks

```
package main

import (
    "fmt"
    "math/cmplx"
)

var (
    ToBe   bool       = false
    MaxInt uint64     = 1<<64 - 1
    z      complex128 = cmplx.Sqrt(-5 + 12i)
)

func main() {
    fmt.Printf("Type: %T Value: %v\n", ToBe, ToBe)
    fmt.Printf("Type: %T Value: %v\n", MaxInt, MaxInt)
    fmt.Printf("Type: %T Value: %v\n", z, z)
}
```
# Aggregate type: struct

```go
type Vertex struct {
    X, Y int
}

func main() {
    v := {Y: 200, X: 100}       // Order irrelevant due to eplicitly naming
    fmt.Println(v)
}
```

# Named types

A **type** declaration gives a _name_ to an existing type.
```go
type Point struct {
    X, Y int
}
var p Point
```

In the below two types, though the underlying type is same, `float64`, they
can't be compared or combined in arithmetic expressions.
```go
type Celsius float64
type Fahrenheit float64

type status = bool
type real = float32
```

Distinguishing the types makes it possible to avoid errors like inadvertently
combining temperatures in the two different scales; an explicit type conversion
like `Celsius(t)` or `Fahrenheit(t)` is required to convert from a
`float64`. `Celsius(t)` and `Fahrenheit(t)` are _conversions_, not function
calls. They don't change the value or representation in any way, but they make
the change of meaning explicit.

Type declarations most often appear at package level, where the named type is
visible throughout the package, and if the name is exported (it starts with an
upper-case letter), it’s accessible from other packages as well.

# Type Conversion

`T(v)` or `(T)(v)` where the value `v` is attempted to be converted to type `T`.

A conversion from one type to another is allowed if both have the same
underlying type, or if both are unnamed pointer types that point to variables of
the same underlying type; _these conversions change the type but not the
representation of the value_.

Conversions are also allowed between numeric types, and between string and some
slice types. These conversions may change the representation of the value. For
instance, converting a floating-point number to an integer discards any
fractional part, and converting a `string` to a `[]byte` slice allocates a copy
of the string data. In any case, _a conversion never fails at run time_.

Comparison operators like `==` and `<` allow comparison of a value of a named
type to a value of the underlying type. So it is possible to compare a `Celsius`
value or a `Fahrenheit` value with a `float64` value.

## Type T(v) where T is a string and v is an integer

The result of `T(v)` is a string of type T and contains the UTF-8 representation
of the integer as a Unicode code point. Integer values outside the range of
valid Unicode code points produce strings represented by "\uFFFD" (a.k.a.,
"\xef\xbf\xbd"). 0xFFFD is the code point for the Unicode replacement
character. _The result string of a conversion from an integer always contains one
and only one rune._

```go
fmt.Println(string(0141))               // Prints a and NOT a string "0141"
fmt.Println("\xef\xbf\xbd" == "\uFFFD") // Prints true
```

The following conversions are valid, however the conversion results in a code
point for the Unicode replacement character.
```go
fmt.Println(string(-1))                 // "\uFFFD"
fmt.Println(string(0xFFFD))             // "\uFFFD"
fmt.Println(string(0x2FFFFFFFF))        // "\uFFFD"
```

Running `go vet` in a program using the above displays the warning: `from
untyped int to string yields a string of one rune, not a string of digits (did
you mean fmt.Sprint(x)?)`

## Illegal Type Conversions

```go
int(1.23)       // 1.23 is not representable as a value of int.
uint8(-1)       // -1 is not representable as a value of uint8.
float64(1+2i)   // 1+2i is not representable as a value of float64.

float(-1e+1000)                 // Constant -1e+1000 overflows float64.
int(0x10000000000000000)        // Constant 0x10000000000000000 overflows int.
string(65.0)                    // 65.0 is a float64 and not an integer type.
string(66+0i)                   // of type complex128 and not an integer type.
```

# Type Inference (or Type Deduction)

When the right hand side of the declaration is typed, the new variable is of
that same type:
```go
var i int
j := i                  // j is an int
```

When the right hand side contains an untyped numeric constant, the new variable
may be an int, float64, or complex128 depending on the precision of the
constant:
```go
i := 42                 // int
f := 3.142              // float64
g := 0.867 + 0.5i       // complex128
```

# Literals

## Floating Point, Octal, Hexadecimal with power-of-10

```go
f := 3.142e0            // 3.142 * ⏨0
g := 0.03142e2          // 0.03142 * ⏨2
g1 := 31.42e-1          // 30.142 * ⏨-1
f1 := 010.12            // same as 10.12 and not an octal number

o := 010                // octal 10 = decimal 8
o1 := 0O10              // octal 10 = decimal 8
o2 := 0o10              // octal 10 = decimal 8

h := 0xf                // hex f = decimal 16
h1 := 0xF               // hex F = decimal 16
```

## Hexadecimal floating point with power-of-2

```go
h2 := 0x12.2p3          // (0x12 + 2.0/16)*2^3 = (18.125 * 8) = 145.0
0x1p-2                  // 1.0/4 = 0.25
0x2.p10                 // 2.0 * 2^10 = 2.0 * 1024 = 2048.0
0x1.Fp+0                // 1 + 15.0/16 = 1.9375
0X.8p1                  // 8.0/16 * 2 = 1.0
0X1FFFP-16              // 0x1fff * 2^-16 = 0x1fff / 2^16 = 0.1249847412109375
```

Note that the following is not an exponent because there is no decimal
point. `go fmt` formats the below as `0x15e - 2`.
```go
a := 0x15e-2            // same as (0x15e - 2) and NOT (0x15 * ⏨-2)
```

The following are invalid literals
```go
0x.p1                   // hexadecimal literal has no digits
1p-2                    // 'p' exponent requires hexadecimal mantissa
0x1.5e-2                // hexadecimal mantissa requires a 'p' exponent
```

## _ as separators in literals for better readability

Below are valid literals:
```go
6_9                     // 69
0x_12_34_ab             // 0x1234ab
0_12_34_56              // 0123456
0X12_34_AB_FFP-16       // 0X1234ABFFP-16
0b_1_01_001_11          // 0b10100111
```

Below are invalid literals. `_` needs to appear between digits or after the
prefix `0x`, `0o`, `0b`.
```go
_6_9                    // invalid; _ can't be the 1st character.
6._9                    // invalid; _ must separate successive digits.
6.9_                    // invalid; _ can't be the last character.
```

## Rune Literals

A rune literal denotes an Unicode code point. An Unicode character comprises one
or more rune literals. It is enclosed in single-quotes and can be represented as
below (Unicode value of char a --- value 97):
```go
'\141'                  // three octal digits followed by \
'\x61'                  // two hex digits followed by \x
'\u0061'                // four hex digits followed by \u
'\U00000061'            // eight hex digits followed by \U
```

A rune literal like `'\n'` with two characters represent an escape sequence, for
instance, `line feed` or `newline`.

## String value literals

String values in Go are UTF-8 encoded. In fact, all Go source files must be
UTF-8 encoding compatible.

The following two forms are equivalent.
```go
"Hello\nworld!\n\"你好世界\""   // interpreted string literal (double-quote form)

// raw string literal (backquote form) below. It can straddle multiple lines.
`Hello
world!
"你好世界\"`
```

The following interpreted string literals are equivalent.
```go
"\141\142\143"
"\x61\x62\x63"
"\x61b\x63"
"abc"
```

Note that \\" is legal only in interpreted string literals and \\` is legal only
in rune literals. In a raw string literal, no character sequences will be
escaped. The backquote character is not allowed to appear in a raw string
literal. To get better cross-platform compatibility, carriage return characters
(Unicode code point 0x0D) inside raw string literals are discarded.

# Functions with Named Return Values

The 2nd form below is an example of "Named Return Value". It is similar to `val`
being declared at the top of the function. It is meant to document the meaning
of the return values.

```go
func add(x, y int) int {
    return x+y
}

(OR)

func add(x, y int) (val int) {
    val = x+y
    return
```

The "naked" `return` statement above returns `val` because of the named return
value; however, it may impact readability and hence is meant only for small
functions.

# Pointers

A pointer value is the address of a variable.

If a variable is declared `var x int`, the expression `&x` ("address of x")
yields a pointer to an integer variable, that is, a value of type `*int`, which
is pronounced _pointer to int_. If this value is called `p`, we say _p points to
x_, or equivalently _p contains the address of x_. The variable to which `p`
points is written `*p`.

**It is perfectly safe for a function to return the address of a local
variable.**
```go
var p = f()

func f() *int {
    v := 1
    return &v
}

// Each call of f returns a distinct value:
fmt.Println(f() == f())         // "false"
```

Each time we take the address of a variable or copy a pointer, we create new
aliases or ways to identify the same variable. It's not just pointers that
create aliases; aliasing also occurs when we copy values of other reference
types like _slices_, _maps_, and _channels_, and even _structs, arrays, and
interfaces that contain these types_.

**Unlike the C language, Go doesn't have pointer arithmetic**.

In the sample program below, unlike the "C language", Go doesn't have a "->"
operator. So it is OK to access `(*p).X` as `p.X`.
```go
type Vertex struct {
    X int
    Y int
}

func main() {
    v := Vertex{1, 2}
    p := &v
    p.X = 1e2           // Note: We don't need a "->" operator as in C
    fmt.Println(v)
}
```

# Arrays

The `type [n]T` is an `array of n values` of `type T`.

**Unlike the C language, passing an array in Go will result in a copy of the whole
array**. This can be expensive and to avoid this copying, _slice_ can be used.
```go
/*
 * This sample program shows arrays in Go copy the values
 */
package main

import (
    "fmt"
)

func myPrint(words [9]string) {
    for _, w := range words {
        fmt.Printf(" %s", w)
    }

    fmt.Printf("\n")

    words[0] = "Modified in myPrint"    // caller doesn't see this modification
}

func main() {
    words := [9]string{"The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"}
    myPrint(words)
    myPrint(words)
}
```

If we want the modification in `myPrint()` to be visible to the caller, pass a
slice `[]string` between `main()` and `myPrint()` instead. This can be done as
below:
```go
Modifications in main():

    // Array declaration changed to slice
    // A slice is passed from main() to myPrint()

    words := []string{"The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"}
    myPrint(words[0:])          // now we are passing a slice from main() to myPrint()
    myPrint(words[0:])

Modifications in myPrint():

func myPrint(words []string) {
    // No change other than the param change to get a slice from the caller
}
```

# Slice

An array has a fixed size. A slice, on the other hand, is a dynamically-sized,
flexible view into the elements of an array. In practice, slices are much more
common than arrays.

The `type []T` is a `slice with elements of type T`.

A slice is formed by specifying two indices, a low and high bound, separated by
a colon:
`a[low : high]`
This selects a half-open range which includes the first element, but excludes
the last one.

## Slices are like references to arrays

A slice does not store any data, it just describes a section of an underlying
array.

Changing the elements of a slice modifies the corresponding elements of its
underlying array.

Other slices that share the same underlying array will see those changes.

## Slice literals

A slice literal is like an array literal without the length.

This is an array literal:
`[3]bool{true, true, false}`

This creates the same array as above, then builds a slice that references it:
`[]bool{true, true, false}`

## Byte Slices

Given below is a sample program that opens a file named "/tmp/test.go", reads a
max of 1024 bytes from the file, converts the byte-stream to a string, and then
displays that string. Note that `os.Read()` takes a byte slice as a param and
this interface determines the max bytes to be read as `len(byte slice)`. It also
shows the usage of `errors` package to help define our own errors.

```go
package main

import (
    "errors"
    "fmt"
    "os"
)

var (
    ErrFileNotFound = errors.New("File not found")
    ErrReadingFile  = errors.New("Error reading from file")
)

func readFile(fname string) (err error) {
    f, err := os.Open(fname)
    if err != nil {
        err = ErrFileNotFound
        return err
    }

    defer f.Close()

    b := make([]byte, 1024)
    n, err := f.Read(b)
    if err != nil {
        err = ErrReadingFile
        return err
    }

    asString := string(b)
    fmt.Printf("Bytes read = %d, Contents\n%s", n, asString)

    return err
}

func main() {
    switch err := readFile("/tmp/test.go"); err {
    case ErrFileNotFound:
        fmt.Println("File not found")
    case ErrReadingFile:
        fmt.Println("Error reading from file")
    case nil:
        fmt.Println("Success")
    default:
        fmt.Println(err)
    }
}
```

# Maps

Go supports `map` data structure which is like an associative array made up of
"<key>, <value>" pairs. Entries can be inserted into a `map` like an `array` and
the `delete` function deletes entries from a map.
```
func main() {
    daysInMonths := make(map[string]int)
    daysInMonths["Jan"] = 31
    daysInMonths["Feb"] = 28
    daysInMonths["Mar"] = 31
    // Fill for the remaining months in the year

    for m, d := range daysInMonths {
        fmt.Printf("Month[%s] has %d days\n", m, d)
    }
}
```

Note that the order of retrieval of entries isn't same as how they were inserted. When run,
entries were displayed in the following order:
```
Month[Mar] has 31 days
Month[Jan] has 31 days
Month[Feb] has 28 days
```

To delete an entry from the above map, say the month of "Feb", use
`delete(daysInMonths, "Feb")`.

To check if an entry exists in the above map, say the month of "Mar":
```
    _, ok := daysInMonths["Mar"]   // Ignore the value by assigning it to _
    if !ok {
        fmt.Println("Month Mar doesn't exist in daysInMonths")
    }
```

# Operators

One of the operators where Go differs from C/C++ is the `bitwise complement
(bitwise not)` unary operator; in Go, the unary operator is `^`, whereas in
C/C++, it is `~`. Go's `binary xor` operator is `^`, which is same as that of
C/C++. Go operates an `unary ^` operator on a value as equivalent to `0xFF... ^
value` and the type of `0xFF...` (number of ones on the left-hand side) is
chosen based on the type of value.

Go has a special operator to clear the specified bits in a value and this is `&^
(bitwise clear)`; `value1 &^ value2` is equivalent to `value1 & (^value2)`. The
truth table for `&^` is as below:
| Bit in Value1 | Bit in Value2 | Resultant Bit with `&^` |
|:-------------:|:-------------:|:-----------------------:|
| 0             | 0             | 0                       |
| 0             | 1             | 0                       |
| 1             | 0             | 1                       |
| 1             | 1             | 0                       |

## Result of a binary arithmetic operation when both operands are untyped

Except bitwise shift operations, the result of a binary arithmetic operation is
still an untyped value if both of the two operands are untyped. The default type
of the result value is one of the two default types and it is the one appears
latter in this list: `int`, `rune`, `float64`, `complex128`. _For example, if
the default type of one untyped operand is int, and the other one is rune, then
the default type of the result untyped value is rune_.

# defer statement

A defer statement defers the execution of a function until the surrounding
function returns.

The deferred call's arguments are evaluated immediately, but the function call
is not executed until the surrounding function returns.

Deferred function calls are pushed onto a stack. When a function returns, its
deferred calls are executed in last-in-first-out order. For instance, in the
sample program below the prints will be A, B, followed by C.
```go
func main() {
    defer fmt.Println("Statement C")
    defer fmt.Println("Statement B")

    fmt.Println("Statement A")
}
```

# Methods and Interfaces

The declaration below, in which the `Celsius parameter c` appears before the
function name, associates with the `Celsius` type a _method named String()_ that
returns `c’s` numeric value followed by °C:
```go
func (c Celsius) String() string { return fmt.Sprintf("%g°C", c) }
```

Many types declare a `String` method of this form because it controls how values
of the type appear when printed as a string by the `fmt` package.
```go
type Celsius float64
var c Celsius = 100.1;

fmt.Println(c.String())         // explicitly call the String() method
fmt.Printf("%v\n", c)           // implicitly calls c.String() that returns a string
fmt.Printf("%s\n", c)           // implicitly calls c.String() that returns a string
fmt.Println(c)                  // implicitly calls c.String() that returns a string
fmt.Printf("%g\n", c)           // does not call the String() method
fmt.Println(float64(c))         // does not call the String() method
```

# Goroutines

Go language provides built-in concurrent programming support in the form of
`goroutines` and `channels`.

A sample program introducing the notion of goroutines is given below:
```go
package main

import (
    "fmt"
)

func emit(c chan string) {
    defer close(c) // try the program by commenting out this line

    // try the below under an infinite loop to continously keep sending data
    words := []string{"One", "Two", "Three", "Four"}
    for _, w := range words {
        c <- w
    }
}

func main() {
    channel := make(chan string)

    go emit(channel)

    for w := range channel {
        fmt.Printf("%s ", w)
    }
    fmt.Println()

    // Now check if channel is still emitting some entries
    w, ok := <-channel
    fmt.Println(w, ok) // It should display an empty string, followed by false

    // Now spawn the emit routines multiple times and observe what happens
    channel = make(chan string) // No concept of reopen; so create another one
    for i := 0; i < 100; i++ {
        go emit(channel)
    }

    for w := range channel {
        fmt.Printf("%s ", w)
    }
    fmt.Println()

    /*
     The above loop may print the words multiple times and in different
     order. This is because the same channel is being used by multiple emit
     goroutines to send data to us.

     It may also result in a panic as an emit goroutine may still be attempting
     to send data while another one has closed the channel.

     In the shell prompt, run this go program in a loop and see varying set of
     behavior from invocation to invocation.
    */
}

```
# Packages

## Exporting and Importing Symbols

A name is exported if it starts with a capital letter. For instance, `math`
package exports the symbol `Pi`. Similarly when importing a package, you can
refer only its exported names, which means, only those symbols that start with a
capital letter.

## Compilation error with unused packages

Go automatically flags an error during compilation if packages are declared but
unused.

# Modules

# Toolchain

## go build

## go doc

## go fmt

Format the Go program to use a consistent coding style.

## go get

## go help

## go install

## go mod

### go mod init

### go mod tidy

## go run

## go test

## go vet

# Programming Style

Stylistically, Go programmers use "camel case" when forming names by combining
words; that is, _interior capital letters are preferred over interior
underscores_.

The letters of acronyms and initialisms like ASCII and HTML are always rendered
in the same case, so a function might be called _htmlEscape_, _HTMLEscape_, or
_escapeHTML_, but not ~~escapeHtml~~.

# Programming in emacs

[melpa](https://www.emacswiki.org/emacs/MELPA) repo has a package
[go-mode.el](https://github.com/dominikh/go-mode.el) for programming in
golang. [eglot](https://github.com/joaotavora/eglot/) and
[lsp-mode](https://emacs-lsp.github.io/lsp-mode/) are
[LSP](https://github.com/Microsoft/language-server-protocol/ clients for
emacs. These lsp clients are also available in [melpa](https://www.emacswiki.org/emacs/MELPA)
Sample setup below with eglot:
``` elisp
(use-package go-mode
  :config
  (add-hook 'go-mode-hook (lambda ()
                            (local-set-key (kbd "C-c C-r")
                                           'go-remove-unused-imports)
                            (eglot-ensure)))
  (add-hook 'before-save-hook 'gofmt-before-save))
```
