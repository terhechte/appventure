[frontMatter]
description = "Swift's @autoclosure allows to extend the Swift syntax in fantastic ways. Observe how we re-implement the `cond` function from Lisp"
title = "Using @autoclosure to write a Swift syntax extension"
created = "2014-06-08"
published = true
keywords = ["clojure", "lisp", "swift", "cond", "syntax", "macro", "extension", "cocoa", "ios", "feature"]
slug = "2014-06-08-writing-simple-syntax-extensions-in-swift.html"
tags = ["autoclosure"]
category = ["Language", "All"]

[meta]
swift_version = "1.0"
---

It has been less than a week since Apple announced Swift, and people are
already writing libraries, snippet collections, or best practice posts.
I suppose most did not even find the time to thouroughly read the Swift
Book yet [^1].

Some Examples are the [Swift
Cheatsheet](https://github.com/grant/swift-cheat-sheet), [Swiftz, a
functional programming paradigm library for
Swift](https://github.com/maxpow4h/swiftz), or [blog posts like this
one.](http://nategriswold.blogspot.com/2014/06/couple-swift-notes-from-wwdc.html)

### Simple Custom Syntax

One Swift cricitism has been the lack of a macro system that would allow
users to freely extend the language like Lisp (and other homoiconic)
languages do. While this is indeed not possible, there is a hidden gem
in the Swift language that gives us some flexibility in this domain. If
you look at the Swift documentation for the various operators, you\'ll
find this line:

``` Swift
func &&(lhs: LogicValue, rhs: @auto_closure () -> LogicValue) -> Bool
```

The `&&` operator has two arguments: The left hand side and the right
hand side. Swift first checks the left hand side. If this evaluates to
true, only then will it evaluate the right hand side. This means that
the right hand side expression will defer evaluation until the left hand
side was evaluated.

How does Swift do this? Through the magic `@auto_closure` syntax. This
tells Swift to wrap the expression into a closure and only evaluate it
if explicitly told to do so. The full function might look something like
this

``` Swift
func &&(lhs: LogicValue, rhs: @auto_closure () -> LogicValue) -> Bool {
  // Proof for left hand side
  if lhs {
    // Only then execute and thus proof right hand side
    if rhs() == true {
      return true
    }
  }
  return false
}
```

This is an interesting feature and allows us to implement more complex
constructs with a bit of tinkering. How about implementing something
new, namely the `cond` expression from Lisp?

### Writing a cond expression for Swift

In Lisp, `cond` works as follows:

``` Clojure
(cond ((= a 1) "a is one")
      ((= a 2) "a is two")
      ((= a 4) "a is four"))
```

Much like a `switch` statement, different cases are being tested for.
Each line defines a test and after that a expression result. So if a
equals 2 the switch statement will return \"a is two\". If a equals 1,
it will return \"a is one\". In comparison to `switch`, `cond` also
allows to test for different variables in one statement (i.e. is a 2 or
is b 3). Another difference is that `cond` returns a value, while the
Swift `switch` statement does not ([there\'s actually a rdar bug for
this](http://nategriswold.blogspot.com/2014/06/couple-swift-notes-from-wwdc.html))

Given the `@auto_closure` feature from above, we can actually implement
`cond` in Swift ourselves.

-   We need an expression that evaluates to bool `() -> Bool`
-   We need an expression that evaluates to Any result type `() -> Any`

These should be wrapped into closures, so that they will be evaluated
sequentially and only if necessary. Lets start with a simple
implementation and build upon that.

Imagine the following situation: You\'re processing user input, and you
want to delete something from either the memory or the database,
depending on what the user selected.

We want something that works for the current theoretical code:

``` Swift
var a = get_user_input()
var b = get_current_entity()
// delete fro memory or db depending on what user selected
var result = cond(a == 1, delete_from_db(b),
                  a == 2, delete_from_memory(b))
// make sure we deleted the correct one
if result != b ....
```

The important part here is that `delete_from_db` and
`delete_from_memory` are only being executed if the condition \'a == ?\'
is true for the selected case. Under no circumstance do we want our
entity to be deleted from the db and the memory.

### A first version

``` Swift
func cond_1 (a1: @auto_closure () -> Bool, b1: @auto_closure () -> Any,
    a2: @auto_closure () -> Bool, b2: @auto_closure () -> Any,
    bf: @auto_closure () -> Any) -> Any {
        if a1() {
            return b1()
        } else if a2() {
            return b2()
        }
        return bf()
}
```

There\'s our expression. We can hand it two different cases and a
default expression (as a fallback). Lets see how it works. We will
define two simple functions that perform side effects (imagine deleting
a file, or writing to a file).

``` Swift
func perform_side_effects1() -> Any {
    println("modify a state")
    return 1
}
func perform_side_effects2() -> Any {
    println("modify another state")
    return 2
}

var a = 1
var ctest = cond_1(a == 1, 2 + perform_side_effects1(),
                  a == 2, 3 + perform_side_effects2(),
                  0)
// ctest is 3 (2 + 1)
// prints only "modify a state"
ctest

```

### Handling more cases

This works fine, but it has a limitation in that it only works for two
cases. This is clearly not optimal. Thankfully, Swift is pretty good at
function overloading so we can simply define more functions with more
cases and let swift do the hard work of figuring out which one to
choose:

``` Swift
func cond_2 (a1: @auto_closure () -> Bool, b1: @auto_closure () -> Any,
    a2: @auto_closure () -> Bool, b2: @auto_closure () -> Any,
    bf: @auto_closure () -> Any) -> Any {
        if a1() {
            return b1()
        } else if a2() {
            return b2()
        }
        return bf()
}

func cond_2 (a1: @auto_closure () -> Bool, b1: @auto_closure () -> Any,
    a2: @auto_closure () -> Bool, b2: @auto_closure () -> Any,
    a3: @auto_closure () -> Bool, b3: @auto_closure () -> Any,
    bf: @auto_closure () -> Any) -> Any {
        if a1() {
            return b1()
        } else if a2() {
            return b2()
        } else if a3() {
            return a3()
        }
        return bf()
}
```

You can then extend this to ever more cases. Of course, this smells like
code duplication and there is a way around this, but that currently
crashes the Swift Compiler. I\'ll come back to how to (at least
theoretically) do this at the end. First, there is another issue that we
need to address.

### Making it generic

Our current version succumbs every variable down to the `Any` type which
means that the compiler won\'t be able to perform advanced type
inference for anything that comes out of this function. For example, the
following will not work because even though we\'re clearly returning
`Int` our actual function is set to return `Any`

``` Swift
// Causes an error
var b:Int = cond_2(0 == 1, 1, 0 == 2, 2, 3)
// Works fine
var b:Any = cond_2(0 == 1, 1, 0 == 2, 2, 3)
```

Since types give us safety we\'d rather have a funcion that tells us if
we accidentally try to do something wrong here. Thankfully, Swift has
support for [Generic
Programming](http://en.wikipedia.org/wiki/Generic_programming) and only
a simple change is necessary for this:

``` Swift
func cond_3<T> (a1: @auto_closure () -> Bool, b1: @auto_closure () -> T,
    a2: @auto_closure () -> Bool, b2: @auto_closure () -> T,
    bf: @auto_closure () -> T) -> T {
        if a1() {
            return b1()
        } else if a2() {
            return b2()
        }
        return bf()
}

// Works fine!
var b:Int = cond_3(0 == 1, 1, 0 == 2, 2, 3)
```

That\'s it, now we\'re telling Swift that this function handles items of
type T and that the very same type T is the return type of this funcion.

Through this, we can use our cond~3~ function on types of any kind like
String, Array, Int, or custom types.

### Wrap up

That\'s it! We\'ve implemented our own syntax extension for Swift! Now
we can write code this as this

``` Swift
var a = get_user_input()
var b = get_current_entity()
// delete fro memory or db depending on what user selected
var result = cond(a == 1, delete_from_db(b),
                  a == 2, delete_from_memory(b))
// make sure we deelted the correct one
if result != b ....
```

Now, the entity would only be deleted from db or from memory if a
contains the correct variable. Keep in mind that this was only a simple
example. Much more is possible if you use this in a smart way.

Even better if one combines this in a neat way with the first closure as
body mechanism or with operators. I\'m sure that we can already create
some pretty stunning syntax extensions with this. However, this, only if
it doesn\'t crash the compiler, which brings us to the next and final
section.

### Limitations

All current Swift projects suffer from the current slightly beta state
of the build tools and the Swift compiler. This leads to much code that
looks a bit cumbersome but can easily be improved in the future. In this
case, here\'s some untested code, that wraps the complete logic in one
big function and only defines additional lightweight wrappers to deal
with the parameters variations. Still not optimal but much more
readable. Sadly, this crashes the compiler (actually it kills Xcode the
minute you type it in, which is pretty impressive.[^2]).

``` Swift
func _cond<T> (a1: @auto_closure () -> Bool, b1: @auto_closure () -> T?,
    a2: @auto_closure () -> Bool, b2: @auto_closure () -> T?,
    a3: @auto_closure () -> Bool, b3: @auto_closure () -> T?,
    a4: @auto_closure () -> Bool, b4: @auto_closure () -> T?,
    a5: @auto_closure () -> Bool, b5: @auto_closure () -> T?
) -> T? {
        if a1() {
            return b1()
        } else if a2() {
            return b2()
        } else if a3() {
            return b3()
        } else if a4() {
            return b4()
        } else if a5() {
            return a5()
        }
        return nil
}
// two parameter implementation
func cond<T>(a1: @auto_closure () -> Bool, b1: @auto_closure () -> T,
    a2: @auto_closure () -> Bool, b2: @auto_closure () -> T,
    bf: @auto_closure () -> T) -> T {
        if let r = _cond(a1, b1, a2, b2, false, {}(), false, {}(), false, {}()) {
            return r
        }
        return bf()
}
// three parameter implementation
func cond<T>(a1: @auto_closure () -> Bool, b1: @auto_closure () -> T,
    a2: @auto_closure () -> Bool, b2: @auto_closure () -> T,
    a3: @auto_closure () -> Bool, b3: @auto_closure () -> T,
    bf: @auto_closure () -> T) -> T {
        if let r = _cond(a1, b1, a2, b2, a3, b3, false, {}(), false, {}()) {
            return r
        }
        return bf()
}
```

I\'m not sure if this would lead to correct results if it would work,
but based on my current understanding of the language it should be fine.

### Update

[bjustin](https://news.ycombinator.com/user?id%3Dbjustin) offered [this
slight modification](https://news.ycombinator.com/item?id%3D7865603)
that makes it easy to use unlimited cases. The only downside is that the
fallback has to be the first item.

``` Swift
func cond<T>(#fallback: T, testsAndExprs: (test: @auto_closure () -> Bool, expr: @auto_closure () -> T)...) -> T {
    for (t, e) in testsAndExprs {
        if t() {
            return e()
        }
    }
    return fallback
}

// And in use:

// y is assigned "0 == 0, of course"
let y = cond(fallback: "fallback", (test: false, expr: "not this branch"), (test: 0 == 0, expr: "0 == 0, of course"))
```

[^1]: I completely omitted the language reference. Impossible to work
    through something like that during a chronically sleep-deprived week
    like WWDC

[^2]: Rdar 17224140
