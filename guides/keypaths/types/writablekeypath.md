[frontMatter]
title = "WritableKeyPath"
tags = ["keypath", "writablekeypath"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# WritableKeyPath<Root, Value>

In the example above, our type was a `WritableKeyPath`. WritableKeyPaths are, as the name implies, keypaths that allow you to write information. They're formed for `var` properties on `var` instances.

``` Swift
struct MutableUser {
  var username: String
}
var firstUser = MutableUser(username: "Shinji")

firstUser[keyPath: \MutableUser.username] = "Ikari"
```

If you want to have a keypath argument to a function that allows mutating the contents, `WritableKeyPath` is a good choice:

``` Swift
func modify(user: User, keyPath: WritableKeyPath<User, String>) {
  user[keyPath: keyPath] = "Hello World"
}
```

There's another variant of the `WritableKeyPath`, which we will introduce next.
