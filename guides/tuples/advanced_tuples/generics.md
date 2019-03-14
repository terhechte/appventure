[frontMatter]
title = "Generics"
tags = ["tuples", "generics", "typealias", "either"]
created = "2019-03-01 17:35:30"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Generics

There\'s no `Tuple` type available in Swift. If you wonder why that is,
think about it: every tuple is a totally different type, depending on
the types within it. So instead of defining a generic tuple requirement,
you define the specific but generic incarnation of the tuple you intend
to use:

``` Swift
func wantsTuple<T1, T2>(_ tuple: (T1, T2)) -> T1 {
    return tuple.0
}

wantsTuple(("a", "b")) // "a"
wantsTuple((1, 2)) // 1
```

You can also use tuples in `typealiases`, thus allowing subclasses to
fill out your types with details. This looks fairly useless and
complicated, but I\'ve already had a use case where I need to do exactly
this.

``` Swift
class BaseClass<A,B> {
    typealias Element = (A, B)
    func add(_ elm: Element) {
        print(elm)
    }
}

class IntegerClass<B> : BaseClass<Int, B> {
}

let example = IntegerClass<String>()
example.add((5, ""))
// Prints (5, "")
```

You can also define a `typealias` with generic parameters
like in this example where we introduce a custom `Either` type:

``` Swift
typealias MyEither<A, B> = (left: A, right: B)
```
