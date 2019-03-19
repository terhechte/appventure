[frontMatter]
title = "Creating and Accessing Tuples"
tags = ["tuples"]
created = "2019-03-01 17:35:30"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# The absolute Basics

A tuple can combine different types into one. Where an array is a sequence
of a certain type (`let x: [Int] = [1, 2, 3, 4, 5]`) a tuple can have
a different type for each element: `let x: (Int, Double, String) = (5, 2.0, "Hey")`.

Tuples are a very simple manner of grouping related data items together without having
to create a struct.

They are value types and even though they look like sequences they aren\'t.
One main difference is that you can't easily loop over the contents of a tuple.

We\'ll start with a quick primer on how to create and use tuples.

# Creating and Accessing Tuples

``` Swift
// Constructing a simple tuple
let tuple1 = (2, 3)
let tuple2 = (2, 3, 4)

// Constructing a named tuple
let tupl3 = (x: 5, y: 3)

// Different types
let tuple4 = (name: "Carl", age: 78, pets: ["Bonny", "Houdon", "Miki"])

```

Once you've created some tuples, you can access their elements:

``` Swift
// Accessing tuple elements
let tuple5 = (13, 21)
tuple5.0 // 13
tuple5.1 // 21

// Access by name
let tuple6 = (x: 21, y: 33)
tuple6.x // 21
tuple6.y // 33
```

Nice, so now you can create tuples and access their elements. But what would you 
use them for? The use case we will discuss is for `pattern matching`.
