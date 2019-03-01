[frontMatter]
title = "Iteration"
tags = []
created = "2019-03-01 17:35:30"
description = ""
published = false

---

# Iteration

In the above descriptions, I\'ve tried to steer clear of calling tuples
sequences or collections because they aren\'t. Since every element of a
tuple can have a different type, there\'s no type-safe way of looping or
mapping over the contents of a tuple. Well, no beautiful one, that is.

Swift does offer limited reflection capabilities, and these allow us to
inspect the elements of a tuple and loop over them. The downside is that
the type checker has no way to figure out what the type of each element
is, and thus everything is typed as `Any`. It is your job then to cast
and match this against your possible types to figure out what to do.

``` Swift
let t = (a: 5, b: "String", c: Date())

let mirror = Mirror(reflecting: t)
for (label, value) in mirror.children {
    switch value {
    case is Int:
        print("int")
    case is String:
        print("string")
    case is NSDate:
        print("nsdate")
    default: ()
    }
}
```

This is not as simple as array iteration, but it does work if you really
need it.
