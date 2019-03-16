[frontMatter]
title = "Associated Types"
tags = ["associated", "protocol"]
created = "2019-03-01 11:01:50"
description = ""
published = true

[meta]
swift_version = "5.1"
talk = "https://www.youtube.com/watch?v=P_ifSjia9mE"
---

# Associated Types

Swift is a powerful language with a very powerful type system. Among the
features that define said type system are `associated types`. They can
be defined on a `protocol` to allow implementors of the `protocol` to
specialize certain types in a generic way:

``` Swift
protocol Example {
  associatedtype Value
  var value: Value { get }
}
```

In the snippet above, any type that implements the `Example` protocol
has to define the `Value` type. Protocols with `associated types` can be
understood as **unfinished types**. Compared to regular protocols, which
can be used within Swift like normal types, those protocols can only be
used as a generic constraint. This means that once your type requires an
`associated type`, using it suddenly becomes much more complicated.

The example below shows an example of ****finishing**** a type. By
explicitly telling the compiler that the `Value` type is `Int` it is now
able to understand `ImplementExample` fully.

``` Swift
struct ImplementExample: Example {
  typealias Value = Int
}
```

Associated types are useful for a certain kind of problems where
subclassing and composition does allow you to build the right kind of
abstractions. However, this is a seperate
topic. The topic of this article, on the other hand, is what to do when
you end up with associated types trouble.
