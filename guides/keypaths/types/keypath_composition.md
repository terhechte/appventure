[frontMatter]
title = "KeyPath Composition"
tags = ["keypath", "composition"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# KeyPath Composition

The last keypath concept that we should tackle is keypath composition: Swift allows you to dynamically combine `KeyPath` types at runtime if the types match up. 

In order to showcase this, we will go back to our `User` and `Address` struct:

``` Swift
struct User {
  let address: Address
}

struct Address {
  let street: String
}
```

### Example

Based on this structure, we will take two different keypaths; first, one to the `address` property on the `User`, and then one on the `String` property on the `Address`:

``` Swift
let addressKeyPath = \User.address

let streetKeyPath = \Address.street
```

Given these two variables, we can now compose them to manifest a new keypath at runtime that goes from `User` to the `street`:

``` Swift
let newKeyPath = addressKeyPath.appending(path: streetKeyPath)
```

Here, we created a new `KeyPath<User, String>` at runtime by joining a `KeyPath<User, Address>` and a `KeyPath<Address, String>`. However, what should Swift do if you try to merge a `KeyPath<User, String>` and a `KeyPath<House, Int>`. Obviously, there's no relationship between these types. Swift solves this by introducing laws of keypath composition. Lets have a look at them.

