[frontMatter]
title = "Method-Only Types"
tags = ["box", "associated"]
created = "2019-03-01 11:01:50"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Method-Only Types

If your `associated type` requirement doesn\'t come from `Equatable`
conformance but instead from your own use, you can double-check if you
actually need these associated types.

Take this example of a validator type:

``` Swift
protocol Validator {
    associatedtype I
    func validate(_ input: I) -> Bool
}
```

As the `associated type` is only used in one method, you can
alternatively just make it a `generic` method and thus save yourself
from introducing unnecessary unfinished types:

``` Swift
protocol Validator {
    func validate<I>(_ input: I) -> Bool
}
```
