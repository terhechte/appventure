[frontMatter]
title = "Fibonacci"
tags = ["pattern matching", "switch"]
created = "2019-02-15 20:40:47"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Fibonacci

Also, see how beautiful an implementation of the fibonacci algorithm
looks with pattern matching.

``` Swift
func fibonacci(i: Int) -> Int {
    switch(i) {
    case let n where n <= 0: return 0
    case 0, 1: return 1
    case let n: return fibonacci(n - 1) + fibonacci(n - 2)
    }
}

print(fibonacci(8))
```

Since we're doing recursion here, this will fail to work with sufficiently large numbers
(you'll see the dreaded `stack overflow` error)
