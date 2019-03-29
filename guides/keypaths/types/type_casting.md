[frontMatter]
title = "Type-Casting KeyPaths"
tags = ["keypath", "type", "casting", "type-casting", "as", "anykeypath", "partialkeypath"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Type-Casting KeyPaths

As we've seen before, Swift offers `PartialKeyPath<Root>` and `AnyKeyPath` as a way to generalize `KeyPath` handling. While this makes it easier to store these keypaths in generic functions and arrays, it makes it much harder to actually use them. There's not much we can do with them - except for printing maybe - which is why most of our usage examples were about printing. 

Type-casting changes this. It allows you to cast a type-erased `KeyPath` back into (for example) a `WritableKeyPath` in a totally type-safe manner. Observe the magic:

``` Swift
let keyPath: AnyKeyPath = \User.username
var user = User(username: "Hello")

if let writableUsername = keyPath as? WritableKeyPath<User, String> {
   user[keyPath: writableUsername] = "World"
}
```

In this example, you saw how we converted an `AnyKeyPath` back into a `WritableKeyPath<User, String>`. The important part is that `as?` returns on optional. So if the `KeyPath` is not of type `<User, String>` nothing would happen as the expression would return `nil`. Therefore, in order to work with multiple types (`String`, `Int`, `Float`, etc), you need more than one `if` statement. Preferrably a [`switch`](lnk::switch) statement.

In this example, we're using `switch` to identify the specific type of the `keyPath` and then perform a different operation depending on the type.

``` Swift
let keyPath: AnyKeyPath = \User.username
switch keyPath {
case let a as KeyPath<Yeah, String>:
    print("String" + xxx[keyPath: a])
case let a as KeyPath<Yeah, Int>:
    print(1 + xxx[keyPath: a])
default:
    print("Unknown keypath type")
}
```
