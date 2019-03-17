[frontMatter]
title = "Optionals"
tags = ["pattern matching", "switch", "optional"]
created = "2019-02-15 20:40:47"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Optionals

[There\'re many ways to unwrap
optionals,](lnk::optional)
and pattern matching is one of them. You\'ve probably used that quite
frequently by now, nevertheless, here\'s a short example:

``` Swift
var result: String? = secretMethod()
switch result {
case nil:
    print("is nothing")
case let a?:
    print("\(a) is a value")
}
```

As you can see, `result` could be a string, but it could also be `nil`.
It\'s an `Optional`. By switching on result, we can figure out whether
it is `.none` or whether it is an actual value. Even more, if it is a
value, we can also bind this value to variable right away. In this case
`a`. What\'s beautiful here, is the clearly visible distinction between
the two states, that the variable `result` can be in.
