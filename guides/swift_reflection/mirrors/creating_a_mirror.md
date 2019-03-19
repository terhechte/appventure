[frontMatter]
title = "Creating a Mirror"
tags = ["reflection", "mirror"]
created = "2019-03-01 11:47:01"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Creating a Mirror

The easiest way of creating a mirror is the `reflecting` initializer:

``` Swift
public init(reflecting: Any)
```

Lets use it with our `Bookmark` `struct`:

``` Swift
let myMirror = Mirror(reflecting: aBookmark)
print(myMirror)
// prints : Mirror for Bookmark
```

So this creates a `Mirror for Bookmark`. As you can see, the type of the
subject is `Any`. This is the most general type in Swift. Anything under
the Swift Sun is at least of type `Any` [^1]. So this makes the mirror
compatible with `struct`, `class`, `enum`, `Tuple`, `Array`,
`Dictionary`, `Set`, etc.

There are three additional initializers in the Mirror struct, however
those are mostly used for circumstances where you\'d want to provide
your own, custom mirror.

[^1]: In particular, `Any` is an empty protocol and everything implicitly conforms to this protocol
