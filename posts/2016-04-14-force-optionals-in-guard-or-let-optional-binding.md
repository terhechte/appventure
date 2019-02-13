[frontMatter]
description = "Mixing optional and non-optional functions in a guard is impossible and requires breaking up the lines. Here's a neat solution on how to circumvent this."
title = "Force optionals in multi-unwrapped 'guard let' or 'if let'"
created = "2016-04-14"
published = true
keywords = ["swift", "guard", "let", "unwrap", "bind", "binding", "unwrapped", "optional", "some", "none", "optionals"]
slug = "2016-04-14-force-optionals-in-guard-or-let-optional-binding.html"
tags = ["swift", "cocoa", "ios"]
---

I really love unwrapping optionals in a multi- `guard` or `let`
statement with additional `where` clauses added. [See my previous post
on this
here](https://appventure.me/2016/03/29/three-tips-for-clean-swift-code/).
However, sometimes I run into a situation where I have one function call
(or a array subscript) in between my others that does not return an
optional:

``` Swift
// Imagine this function does something complicated
func someArray() -> [Int]? {
    return [1, 2, 3, 4, 5, 6]
}

func example() {
    guard let array = someArray(),
        numberThree = array[2]
        where numberThree == 3
        else { return }
    print(numberThree)
}

```

This doesn\'t work. The compiler will explain to you that it expects an
optional:

> \"Initializer for conditional binding must have Optional type, not
> \'Int\'\"

So, what you oftentimes end up with, instead, is something like this:

``` Swift
func example() {
    guard let array = someArray() else { return }
    let numberThree = array[2]
    guard numberThree == 3 else { return }
    print(numberThree)
}
```

Not only is this awful to look at, you also have to write the failure
block twice. That\'s ok for a simple example as this one `{ return }`,
but when you have to perform a bit more work in there you\'ll have to
repeat code blocks; and that\'s bad [^1].

So what\'s the solution here? Well, since the `guard` or `let` requires
an optional, we can just as well create one and unpack it again:

``` Swift
func example() {
    guard let array = someArray(),
        numberThree = Optional.Some(array[2])
        where numberThree == 3
        else { return }
    print(numberThree)
}
```

As you may remember, Swift\'s optionals are internally more or less
`enums` with a `.Some` and a `.None` case. So what we\'re doing here is
creating a new `.Some` case only to unwrap it again in the very same
line: The `array[2]` expression will be wrapped with `Optional.Some` and
then unwrapped again into `numberThree`.

There is a wee bit of overhead here, but on the other hand it does allow
us to keep the `guard` or `let` unwrappings much cleaner.

This obviously doesn\'t just work with array subscripts like `array[3]`
but also with any non-optional function, i.e.:

``` Swift
guard let aString = optionalString(),
    elements = Optional.Some(aString.characters.split("/")),
    last = elements.last,
    count = Optional.Some(last.characters.count),
    where count == 5 else { fatalError("Wrong Path") }
print("We have \(count) items in \(last)")
```

[^1]: Or you start refactoring this into seperate closures or functions,
    but that\'s an awful lot of work for just one guard statement
