[frontMatter]
title = "Generic Types"
tags = ["keypath", "root", "value"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Generic Types

We don't always have to spell out the two generic types `Root` and `Value`. We can, for example, write a generic function that works for any object with any property:

``` Swift
func accept<MyRoot, MyValue>(_ object: MyRoot, keyPath: KeyPath<MyRoot, MyValue>) {
  print(object[keyPath: keyPath])
}
```

Here, we introduce the generic types `MyRoot` and `MyValue` specifically for our `accept` function and also use them for our `KeyPath<MyRoot, MyValue>` definition. Now, we can use this function for different keypaths:

``` Swift
accept(user, keyPath: \User.username)
accept("", keyPath: \String.count)
```
