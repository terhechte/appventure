[frontMatter]
title = "Wildcard Pattern"
tags = []
created = "2019-02-15 20:40:47"
description = ""
published = false

---

# Wildcard Pattern

The wildcard pattern ignores the value to be matched against. In this
case any value is possible. This is the same pattern as `let _ = fn()`
where the `_` indicates that you don\'t wish to further use this value.
The interesting part is that this matches all values including `nil`
[^1]. You can even match optionals by appending a `?`:

``` Swift
let p: String? = nil
switch p {
case _?: print ("Has String")
case nil: print ("No String")
}
```

As you\'ve seen in the trading example, it also allows you to omit the
data you don\'t need from matching `enums` or `tuples`:

``` Swift
switch (15, "example", 3.14) {
    case (_, _, let pi): print ("pi: \(pi)")
}
```
