[frontMatter]
title = "KeyPath"
tags = ["keypath", "readonly"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

## KeyPath<Root, Value>

We've seen this `KeyPath` before. What we did not really talk about yet is that this `KeyPath` is **read only**. You can't use it to modify properties, only to read properties. They're automatically used for accessing immutable properties or instances. Here're a couple of examples of these read-only keypaths:

``` Swift
struct ImmutableUser {
  // `let` properties are immutable
  let username: String
}
var firstUser = ImmutableUser(username: "Shinji")

// This will fail
firstUser[keyPath: \ImmutableUser.username] = "Ikari"

// Prints: KeyPath<ImmutableUser, String>
print(type(of: \ImmutableUser.username))
```

In this example, we could not edit the `firstUser`, because the `username` property was a `let` it was immutable. Just like `firstUser.username = "Ikari"` also would not have worked.

``` Swift
struct MutableUser {
  var username: String
}
var firstUser = MutableUser(username: "Shinji")

// This will work fine
firstUser[keyPath: \MutableUser.username] = "Ikari"
```

Here, it works fine, because 
- `firstUser` is a `var` type
- `MutableUser.username` is a `var` type

So, if `KeyPath` is read-only and in this second example we could actually write to `firstUser`, then what is the type of `\MutableUser.username` here?
