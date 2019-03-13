[frontMatter]
title = "Wildcard Pattern"
tags = ["pattern matching", "switch", "wildcard"]
created = "2019-02-15 20:40:47"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Wildcard Pattern

The wildcard pattern ignores the value to be matched against. In this
case any value is possible. This is the same pattern as `let _ = fn()`
where the `_` indicates that you don\'t wish to further use this value.
The interesting part is that this matches all values including `nil`. 

You can also match [optionals](apv::optional) by appending a `?` to make it `_?`:

``` Swift
let p: String? = nil
switch p {
// Any value is possible, but only if the optional has a value
case _?: print ("Has String")
// Only match the empty optional case
case nil: print ("No String")
}
```

As you\'ve seen in the trading example, it also allows you to omit the
data you don\'t need from matching `enums` or `tuples`:

``` Swift
switch (15, "example", 3.14) {
    // We're only interested in the last value
    case (_, _, let pi): print ("pi: \(pi)")
}
```
