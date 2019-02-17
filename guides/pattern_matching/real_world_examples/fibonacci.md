[frontMatter]
title = "Fibonacci"
tags = []
created = "2019-02-15 20:40:47"
description = ""
published = false

---

# Fibonacci

Also, see how beautiful an implementation of the fibonacci algorithm
looks with pattern matching [^3]

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

Of course, this will kill your stack with big numbers.
