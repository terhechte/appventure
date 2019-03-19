[frontMatter]
title = "Type Aliases"
tags = ["tuples", "tupealias"]
created = "2019-03-01 17:35:30"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Type Aliases

In many of the earlier examples, we rewrote a certain tuple type like
`(Int, Int, String)` multiple times. This, of course, is not necessary,
as we could define a `typealias` for it:

``` Swift
typealias Example = (Int, Int, String)
func add(elm: Example) { }
```

However, if you\'re using a certain tuple construction so often that you
think about adding a typealias for it, you might really be better off
defining a struct.
