[frontMatter]
title = "Associated Types Trouble"
tags = ["box", "associated", "protocol"]
created = "2019-03-01 11:01:50"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Associated Types Trouble

The classic example of `associated types` trouble certainly is the
following Swift error message:

``` bash
protocol 'Bookmarkable' can only be used as a generic constraint because it has Self 
or associated type requirements
var bookmarks: [Bookmarkable]
```

This happens once your type conforms to a protocol which conforms to
`Equatable`:

``` Swift
protocol Bookmarkable: Equatable {
}

struct User {
    var bookmarks: [Bookmarkable]
}
```

Here, the problem is that `Equatable` contains a method `==` which has
two paramters of type `Self`. Protocol Methods with `Self` parameters
automatically opt in to `associated types`.

Let's investigate several patterns that allow
you to work your way around the `associated type` requirement or that
show how such a type can be handled.
