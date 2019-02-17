[frontMatter]
title = "Language Support"
tags = []
created = "2019-02-15 20:40:47"
description = ""
published = false

---

# Patterns with other Keywords

The Swift documentation points out, that not all patterns can be used
with the `if`, `for` or the `guard` statement. However, the docs seem to
be outdated. All 7 patterns work for all three keywords.

For those interested, I compiled an example Gist that has an example for
each pattern for each keyword.

[You can see the example patterns
here.](https://gist.github.com/terhechte/6eaeb90276bbfcd1ea41)

As a shorter example, see the **Value Binding**, **Tuple**, and **Type
Casting** pattern used for all three keywords in one example:

``` Swift
// This is just a collection of keywords that compiles. This code makes no sense
func valueTupleType(a: (Int, Any)) -> Bool {
    // guard case Example
    guard case let (x, _ as String) = a else { return false}
    print(x)

    // for case example
    for case let (a, _ as String) in [a] {
        print(a)
    }

    // if case example
    if case let (x, _ as String) = a {
       print("if", x)
    }

    // switch case example
    switch a {
    case let (a, _ as String):
        print(a)
        return true
    default: return false
    }
}
let u: Any = "a"
let b: Any = 5
print(valueTupleType((5, u)))
print(valueTupleType((5, b)))
// 5, 5, "if 5", 5, true, false
```

With this in mind, we will have a short look at each of those keywords
in detail.
