[frontMatter]
title = "Associated Types and Self"
tags = ["box", "associated", "self"]
created = "2019-03-01 11:01:50"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Associated Types and Self

Another vector which can introduce `associated types` into your codebase
is the usage of `Self`:

``` Swift
protocol Example {
  /// Indirect Associated Type
  var builder: Self { get }
  /// Indirect Associated Type
  func makeSomething(with example: Self)
}
var myExamples: [Example] = []
```

As you can see in the example above, using `Self` as a method parameter
or using `Self` as a property type automatically introduces an
`associated type` (like we saw with `Equatable`, earlier).

The most helpful note here is that once you use a `method` instead of a
`property` in order to return something of type `Self` you will not opt
in to an `associated type`:

``` Swift
protocol Example {
  /// No Indirect Associated Type
  func builder() -> Self
}
var myExamples: [Example] = []
```

This example works fine. No `indirect associated` type is introduced.
