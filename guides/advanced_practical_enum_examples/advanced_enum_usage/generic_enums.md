[frontMatter]
title = "Generic Enums"
tags = ["enum", "generics", "where"]
created = "2019-03-01 16:29:51"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Generic Enums

Enums can also be defined over generic parameters. You\'d use them to
adapt the associated values of an enum. The simplest example comes
straight from the Swift standard library, namely the [`Optional` type](lnk::optional).
You probably mostly use it with **optional chaining** (`?`), `if let`,
`guard let`, or `switch`, but syntactically you can also use Optionals
like so:

``` Swift
let aValue = Optional<Int>.some(5)
let noValue = Optional<Int>.none
if noValue == Optional.none { print("No value") }
```

This is the direct usage of an Optional without any of the syntactic
sugar that Swift adds in order to make your life a tremendous amount
easier. If you look at the code above, you can probably guess that
internally the `Optional` is defined as follows [^5]:

``` Swift
// Simplified implementation of Swift's Optional
enum MyOptional<T> {
  case some(T)
  case none
}
```

What\'s special here is, that the enum\'s **associated values** take the
type of the generic parameter `T`, so that optionals can be built for
any kind you wish to return.

Enums can have multiple generic parameters. Take the well-known
**Either** type which is not part of Swift\'s standard library but
implemented in many open source libraries as well as prevalent in other
functional programming languages like Haskell or F\#. The idea is that
instead of just returning a value or no value (née Optional) you\'d
return either one of two different values. 

For example, if you parse user input, the user could enter a name or a number,
in that case the type of `Either` would be `Either<String, Int>`.

``` Swift
enum Either<T1, T2> {
  case left(T1)
  case right(T2)
}
```

Finally, all the type constraints that work on classes and structs in
Swift also work on enums. Here, we have a type `Bag` that is either empty
or contains an array of elements. Those elements **have** to be `Equatable`.

``` Swift
enum Bag<T: Sequence> where T.Iterator.Element==Equatable {
    case empty
    case full(contents: [T)]
}
```

