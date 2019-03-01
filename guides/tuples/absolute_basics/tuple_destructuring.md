[frontMatter]
title = "Tuple Destructuring"
tags = []
created = "2019-03-01 17:35:30"
description = ""
published = false

---

# Tuple Destructuring

Swift took a lot of inspiration from different programming languages,
and this is something that Python has been doing for years. While the
previous examples mostly showed how to easily get something into a
tuple, destructuring is a swifty way of getting something out of a
tuple, and in line with the `abc` example above, it looks like this:

``` Swift
let (a, b, c) = abc()
print(a)
```

Another example is getting several function calls into one line:

``` Swift
let (a, b, c) = (a(), b(), c())
```

Or, an easy way to swap two values:

``` Swift
var v1: Int
var v2: Int
(v1, v2) = (5, 4)
(a: v1, b: v2) = (a: v2, b: v1) // swapped: v1 == 4, v2 == 5
(v1, v2) = (5, 4)
(a: v1, b: v2) = (b: v1, a: v2) // swapped: v1 == 4, v2 == 5

```
