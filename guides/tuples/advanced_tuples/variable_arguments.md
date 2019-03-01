[frontMatter]
title = "Variable Arguments"
tags = []
created = "2019-03-01 17:35:30"
description = ""
published = false

---

# Variable Arguments

Varargs i.e. variable function arguments are a very useful technique for
situations where the number of function parameters is unknown.

``` Swift
// classic example
func sum(of numbers: Int...) -> Int {
    // add up all numbers with the + operator
    return numbers.reduce(0, +)
}

let theSum = sum(of: 1, 2, 5, 7, 9) // 24
```

A tuple can be useful here if your requirement goes beyond simple
integers. Take this function, which does a batch update of `n` entities
in a database:

``` Swift
func batchUpdate(updates: (String, Int)...) {
    self.db.begin()
    for (key, value) in updates {
        self.db.set(key, value)
    }
    self.db.end()
}

// We're imagining a weird database
batchUpdate(updates: ("tk1", 5), ("tk7", 9), ("tk21", 44), ("tk88", 12))
```
