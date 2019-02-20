[frontMatter]
title = "Reduce"
tags = []
created = "2019-02-20 19:49:10"
description = ""
published = false

---

# Reduce

Reduce is sort of a generalized version of `map`, `flatMap`, or
`filter`. The basic idea is to **reduce** a sequence into a different
shape utilizing an **accumulator** that can keep incremental state. To
do this, we hand the function a **combinator** closure/function/method
which is called once for each item in the sequence. This may sound
complicated but becomes really easy with a couple of examples.

It is a method on `SequenceType` and looks like this (simplified):

``` Swift
func reduce<T>(initial: T, combine: (T, Self.Generator.Element) -> T) -> T
```

So we have an initial value, and we have a closure which expects us to
return the same type as the initial value. The final value of the
operation is also of the same type as the initial value.

If we take a very simple reduce operation - adding up a list of
integers, the evaluation will look like this:

``` Swift
func combinator(accumulator: Int, current: Int) -> Int {
   return accumulator + current
}
[1, 2, 3].reduce(0, combine: combinator)
// The following steps will be performed
combinator(0, 1) { return 0 + 1 } = 1
combinator(1, 2) { return 1 + 2 } = 3
combinator(3, 3) { return 3 + 3 } = 6
= 6
```

The **combinator** function will be called once for each item in the
list `[1, 2, 3]`. The state will be kept in the **accumulator** variable
which is just an Integer.

Let\'s start re-implementing some of our other, trusted, functional
programming friends. In order to keep things simple for now, all these
functions will operate on `Int` or `Optional<Int>`; i.e. we will ignore
generics in here. Also, keep in mind that the implementations below
exist to explain the behaviour of `reduce`. The native Swift
implementations are usually much faster compared to the reduce versions
below[^1]. Reduce shines in a different set of problems, which will be
explained further below.

[^1]: For reasons why, [have a look at this blog
    post](http://airspeedvelocity.net/2015/08/03/arrays-linked-lists-and-performance/)
