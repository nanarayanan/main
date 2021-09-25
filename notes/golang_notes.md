Notes on Golang from various sources on the web and from books.

# References

1. [The Go Programming Language by Alan Donovan and Brian Kernighan
   book](https://learning.oreilly.com/library/view/the-go-programming/9780134190570/)

2. [The book titled "Learning Go" by Jon
   Bodner](https://learning.oreilly.com/library/view/learning-go/9781492077206/)

3. https://learning.oreilly.com/videos/learning-path-go/9781491958100/

4. Docs/Info in go.dev

   1. https://go.dev/ref/spec
   
   2. https://go.dev/doc
   
      1. https://go.dev/doc/code
      
      2. https://go.dev/doc/effective_go
      
   3. https://go.dev/tour/

   4. https://go.dev/src
   
   5. https://go.dev/pkg

5. Docs in github.com/golang

   1. https://github.com/golang/go/issues
   
   2. https://github.com/golang/go/wiki

6. https://research.swtch.com/
   
7. https://groups.google.com/g/golang-nuts

8. https://www.youtube.com/watch?v=f6kdp27TYZs (Rob Pike on Concurrency)

9. https://go101.org/

10. https://github.com/avelino/awesome-go

11. https://gobyexample.com/

# Introduction

Developed by Robert Griesemer, Rob Pike, and Ken Thompson of Google and with
some concepts leveraged from multiple programming languages like Algol, Pascal,
Modula, Oberon, C, CSP, Squeak, Newsqueak, Alef, etc.

From C, Go inherited its expression syntax, control-flow statements, basic data
types, call-by-value parameter passing, pointers, and above all, C's emphasis on
programs that compile to efficient machine code and cooperate naturally with the
abstractions of current operating systems.

Go has comparatively few features. For instance, it has no implicit numeric
conversions, no constructors or destructors, no operator overloading, no default
parameter values, no inheritance, no generics, no exceptions, no macros, no
function annotations, and no thread-local storage.

# Usage of semicolon

Go does not require semicolons at the end of statements or declarations, except
where two or more appear on the same line. In effect, newlines following certain
tokens are converted into semicolons, so where newlines are placed matters to
proper parsing of Go code. For instance, the opening brace `{` of the function
must be on the same line as the end of the `func` declaration, not on a line by
itself, and in the expression `x+y`, a newline is permitted after but not before
the `+` operator.

# Expressions and Statements

The increment statement `i++` adds 1 to i; it is equivalent to `i += 1` which is
in turn equivalent to `i = i+1`. There is a corresponding decrement statement
`i--` that subtracts 1. These are statements, and not expressions as they are in
languages like `C`, so `j = i++` is not valid in Go. In Go, these statements are
postfix only and so `++i` or `--i` are also illegal.

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

## for statement

```go
for initialization; condition; post {
    // zero or more statements
}
```

The _condition_ is a boolean expression that is evaluated at the beginning of
each iteration of the loop; if it evaluates to true, the statements controlled
by the loop are executed. The post statement is executed after the body of the
loop, then the condition is evaluated again. The loop ends when the condition
becomes false.

## C's while loop

The _initialization_ and _post_ can be omitted and in which case the semicolons
can be omitted too. This is same as C's `while` loop.
```go
for condition {
    // zero or more statements
}
```

## forever loop

To accomplish a traditional infinite loop:
```go
for {
    // zero or more statements
}
```

## Iterate over a range

To iterate over a range of values from a data type like a string or a slice: in
each iteration of the loop, range produces a pair of values---the index and the
value of the element at that index.
```go
for _, arg := range os.Args[1:] {
    // zero or more statements
}
```

## Labeling statements to help break/continue refer to them

The `break` and `continue` statements modify the flow of contro . A `break`
causes control to resume at the next statement after the innermost `for`,
`switch`, or `select` statement and a `continue` causes the innermost `for` loop
to start its next iteration.

Statements may be labeled so that `break` and `continue` can refer to them, for
instance to break out of several nested loops at once or to start the next
iteration of the outermost loop.

```go
label_1:
   for {
       for {
           break label_1    // This breaks out of the outer for-loop
           // Without label_1, it would break only out of the inner for-loop
       }
   }
```

```go
outer:
    for _, outerVal := range outerValues {
        for _, innerVal := range outerVal {
            // process innerVal
            if invalidSituation(innerVal) {
                continue outer
            }
        }
        // here we have code that runs only when all of the
        // innerVal values were sucessfully processed
    }
```

## switch

Given below is a snippet with a _blank switch value_, meaning one that doesn't
switch on a value; instead, it allows you to use any boolean comparison for each
`case`.

```go
words := []string{"hi", "salutations", "hello"}
for _, word := range words {
    switch wordLen := len(word); {
    case wordLen < 5:
        fmt.Println(word, "is a short word!")
    case wordLen > 10:
        fmt.Println(word, "is a long word!")
    default:
        fmt.Println(word, "is exactly the right length.")
    }
}

Output below:
~~~~~~~~~~~~
hi is a short word!
salutations is a long word!
hello is exactly the right length.
```

Favor `blank switch` statements over `if/else` chains when you have multiple
related `cases`. Using a switch makes the comparisons more visible and
reinforces that they are a related set of concerns.

Of course, there is nothing in Go that prevents you from doing all sorts of
unrelated comparisons on each `case` in a `blank switch`. However, this is not
idiomatic. If you find yourself in a situation where you want to do this, use a
series of `if/else` statements (or perhaps consider refactoring your code).

## goto statement

Go supports `goto` but avoid it if you can. A `goto` statement specifies a
labeled line of code and execution jumps to it. However, you can’t jump
anywhere. Go forbids jumps that skip over variable declarations and jumps that
go into an inner or parallel block.

Code snippet below won't compile.

```go
package main

import "fmt"

func main() {
    a := 10
    goto skip
    b := 20
skip:
    c := 30
    fmt.Println(a, b, c)
    if c > a {
        goto inner
    }
    if a < b {
    inner:
        fmt.Println("a is less than b")
    }
}
```

Compilation fails:

```go
./test.go:7:7: goto skip jumps over declaration of b at ./test.go:8:4
./test.go:13:8: goto inner jumps into block starting at ./test.go:15:11
```

You should try very hard to avoid using `goto`. But in the rare situations where
it makes your code more readable, it is an option. Below is a contrived example
where a `goto` can be clearer than other alternatives.

```go
func main() {
    a := rand.Intn(10)
    for a < 100 {
        if a%5 == 0 {
            goto done
        }
        a = a*2 + 1
    }
    fmt.Println("do something when the loop completes normally")
done:
    fmt.Println("do complicated stuff no matter why we left the loop")
    fmt.Println(a)
}
```

# Keywords

Go has 25 keywords:
```go
break         default         func         interface         select
case          defer           go           map               struct
chan          else            goto         package           switch
const         fallthrough     if           range             type
continue      for             import       return            var
```

# Pre-declared names

The following names are not reserved and hence may be used in declarations;
however, it is recommended that we don't use them as it would confuse a reader.

Constants
```go
true    false    iota    nil
```

Types
```go
int      int8      int16      int32        int64
uint     uint8     uint16     uint32       uint64    uintptr
float32  float64   complex64  complex128
bool     byte      rune       string       error
```

Functions
```go
make      len        cap    new    append    copy    close    delete
complex   real       imag
panic     recover
```

# Scope of Entities

The _scope_ of a declaration is the part of the source code where a use of the
declared name refers to that declaration. The scope of a variable is a region of
the program text; it is a compile-time property.

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

## Blocks

A _syntactic block_ is a sequence of statements enclosed in braces like those
that surround the body of a function or loop. A name declared inside a syntactic
block is not visible outside that block. The block encloses its declarations and
determines their scope. We can generalize this notion of blocks to include other
groupings of declarations that are not explicitly surrounded by braces in the
source code; we refer to them as _lexical blocks_. There is a lexical block for
the entire source code, called the _universe block_; for _each package_; for
_each file_; for _each for_, _if_, and _switch statement_; for _each case_ in a
_switch_ or _select statement_; and, of course, for each explicit syntactic
block.

### Universal Block

Go is a small language with only 25 keywords. What’s interesting is that the
built-in types (like `int` and `string`), constants (like `true` and `false`),
and functions (like `make` or `close`) aren’t included in that list. Neither is
`nil`.

Rather than make them keywords, Go considers these `predeclared identifiers` and
defines them in the `universe block`, which is the block that contains all other
blocks.

Because these names are declared in the universe block, it means that they can
be shadowed in other scopes. You must be very careful to never redefine any of
the identifiers in the universe block.

## Scopes

The _scope of a control-flow label_, as used by _break_, _continue_, and _goto_
statements, is the _entire enclosing function_.

If an entity is declared within a function, it is local to that function. If
declared outside of a function, however, it is visible in all files of the
package to which it belongs. _The case of the first letter of a name determines
its visibility across package boundaries_. If the name begins with an upper-case
letter, it is exported, which means that it is visible and accessible outside of
its own package and may be referred to by other parts of the program, as with
`Printf` in the fmt package. Package names themselves are always in lower case.

Consider the following Go code snippet:
```go
x = "hello world\n"
for i := 1; i < 10; i++ {       // "for" Scope start: an implicit scope
    x := x[i] + 1               // Another scope start: an explicit scope
}                               // "for" Scope end
```
A `for` loop starts an implicit scope and the var `i` declared is visible to the
_for condition_, _post increment_ and to the enclosed _for body_. Inside the
_for body_, in the expression `x[i] + 1`, _x_ is from the outer scope associated
with the string "hello world\n" and `i` is from the _for's_ implicit
scope. Inside the _for body_, we are declaring _another x_ and so it will start
masking the _outer scope's x_ till the `for` loop ends. Outside the `for` loop,
`i` is not visible and the _outer scope's x_ will get unmasked.

Like `for` loops, `if` statements and `switch` statements also create implicit
blocks in addition to their body blocks.

## if statement --- Implicit and Explict scopes

```go
if x := f(); x == 0 {           // "if" starts an implicit scope
    fmt.Println(x)              // an explicit scope between "{" and "}"
} else if y := g(x); x == y {   // starts another implicit scope;
                                //    "x" is visible from the previous "if"'s
                                //    implicit scope
    fmt.Println(x, y)           // another explicit scope between "{" and "}"
} else {
    fmt.Println(x, y)           // another explicit scope between "{" and "}"
}
fmt.Println(x, y)   // compile error: x and y are not visible here
```

## variable declaration overriding outer scope

In the below code snippet, though the intenton is to just declare _err_ as a new
variable and to just assign a value to the outer scope's _cwd_ variable, the _variable_
declaration `cwd, err := os.Getwd()` would actually result in a new var _cwd_
getting declared; this declaration ends up masking the original _cwd_.
```go
var cwd string

func init() {
    cwd, err := os.Getwd()  // compile error: unused: cwd
    if err != nil {
        log.Fatalf("os.Getwd failed: %v", err)
    }
}
```
In the above snippet, we would be come to know about thanks to the compilation
failure indicating the inner _cwd_ though declared is unused. However, we would
have missed to notice this masking if we had written the augmented the code
snippet as below to log the value of _cwd_.
```go
var cwd string

func init() {
    cwd, err := os.Getwd()  // NOTE: we are declaring a new "cwd" here
    if err != nil {
        log.Fatalf("os.Getwd failed: %v", err)
    }
    log.Printf("Working directory = %s", cwd)   // logs the newly declared "cwd"
}
```
One way to workaround this problem is to not use _a single short var_ declaration and
instead assign to _cwd_ separately and declare _err_ separately as shown below:
```go
var cwd string

func init() {
    var err error           // declare only "err" here
    cwd, err = os.Getwd()   // no longer a declaration and just an assignment
    if err != nil {
        log.Fatalf("os.Getwd failed: %v", err)
    }
}
```

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

_In practice, you should generally use one of the first two forms, with explicit
initialization to say that the initial value is important and implicit
initialization to say that the initial value doesn't matter._

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

Constants in Go are a way to give names to literals. There is no way
in Go to declare that a variable is immutable. Constants can be
character, string, boolean, or numeric literals.

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

## Untyped Constants

`Constants` in Go are a bit unusual. Although a `constant` can have any of the
basic data types like `int` or `float64`, many constants are not committed to
any particular type. The compiler represents these uncommitted constants with
much greater numeric precision than values of basic types, and arithmetic on
them is more precise than machine arithmetic; _you may assume at least 256 bits
of precision_. There are six flavors of these uncommitted constants, called
`untyped boolean`, `untyped integer`, `untyped rune`, `untyped floating-point`,
`untyped complex`, and `untyped string`.

By deferring this commitment, untyped constants not only retain their higher
precision until later, but they can participate in many more expressions than
committed constants without requiring conversions.

```go
const (
    _ = 1 << (10 * ioata)
    KiB     // 1 << 10
    MiB     // 1 << 20
    GiB     // 1 << 30
    TiB     // 1 << 40      (exceeds 1 << 32)
    PiB     // 1 << 50
    EiB     // 1 << 60
    ZiB     // 1 << 70      (exceeds 1 << 64)
    YiB     // 1 << 80
)

fmt.Println(YiB/ZiB)    // 1024 (though YiB and ZiB are too big, the division works)
```

The floating-point constant `math.Pi` may be used wherever any floating-point or
complex value is needed.

```go
var x float32 = math.Pi
var y float64 = math.Pi
var z complex128 = math.Pi
```

If `math.Pi` had been committed to a specific type such as `float64`, the result
would not be as precise, and type conversions would be required to use it when a
`float32` or `complex128` value is wanted:

```go
const Pi64 float64 = math.Pi

var x float32 = float32(Pi64)       // Note the need for a type conversion
var y float64 = Pi64
var z complex128 = complex128(Pi64) // Note the need for a type conversion
```

For literals, syntax determines flavor. The literals `0`, `0.0`, `0i`, and
`'\u0000'` all denote constants of the same value but different flavors:
`untyped integer`, `untyped floating-point`, `untyped complex`, and `untyped
rune`, respectively. Similarly, `true` and `false` are `untyped booleans` and
string literals are `untyped strings`.

Only constants can be untyped. When an untyped constant is assigned to a
variable, as in the first statement below, or appears on the right-hand side of
a variable declaration with an explicit type, as in the other three statements,
the constant is implicitly converted to the type of that variable if possible.

```go
var f float64 = 3 + 0i  // untyped complex -> float64
f = 2                   // untyped integer -> float64
f = 1                   // untyped floating-point -> float64
f = 'a'                 // untyped rune -> float64
```

### An untyped const value can overflow its default type

Whether implicit or explicit, converting a constant from one type to another
requires that the target type can represent the original value. Rounding is
allowed for real and complex floating-point numbers.

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

The autocomplete feature plus the `iota` _constant generator_ feature is a very
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
program executes. The lifetime of a variable is the range of time during
execution when the variable can be referred to by other parts of the program; it
is a run-time property.

The lifetime of a package-level variable is the entire execution of the program.

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

# Go's Types

1. Basic types

2. Aggregate types

3. Reference types

   * Includes pointers, maps, slices, functions and channels.

   * What they have in common is that they all refer to program variables or
     state _indirectly_, so that the effect of an operation applied to one
     reference is observed by all copies of that reference.

4. Interface types

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

Regardless of their size, `int`, `uint`, and `uintptr` are different types from
their explicitly sized siblings. Thus `int` is not the same type as `int32`,
even if the natural size of integers is 32 bits, and an explicit conversion is
required to use an _int_ value where an _int32_ is needed, and vice versa.

Go doesn’t allow automatic type promotion between variables. You must use a type
conversion when variable types do not match. Even different-sized integers and
floats must be converted to the same type to interact.

Go’s binary operators for arithmetic, logic, and comparison are listed here in order of decreas-
ing precedence:
```go
*       /       %       <<      >>      &       &^
+       -       |       ^
==      !=      <       <=      >       >=
&&
||
```

There are only five levels of precedence for binary operators. Operators at the
same level associate to the left, so parentheses may be required for clarity, or
to make the operators evaluate in the intended order in an expression like `mask
& (1 << 28)`.

The behavior of `%` for negative numbers varies across programming languages. In
Go, _the sign of the remainder is always the same as the sign of the dividend_,
so `-5 % 3` and `-5 % -3` are `both -2`.

_xor_ gives the _symmetric difference_ and _&^_ gives the _difference_ if we
consider the bits as a Set.

## Non-zero value doesn't mean it is true

Since all type conversions in Go are explicit, you cannot treat another Go type
as a boolean. In many languages, a non-zero number or a nonempty string can be
interpreted as a boolean `true`.

## Special names

Go does have some special names for integer types. A `byte` is an alias for
`uint8`; it is legal to assign, compare, or perform mathematical operations
between a `byte` and a `uint8`. However, _you rarely see uint8_ used in Go code;
_just call it a byte_.

The second special name is `int`. On _a 32-bit CPU, int is a 32-bit signed
integer like an int32_. On _most 64-bit CPUs, int is a 64-bit signed integer,
just like an int64_. Because `int` isn’t consistent from platform to platform,
it is a _compile-time error to assign, compare, or perform mathematical
operations between an int and an int32 or int64 without a type conversion_.

The third special name is `uint`. It follows the same rules as `int`, only it is
unsigned (the values are always 0 or positive).

There are two other special names for integer types, rune and uintptr.

## Usage of signed int vs uint

Although Go provides unsigned numbers and arithmetic, we tend to use the signed
int form even for quantities that can't be negative, such as the length of an
array. This will prove beneficial for instance, when we loop over a quantity,
and using a _signed int_ as the _index_ will help terminate the loop correctly.
```go
medals := []string{"gold", "silver", "bronze"}
for i := len(medals) - 1; i >= 0; i-- {
    fmt.Println(medals[i]) // "bronze", "silver", "gold"
}
```
If `i` were to be _unsigned_, the loop won't terminate as `uint(0 - 1)` is _not
-1_, but _a very large quantity with the value (2^64 - 1) or (2^32 - 1)
depending on the implementation_. That's why functions like `len()` return a
_signed value_.

For this reason, unsigned numbers tend to be used only when their bitwise
operators or peculiar arithmetic operators are required, as when implementing
bit sets, parsing binary file formats, or for hashing and cryptography. They are
_typically not used for merely non-negative quantities_.

## What "int" type to use

Unless you need to be explicit about the size or sign of an integer for
performance or integration purposes, use the `int` type. Consider any other type
to be a premature optimization until proven otherwise.

## Floating Point Numbers

Just like other languages, Go floating point numbers have a huge range, but they
cannot store every value in that range; they store the nearest
approximation. Because floats aren’t exact, they can only be used in situations
where inexact values are acceptable or the rules of floating point are well
understood. That limits them to things like graphics and scientific operations.

A floating point number cannot represent a decimal value exactly. Do not use
them to represent money or any other value that must have an exact decimal
representation!

Very small or very large numbers are better written in scientific notation, with
the letter `e` or `E` preceding the decimal exponent:

```go
const Avogadro = 6.02214129e23
const Planck = 6.62606957e-34
```

Go (and most other programming languages) stores floating point numbers using a
specification called `IEEE 754`. For example, if you store the number `-3.1415`
in a `float64`, the 64-bit representation in memory looks like:
`1100000000001001001000011100101011000000100000110001001001101111` which is
exactly equal to `-3.14150000000000018118839761883`. Out of the 64 bits above,
one is used to represent the sign (positive or negative), 11 bits are used to
represent a base two exponent, and 52 bits are used to represent the number in a
normalized format (called the `mantissa`).

`float64` should be preferred for most purposes because `float32` computations
accumulate error rapidly.

Floating-point values are conveniently printed with `Printf’s %g verb`, which
chooses the most compact representation that has adequate precision, but for
tables of data, the `%e (exponent)` or `%f (no exponent)` forms may be more
appropriate. All three verbs allow _field width_ and _numeric precision_ to be
controlled, for instance, by specifying something like `%8.3f`.

In addition to a large collection of the usual mathematical functions, the
`math` package has functions for creating and detecting the special values
defined by _IEEE 754_: the _positive_ and _negative_ `infinities`, which
represent numbers of excessive magnitude and the result of division by zero; and
_NaN_ ("not a number"), the result of such mathematically dubious operations as
`0/0` or `Sqrt(-1)`.

While Go lets you use `==` and `!=` to compare floats, don’t do it. Due to the
inexact nature of floats, two floating point values might not be equal when you
think they should be. Instead, define a maximum allowed variance and see if the
difference between two floats is less than that. This value (sometimes called
`epsilon`) depends on what your accuracy needs are.

## Complex Numbers

Go provides two sizes of complex numbers, `complex64` and `complex128`, whose
components are `float32` and `float64` respectively. The built-in function
`complex` creates a complex number from its `real` and `imaginary` components,
and the built-in `real` and `imag` functions extract those components:

```go
var x complex128 = complex(1, 2)    // 1+2i
var y complex128 = complex(3, 4)    // 3+4i
fmt.Println(x*y)                    // "(-5+10i)"
fmt.Println(real(x*y))              // "-5"
fmt.Println(imag(x*y))              // "10"
```

The `math/cmplx` package provides library functions for working with _complex_
numbers, such as the _complex_ _square root_ and _exponentiation_ functions.

## Booleans

A value of type `bool`, or _boolean_, has only two possible values, `true` and
`false`. The conditions in `if` and `for` statements are booleans, and
comparison operators like `==` and `<` produce a boolean result. The unary
operator `!` is _logical negation_, so `!true is false`.

There is no implicit conversion from a boolean value to a numeric value like `0`
or `1`, or vice versa.

## Strings

A `string` is an immutable sequence of bytes. Strings may contain arbitrary
data, including bytes with value 0. Text strings are conventionally interpreted
as UTF-8-encoded sequences of Unicode code points (`runes`).

The built-in `len` function returns the number of bytes (`not runes`) in a
string, and the _index operation_ `s[i]` retrieves the "i-th byte of string s",
where `0 ≤ i < len(s)`. Attempting to access a byte outside this range results
in a panic. The i-th byte of a string is not necessarily the i-th character of a
string, because the UTF-8 encoding of a non-ASCII code point requires two or
more bytes.

The _substring_ operation `s[i:j]` yields a new string consisting of the bytes
of the original string starting at `index i` _and continuing up to, but not
including, the byte at_ `index j`. The result contains `j-i bytes`. Again, a
panic results if either index is out of bounds or if `j` is less than `i`.

The `+` operator makes a new string by concatenating two strings.

Immutability means that it is safe for two copies of a string to share the same
underlying memory, making it cheap to copy strings of any length. Similarly, a
string `s` and a substring like `s[7:]` may safely share the same data, so the
substring operation is also cheap. No new memory is allocated in either case.

### Packages relevant to strings

Four standard packages are particularly important for manipulating strings:
`bytes`, `strings`, `strconv`, and `unicode`.

The `strings` package provides many functions for searching, replacing,
comparing, trimming, splitting, and joining strings.

The `bytes` package has similar functions for manipulating _slices of bytes_, of
type `[]byte`, which share some properties with `strings`. Because strings are
immutable, building up strings incrementally can involve a lot of allocation and
copying. In such cases, it's more efficient to use the `bytes.Buffer` type.

The `strconv` package provides functions for converting `boolean`, `integer`,
and `floating-point` values to and from their string representations, and
functions for quoting and unquoting strings.

The `unicode` package provides functions like `IsDigit`, `IsLetter`, `IsUpper`,
and `IsLower` for classifying runes. Each function takes a single `rune`
argument and returns a `boolean`. Conversion functions like `ToUpper` and
`ToLower` convert a rune into the given case if it is a letter. The `strings`
package has similar functions, also called `ToUpper` and `ToLower`, that return
a new string with the specified transformation _applied to each character of the
original string_.

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
    v := Vertex{100, 200}            // Order relevant; X=100 and Y=200
    v = Vertex{Y: 200, X: 100}       // Order irrelevant due to eplicitly naming
    fmt.Println(v)
}
```

If we want to initialize only a subset of the fields in a struct and leave the
rest to their zero values, we can choose to use the initialization format
`{FieldName: Value}` that requires the fields to be named. In the other format
where only the values are specified, even if the fields to be explicitly
initialized are contiguous and all grouped at the beginning of the struct, Go
expects _all_ the values to be specified. This helps in scenarios where the
struct undergoes some changes in the future and the implementation forgets to
handle it.

## Anonymous Struct

```go
var person struct {
    name    string
    address string
}

dog := struct {
    breed string
}{
    "Shi Tzu"
}
```

## Are structs comparable?

Whether or not a struct is comparable depends on the struct’s fields. Structs
that are entirely composed of comparable types are comparable; those with slice,
map, function and channel fields prevent a struct from being comparable.

Just like Go doesn’t allow comparisons between variables of different primitive
types, Go doesn’t allow comparisons between variables that represent structs of
different types. Go does allow you to perform a type conversion from one struct
type to another if the fields of both structs have the same names, order, and
types.

For instance, in the snippet below, the structs `firstPerson` and `fourthPerson`
aren't comparable and hence can't be typecast to each other because the field
names don't match.

```go
type firstPerson struct {
    name string
    age  int
}

type fourthPerson struct {
    firstName string
    age       int
}
```

## No need for Getter and Setter Methods

Do not write getter and setter methods for Go structs, unless you need them to
meet an interface. Go encourages you to directly access a field. Reserve methods
for business logic. The exceptions are when you need to update multiple fields
as a single operation or when the update isn’t a straightforward assignment of a
new value.

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

Though literals in Go are _untyped_, it goes only so far; you can't assign a
literal string to a variable with a numeric type or a literal number to a string
variable, nor can you assign a float literal to an int. These are all flagged by
the compiler as errors.

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

Note that a `range loop` over a string iterates over the indices in terms of
runes and not in terms of bytes. Note also that displaying a `string` or a
`[]rune` in hex displays the whole content and a `for` loop isn't required.

```go
s := "Hello, 世界"
n := 0
for range "Hello, 世界" {
    n++
}
// 13 bytes and 9 runes
fmt.Println(len(s), n)                  // 13  9
fmt.Println(utf8.RuneCountInString(s))  // 9

fmt.Printf("% x\n", s)                  // 48 65 6c 6c 6f 2c 20 e4 b8 96 e7 95 8c
fmt.Printf("%x\n", []rune(s))           // [48 65 6c 6c 6f 2c 20 4e16 754c]
```

# Functions

## Functions with Named Return Values

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

 The named return parameters give a way to declare an _intent_ to use variables
 to hold the return values, but don’t require you to use them.

If you only want to name _some_ of the return values, you can do so by using `_`
as the name for any return values you want to remain nameless.

Though a function with _named return values_ let you use a blank return, this
makes the program hard to understand. If your function returns values, never use
a blank return. It can make it very confusing to figure out what value is
actually returned.

## Anonymous functions

Not only can you assign functions to variables, you can also define new
functions within a function and assign them to variables.

These inner functions are anonymous functions; they don’t have a name. You don’t
have to assign them to a variable, either. You can write them inline and call
them immediately.

```go
func main() {
    for i := 0; i < 5; i++ {
        func(j int) {
            fmt.Println("printing", j, "from inside of an anonymous function")
        }(i)    // "i" is passed as a param to the anonymous function
    }
}
```

Just like any other function, an anonymous function is called by using
parenthesis. The above is not an idiomatic example for using anonymous
functions. There are two situations where declaring anonymous functions without
assigning them to variables is useful: `defer` statements and launching
`goroutines`.

## Closures

Functions declared inside of functions are special; they are `closures`. This is
a computer science word that means that functions declared inside of functions
are able to access and modify variables declared in the outer function.

Closures really become interesting when they are passed to other functions or
returned from a function. They allow you to take the variables within your
function and use those values _outside_ of your function.

## Passing Functions as Parameters

Since functions are values and you can specify the type of a function using its
parameter and return types, you can pass functions as parameters into
functions. This mechanism of creating a closure that references local variables
and then passing that closure to another function is a very useful pattern and
appears several times in the standard library.

```go
type Person struct {
    FirstName string
    LastName  string
    Age       int
}

people := []Person{
    {"Pat", "Patterson", 37},
    {"Tracy", "Bobbert", 23},
    {"Fred", "Fredson", 18},
}
fmt.Println(people)
```

Next, we’ll sort our slice by last name and print out the results:

```go
// sort by last name
sort.Slice(people, func(i int, j int) bool {
    return people[i].LastName < people[j].LastName
})
fmt.Println(people)
```

The closure that’s passed to `sort.Slice` has two parameters, `i` and `j`, but
within the closure, we can refer to `people` so we can sort it by the `LastName`
field. In computer science terms, `people` is captured by the _closure_.

Next, we'll sort our slice by age and print out the results:

```go
// sort by age
sort.Slice(people, func(i int, j int) bool {
    return people[i].Age < people[j].Age
})
fmt.Println(people)
```

Running the above snippets gives the following output:

```go
[{Pat Patterson 37} {Tracy Bobbert 23} {Fred Fredson 18}]
[{Tracy Bobbert 23} {Fred Fredson 18} {Pat Patterson 37}]
[{Fred Fredson 18} {Tracy Bobbert 23} {Pat Patterson 37}]
```

## Returning Functions as Parameters

Not only can you use a closure to pass some function state to another function,
you can also return a closure from a function.

```go
func makeMult(base int) func(int) int {
    return func(factor int) int {
        return base * factor
    }
}

func main() {
    twoBase := makeMult(2)
    threeBase := makeMult(3)
    for i := 0; i < 3; i++ {
        fmt.Println(twoBase(i), threeBase(i))
    }
}

Output:
~~~~~~
0 0
2 3
4 6
```
If you spend any time with programmers who use functional programming languages
like `Haskell`, you might hear the term **higher-order functions**. That’s a very
fancy way to say that **a function has a function for an input parameter or a
return value**.

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

It's not just pointers that create aliases; aliasing also occurs when we copy
values of other reference types like slices, maps, and channels, and even
structs, arrays, and interfaces that contain these types.

## Addresses of Constants

Not being able to take the address of a constant is sometimes inconvenient. If
you have a struct with a field of a pointer to a primitive type, you can’t
assign a literal directly to the field. The following program won't compile.

```go
type person struct {
    FirstName  string
    MiddleName *string
    LastName   string
}

p := person{
  FirstName:  "Pat",
  MiddleName: "Perry", // This line won't compile
  LastName:   "Peterson",
}
```

To handle the above, one option is to:

```go
func stringp(s string) *string {
    return &s
}

p := person{
  FirstName:  "Pat",
  MiddleName: stringp("Perry"), // This works
  LastName:   "Peterson",
}
```

Why does the above work? When we pass a constant to a function, the constant is
copied to a parameter, which is a variable. Since it’s a variable, it has an
address in memory. The function then returns the variable’s memory address.

## Pointers are a last resort

Rather than populating a struct by passing a pointer to it into a function, have
the function instantiate and return the struct.

**Not a preferred approach**

```go
func MakeFoo(f *Foo) error {
  f.Field1 = "val"
  f.Field2 = 20
  return nil
}
```

**Instead, return a struct from the function**

```go
func MakeFoo() (Foo, error) {
  f := Foo{
    Field1: "val",
    Field2: 20,
  }
  return f, nil
}
```

## Use pointer params when the function expects an interface

The only time you should use pointer parameters to modify a variable is when the
function expects an interface. For instance, You see this pattern when working
with JSON.

```go
f := struct {
  Name string `json:"name"`
  Age int `json:"age"`
}
err := json.Unmarshal([]byte(`{"name": "Bob", "age": 30}`), &f)
```

The `Unmarshal` function populates a variable from a slice of bytes containing
JSON. It is declared to take a slice of bytes and an interface{} parameter. The
value passed in for the interface{} parameter must be a pointer.

This pattern is used because _Go doesn’t have generics_. That means there isn’t
a convenient way to pass a type into a function to specify what to unmarshal
into nor is there a way to specify a different return type for different types.

Because JSON integration is so common, this API is sometimes treated as a common
case by new Go developers, instead of the exception that it should be.

That said, there is a way to represent a type in Go in a variable, by using the
`Type type in the reflect package`. _The reflect package is reserved for
situations where there is no other way to accomplish a task_.

## Returning pointers from a function

When returning values from a function, you should favor value types. Only use a
pointer type as a return type if there is state within the data type that needs
to be modified.

## Pointer passing performance

For the vast majority of cases, the difference between using a pointer and a
value won’t affect your program’s performance. But if you are passing megabytes
of data between functions, consider using a pointer even if the data is meant to
be immutable.

## The Zero Value Versus No Value

Pointers can be used to indicate the difference between a variable or field that
has been assigned the zero value and a variable or field that hasn’t been
assigned a value at all. If this distinction matters in your program, use a
`nil` pointer to represent an unassigned variable or struct field.

# The new function

The expression `new(T)` creates an `unnamed variable` of `type T`, initializes
it to the zero value of `T`, and returns its address, which is a value of type
`*T`. A variable created with `new` is no different from an ordinary local
variable whose address is taken.

p := new(int)       // p, of type *int, points to an unnamed int variable
fmt.Println(*p)     // "0"
*p = 2              // sets the unnamed int to 2
fmt.Println(*p)     // "2"

# Call-by-Value

Go is a call by value language, so the values passed to functions are
copies. For non-pointer types like primitives, structs, and arrays, this means
that the called function cannot modify the original. Since the called function
has a copy of the original data, the immutability of the original data is
guaranteed.

# Arrays

The `type [n]T` is an `array of n values` of `type T`. It is an aggregate data
structure with all of its elements being homogeneous and hence of the same
type. The size of an array is fixed and `len(array)` returns the number `n` of
elements in the array. We can use an _array literal_ to initialize an array with
a list of values as `var q [3]int = [3]int{1, 2, 3}`.

## Passing Arrays as Params to Functions

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
// Modifications in main():

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

With the param type change from an array to a slice, `words[0]` will be printed
as "The" and "Modified in myPrint" respectively in the first and second call to
`myPrint()`.

## Using ... for array length

In an array literal, if an ellipsis "..." appears in place of the length, the
array length is determined by the number of initializers.
```go
q := [...]int{1, 2, 3}
fmt.Printf("%T\n", q)   // "[3]int"
```

## Array size is part of its type

The size of an array is part of its type, so `[3]int` and `[4]int` are different
types. The size must be a constant expression, that is, an expression whose
value can be computed as the program is being compiled.
```go
v := [3]int{1, 2, 3}
v = [4]int{1, 2, 3, 4}  // compile error: cannot assign [4]int to [3]int
```

## Initializing Arrays

Initializing an array using a "list of index and value pairs" and the order
depends on the index values. Indices can be omitted and their values will be
initialized to the zero value of the associated type.
```go
s := [6]string{0: "zero", 1: "one", 3: "three", 2: "two", 5: "five"}    // omitted indices [3] and [4]
fmt.Println(s[2])   // prints "two"
fmt.Println(s[3])   // prints "" empty string
```

`r := [...]int{99: -1}` defines an array `r` with 100 elements, all zero except
for the last, which has value `-1`.

## Comparing Arrays

If an array’s element type is comparable then the array type is comparable too,
so we may directly compare two arrays of that type using the `==` operator,
which reports whether all corresponding elements are equal. The `!=` operator is
its negation.
```go
a := [2]int{1, 2}
b := [...]int{1, 2}
c := [2]int{1, 3}
fmt.Println(a == b, a == c, b == c) // "true false false"
d := [3]int{1, 2}
fmt.Println(a == d)                 // compile error: cannot compare [2]int == [3]int
```

## Pointers to an Array

Pointer to an array of integers vs. Pointer to an array of integer pointers:
```go
var a [5]int;
aPtr := &a;
var b [5]*int;
bPtr := &b;
fmt.Printf("type(a)=%T, type(aPtr)=%T, type(b)=%T, type(bPtr)=%T\n",
           a, aPtr, b, bPtr);

// Output:
type(a)=[5]int, type(aPtr)=*[5]int, type(b)=[5]*int, type(bPtr)=*[5]*int
```

# Slice

An array has a fixed size. A slice, on the other hand, is a dynamically-sized,
flexible view into the elements of an array. In practice, slices are much more
common than arrays. Slices represent variable-length sequences whose elements
are all of the same type.

The `type []T` is a `slice with elements of type T`. A slice looks like an array
type without a size.

A slice is formed by specifying two indices, a low and high bound, separated by
a colon:
`a[low : high]`
This selects a half-open range which includes the first element, but excludes
the last one.

## Slices are not comparable

It is a compile-time error to use `==` to see if two slices are
identical or `!=` to see if they are different. The only thing you can
compare a slice with is nil:

The function `len` for slices returns 0 if you pass a `nil` slice to `len`.

```go
x := []int

fmt.Println(x == nil) // prints true
```

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

## Capacity of a Slice

A `slice` is a sequence of values. Each element in a slice is assigned
to consecutive memory locations, which makes it quick to read or write
these values. Every slice has a capacity, which can be larger than its
length.

Each time you append to a slice, one or more values is added to the
end of the slice. Each value added increases the length by one. When
the length reaches the capacity, there’s no more room to put
values.

## Appending to a Slice

If you try to add additional values when the length equals the
capacity, the `append` function uses the Go runtime to allocate a new
slice with a larger capacity. The values in the original slice are
copied to the new slice, the new values are added to the end, and the
new slice is returned.

## Copy between Slices

The `copy` function allows you to copy between two slices even if they
cover overlapping sections of an underlying slice. `Copy` function
looks at the length, and not the capacity, of the destination and
source and copies min(destLength, srcLength) number of elements.

```go
x := []int{1, 2, 3, 4}
num = copy(x[:3], x[1:])
fmt.Println(x, num)
```

In this case, we are copying the last three values in x on top of the
first three values of x. This prints out `[2 3 4 4] 3`.

You can use `copy` with arrays by taking a slice of the array. You can
make the array either the source or the destination of the copy.

```go
x := []int{1, 2, 3, 4}
d := [4]int{5, 6, 7, 8}
y := make([]int, 2)
copy(y, d[:])
fmt.Println(y)
copy(d[:], x)
fmt.Println(d)
```

Output of the above snippet:

```
[5 6]
[1 2 3 4]
```

## Passing slices to functions

When a `slice` is sent to a function as a param, a copy of `len` and `capacity`
and the `pointer to memory containing the slice's contents` are made. So if
modifications to the existing contents of the slice will be reflected in the
caller; however any change in len or capacity won't be reflected back. If the
function appends additional elements and even if they are well within the
original capacity and the pointer to the contents remains the same, the
additional elements are part of the slice but with a change in len and capacity
not being made known to the caller, the caller will fail to the see the
additional elements. For the scenario where a growth in the slice within a
function results in copy/growth to another location in memory, this definitely
won't get reflected as the change in address isn't seen by the caller.

# Maps

Go supports `map` data structure which is like an associative array
made up of "<key>, <value>" pairs. Entries can be inserted into a
`map` like an `array` and the `delete` function deletes entries from a
map.

```go
func main() {
    daysInMonths := make(map[string]int)
    daysInMonths["Jan"] = 31
    daysInMonths["Feb"] = 28
    daysInMonths["Mar"] = 31 // Fill for the remaining months in the year

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

```go
    _, ok := daysInMonths["Mar"]   // Ignore the value by assigning it to _
    if !ok {
        fmt.Println("Month Mar doesn't exist in daysInMonths")
    }
```

## Using Map to implement Set

Go doesn't support a Set data type natively, however, Maps can be used to
implement Sets. Given below are two sample program snippets to implement a
Set---the first one uses a bool, which uses a byte, to determine the existence
of an element, whereas the second one uses an empty struct, which doesn't use
any space.

```go
intSet := map[int]bool{}
vals := []int{5, 10, 2, 5, 8, 7, 3, 9, 1, 2, 10}

for _, v := range vals {
    intSet[v] = true
}

fmt.Println(len(vals), len(intSet))
fmt.Println(intSet[5])
fmt.Println(intSet[500])

if intSet[100] {
    fmt.Println("100 is in the set")
}
```

```go
intSet := map[int]struct{}{}
vals := []int{5, 10, 2, 5, 8, 7, 3, 9, 1, 2, 10}

for _, v := range vals {
    intSet[v] = struct{}{}
}

if _, ok := intSet[5]; ok {
    fmt.Println("5 is in the set")
}
```

The disadvantage is that using a `struct{}` makes your code more clumsy. You
have a less obvious assignment, and you need to use the `comma ok idiom` to
check if a value is in the set:

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

In the expression `z = x &^ y`, each bit of `z` is `0` if the corresponding bit
of `y` is `1`; otherwise it equals the corresponding bit of `x`.

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

In the following example, `defer` modifies the return value and this modified
value is what would be seen by the caller.

```go
package main

import "fmt"

func compute(inpVal int) (retVal int) {
    defer func() int {
        fmt.Printf("In defer: %d, %d\n", retVal, retVal+100)
        retVal += 100
        return 1000 // This return value can't be captured
    }()

    retVal = inpVal + 100
    fmt.Printf("Before defer: %d, %d\n", inpVal, retVal)
    return retVal
}

func main() {
    fmt.Println(compute(100))
}

Output:
~~~~~~
Before defer: 100, 200
In defer: 200, 300
300
```

# Interfaces

Interfaces are abstract types that let us treat different concrete types in the
same way based on what methods they have, not how they are represented or
implemented.

# Methods

A method is a function associated with a named type; Go is unusual in that
methods may be attached to almost any named type. 

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

## Pointer Receivers and Value Receivers

A method needs to receive a Pointer Receiver:

1. If the method needs to modify the receiver.

2. If the method needs to handle `nil` instances.

3. When a type has _any_ pointer receiver methods, a common practice is to be
   consistent and use pointer receivers for _all_ methods, even the ones that
   don’t modify the receiver.

If a method doesn’t modify the receiver, it can be of either Receiver type.

By convention, the receiver name is a short abbreviation of the type’s name,
usually its first letter. It is _non-idiomatic_ to use `this` or `self`.

```go
type Counter struct {
    total             int
    lastUpdated time.Time
}

func (c *Counter) Increment() {
    c.total++
    c.lastUpdated = time.Now()
}

func (c Counter) String() string {
    return fmt.Sprintf("total: %d, last updated: %v", c.total, c.lastUpdated)
}

func main() {
	var c Counter
	fmt.Println(c.String())
	c.Increment() // Calling a method with a Pointer Receiver using a "value type"
	fmt.Println(c.String())
}

Output: // Note that c.total is incremented because of the Pointer Receiver type
~~~~~~
total: 0, last updated: 0001-01-01 00:00:00 +0000 UTC
total: 1, last updated: 2022-02-06 00:15:03.499482931 +0530 IST m=+0.000098083
```

When you use a pointer receiver with a local variable that’s a value type, Go
automatically converts it to a pointer type. In this case, `c.Increment()` is
converted to `(&c).Increment()`.

However, be aware that the rules for passing values to functions still apply. If
you pass a value type to a function and call a pointer receiver method on the
passed value, you are invoking the method on a copy.

## Declaration of Methods

Methods must be declared in the same package as their associated type; Go
doesn’t allow you to add methods to types you don’t control. While you can
define a method in a different file within the same package as the type
declaration, it is best to keep your type definition and its associated methods
together so that it’s easy to follow the implementation.

## Code your Methods for nil Instances

Invoking a method with a value receiver with a `nil` instance results in a panic
as there is no value being pointed to by the pointer. If it's a method with a
pointer receiver, it can work if the method checks and handles `nil`
instance. There are scenarios where having such methods handling `nil` instance
make the code appear better, but such scenarios don't occur that often.

```go
type IntTree struct {
    val         int
    left, right *IntTree
}

func (it *IntTree) Insert(val int) *IntTree {
    if it == nil {
        return &IntTree{val: val}
    }
    if val < it.val {
        it.left = it.left.Insert(val)
    } else if val > it.val {
        it.right = it.right.Insert(val)
    }
    return it
}

func (it *IntTree) Contains(val int) bool {
    switch {
    case it == nil:
        return false
    case val < it.val:
        return it.left.Contains(val)
    case val > it.val:
        return it.right.Contains(val)
    default:
        return true
    }
}
```

The `Contains` method doesn’t modify the `*IntTree`, but it is declared with a
pointer receiver. A method with a value receiver can’t check for `nil` and
panics if invoked with a nil receiver.

Pointer receivers work just like pointer function parameters; it’s a copy of the
pointer that’s passed into the method. Just like `nil` parameters passed to
functions, if you change the copy of the pointer, you haven’t changed the
original. This means you can’t write a pointer receiver method that handles
`nil` and makes the original pointer non-nil. If your method has a pointer
receiver and won’t work for a `nil` receiver, check for `nil` and return an
error.

## Methods are Functions too

Methods in Go are so much like functions that you can use a method as a
replacement for a function any time there’s a variable or parameter of a
function type.

```go
type Adder struct {
    start int
}

func (a Adder) AddTo(val int) int {
    return a.start + val
}
```

We create an instance of the type in the usual way and invoke its method:

```go
myAdder := Adder{start: 10}
fmt.Println(myAdder.AddTo(5)) // prints 15
```

We can also assign the method to a variable or pass it to a parameter of type
`func(int)int`. This is called a `method value`. A _method value_ is a bit like
a closure, since it can access the values in the fields of the instance from
which it was created.

```go
f1 := myAdder.AddTo
fmt.Println(f1(10))           // prints 20
```

You can also create a function from the type itself. This is called a `method
expression`. In the case of a _method expression_, the first parameter is the
receiver for the method; our function signature is `func(Adder, int) int`.

```go
f2 := Adder.AddTo
fmt.Println(f2(myAdder, 15))  // prints 25
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

# Formatting

By convention, formatting functions whose names end in _f_, such as `log.Printf`
and `fmt.Errorf`, use the formatting rules of `fmt.Printf`, whereas those whose
names end in _ln_ follow `Println`, formatting their arguments as if by `%v`,
followed by a ne wline.

## Printf formatting tricks

We can control the radix and format with the `%d`, `%o`, and `%x` verbs:

```go
o := 0666
fmt.Printf("%d %[1]o %#[1]o\n", o)
// Output: 438 666 0666

x := int64(0xdeadbeef)
fmt.Printf("%d %[1]x %#[1]x %#[1]X\n", x)
// Output: 3735928559 deadbeef 0xdeadbeef 0XDEADBEEF
```

Usually a `Printf` format string containing multiple `%` verbs would require the
same number of extra operands, but the `[1]` _adverbs_ after `%` tell `Printf`
to use the first operand over and over again. Second, the `#` _adverb_ for `%o`
or `%x` or `%X` tells `Printf` to emit a `0` or `0x` or `0X` prefix
respectively.

# Packages

Packages in Go help provide modularity, encapsulation, separate compilation, and
reuse. The source code for a package resides in one or more `.go` files, usually
in a directory whose name ends with the import path; for instance, the files of
the `gopl.io/ch1/helloworld` package are stored in directory
`$GOPATH/src/gopl.io/ch1/helloworld`.

Each package serves as a separate name space for its declarations. Within the
`image` package, for example, the identifier `Decode` refers to a different
function than does the same identifier in the `unicode/utf16` package. To refer
to a function from outside its package, we must qualify the identifier to make
explicit whether we mean `image.Decode` or `utf16.Decode`.

Package-level names like the types and constants declared in one file of a
package are visible to all the other files of the package, as if the source code
were all in a single file.

Packages also let us hide information by controlling which names are visible
outside the package, or _exported_.

## Exporting and Importing Symbols

A name is exported if it starts with a capital letter. For instance, `math`
package exports the symbol `Pi`. Similarly when importing a package, you can
refer only its exported names, which means, only those symbols that start with a
capital letter.

## Compilation error with unused packages

Go automatically flags an error during compilation if packages are declared but
unused.

# init functions

Any file may contain any number of functions whose declaration is just

`func init() { /* ... */ }`

Such init functions can’t be called or referenced, but otherwise they are normal
functions. Within each file, init functions are automatically executed when the
program starts, in the order in which they are declared.
```go
package main

import (
    "fmt"
)

func init() {
    fmt.Println("Init function 1")
}

func init() {
    fmt.Println("Init function 2")
}

func main() {
    fmt.Println("In main")
}
```
The above program produces the following output:
```go
go run test.go

Init function 1
Init function 2
In main
```

# Variadic

In the following, `append` is a `variadic function` as it can accept params of
the form `x...`.

```go
var x []int
x = append(x, 1)
x = append(x, 2, 3)
x = append(x, 4, 5, 6)
x = append(x, x...)     // append the slice x
fmt.Println(x)          // "[1 2 3 4 5 6 1 2 3 4 5 6]"
```

The following example shows how to define a _variadic function_.

```go
func appendInt(x []int, y ...int) []int { ... }
```

Here is another example:

```go
func addTo(base int, vals ...int) []int {
    out := make([]int, 0, len(vals))
    for _, v := range vals {
        out = append(out, base+v)
    }
    return out
}

func main() {
    fmt.Println(addTo(3))
    fmt.Println(addTo(3, 2))
    fmt.Println(addTo(3, 2, 4, 6, 8))
    a := []int{4, 3}
    fmt.Println(addTo(3, a...))
    fmt.Println(addTo(3, []int{1, 2, 3, 4, 5}...))
}
```

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
