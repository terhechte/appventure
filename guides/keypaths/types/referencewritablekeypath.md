[frontMatter]
title = "ReferenceWritableKeyPath"
tags = ["keypath", "referencewritablekeypath"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# ReferenceWritableKeyPath

In our earlier examples, we always defined `User` `struct` instances. Which meant that the actual instance we instantiated also had to be mutable (`var`):

``` Swift
var firstUser = User(username: String)
firstUser[keyPath: \User.username] = "Ok"
```

If this had be a `let firstUser`, it would not have worked, because `let` instances are immutable. However, if our `User` is a `class` type, we could still mutate it just fine:

``` Swift
class User {
  var username: String = "Nothing"
}
let firstUser = User()
// This works
firstUser[keyPath: \User.username] = "Something"
```

in The example above, the `username` property can still be modified because `User` is a `class`. Swift distinguishes between keypaths for `reference` (class) types and `value` types. Keypaths to reference types are of the type `ReferenceWritableKeyPath<Root, Value>`.

It is important to note that `ReferenceWritableKeyPath`s are subclasses of `WritableKeyPath`, so any function that accepts a `WritableKeyPath` can also accept a `ReferenceWritableKeyPath`.

The next `KeyPath` we want to look at is the `PartialKeyPath`, however, before we do so, we'll briefly look at a simple class to better understand the need for it and to see some of what we've seen so far in action.
