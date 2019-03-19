[frontMatter]
title = "Language Support"
tags = ["pattern matching", "switch"]
created = "2019-02-15 20:40:47"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Patterns with other Keywords

The Swift documentation points out, that not all patterns can be used
with the `if`, `for` or the `guard` statement. However, the docs seem to
be outdated. All 7 patterns work for all three keywords.

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
```

With this in mind, we will have a short look at each of those keywords
in detail.
