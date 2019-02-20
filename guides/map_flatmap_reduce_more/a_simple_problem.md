[frontMatter]
title = "A Simple Problem"
tags = []
created = "2019-02-20 19:49:10"
description = ""
published = false

---

# A simple Problem

Consider this problem: You\'re getting a list of persons from a JSON
endpoint. You\'d like to know the average age from all people living in
California. The parsed data looks like this:

``` Swift
let persons: [[String: AnyObject]] = [["name": "Carl Saxon", "city": "New York, NY", "age": 44],
 ["name": "Travis Downing", "city": "El Segundo, CA", "age": 34],
 ["name": "Liz Parker", "city": "San Francisco, CA", "age": 32],
 ["name": "John Newden", "city": "New Jersey, NY", "age": 21],
 ["name": "Hector Simons", "city": "San Diego, CA", "age": 37],
 ["name": "Brian Neo", "age": 27]]
```

Note the last entry, which omits a `city` for the person in question.
Those cases have to be silently ignored.

The expected result in the example would be 3 persons , as we have three
persons from California. Let\'s try to implement this in Swift in terms
of `flatMap` and `filter`. The `flatMap` is used instead of `map` as
`flatMap` automatically ignores empty optionals. So
`flatMap([0, nil, 1, 2, nil])` results in `[0, 1, 2]`. This eases the
handling of persons without a proper city.

``` Swift
func infoFromState(state state: String, persons: [[String: AnyObject]]) 
     -> Int {
    return persons.flatMap( { $0["city"]?.componentsSeparatedByString(", ").last })
           .filter({$0 == state})
           .count
}
infoFromState(state: "CA", persons: persons)
//#+RESULTS:
//: 3
```

That\'s simple enough.

However, now consider the following complication: You\'d like to know
how many of those persons live in California, and you\'d like to know
their average age. If we try upgrading the above example, we soon
realize that his is a slightly harder problem. There are various
solutions, but they all seem to not fit well with functional constructs.
A loop-based approach feels much simpler.

When we think about why this does fit, we realize it is because the
shape of the data changes. `map`, `flatMap`, and `filter` all keep the
shape of the data similar. Array goes in, array goes out. The amount and
the contents of the array may change, but the array-shape stays. The
problem above, however, requires us to change the shape to a `struct` or
`tuple` with an **Integer average** and an **Integer sum**.

These are the kind of problems where you can apply `reduce`.
