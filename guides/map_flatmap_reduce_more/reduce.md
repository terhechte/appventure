[frontMatter]
title = "Reduce"
tags = ["map", "compactMap", "filter", "reduce"]
created = "2019-02-20 19:49:10"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Reduce

Reduce is sort of a generalized version of `map`, `compactMap`, `flatMap`, or
`filter`. The basic idea is to **reduce** a sequence into a different
shape utilizing an **accumulator** that can keep incremental state. To
do this, we hand the function a **combinator** closure/function/method
which is called once for each item in the sequence. This may sound
complicated but becomes really easy with a couple of examples.

It is a method on `SequenceType` and looks like this (simplified):

``` Swift
func reduce<T>(_ initialResult: T, _ nextPartialResult: (T, Self.Generator.Element) -> T) -> T
```

There're two parameters here:
1. A `initialResult` value of generic type `T`
2. A closure `nextPartialResult` that receives two parameters and returns the generic type `T`. The two parameters are `T`, once again, and the element type of the array. Imagine we had an array of `String` and we'd like to `reduce` it to the count of elements `Int`. Reduce would look like this:

``` Swift
func reduce(_ initialResult: Int, _ nextPartialResult: (Int, String) -> Int) -> Int
```

So here we have an initial value `Int`, and we have a closure which expects us to
return the same type as the initial value (`Int`). The final value of the
operation is also of the same type as the initial value.

If we take a very simple reduce operation - counting the elments in an array of `String` - , the evaluation will look like this:

``` Swift
func count(accumulator: Int, current: Int) -> Int {
   return accumulator += 1
}
[1, 2, 3].reduce(0, count)

// The following steps will be performed
count(0, 1) { return 0 + 1 } = 1
count(1, 2) { return 1 + 1 } = 2
count(2, 3) { return 2 + 1 } = 3
= 6
```

And if we want to sum up the integer elements in an array of `Int`, we'd write this:

``` Swift
func sum(accumulator: Int, current: Int) -> Int {
   return accumulator + current
}
[1, 2, 3].reduce(0, sum)
// The following steps will be performed
sum(0, 1) { return 0 + 1 } = 1
sum(1, 2) { return 1 + 2 } = 3
sum(3, 3) { return 3 + 3 } = 6
= 6
```

The **nextPartialResult** closure (`sum` in our example) will be called once for each item in the
list `[1, 2, 3]`. The state will be kept in the **accumulator** variable
which is just an Integer.

Let\'s start re-implementing some of our other, trusted, functional
programming friends. In order to keep things simple for now, all these
functions will operate on `Int` or `Optional<Int>`; i.e. we will ignore
generics in here. Also, keep in mind that the implementations below
exist to explain the behaviour of `reduce`. The native Swift
implementations are usually much faster compared to the reduce versions
below. Reduce shines in a different set of problems, which will be
explained further below.

