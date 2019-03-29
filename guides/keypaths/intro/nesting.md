[frontMatter]
title = "Nesting"
tags = ["keypath", "nesting"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Nesting

Obviously, you can also nest KeyPaths. Now, our `User` also has an `address`:

``` Swift
struct Address {
  var street: String
}

struct User {
  var username: String
  var address: Address
}
```

If we want to create a keypath to the amount of characters of the `street` of the user's address, we can simply do that like this:

``` Swift
let keyPath: KeyPath<User, Int> = \User.address.street.count
```

As you can see, this is a `KeyPath` from `User` to `Int` because it points from the `User` to his address' street' count. `count`, finally, is a `Int` type.
