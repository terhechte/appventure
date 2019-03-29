[frontMatter]
title = "PartialKeyPath"
tags = ["keypath", "partialkeypath", "type-erase", "erase"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# PartialKeyPath

`PartialKeyPath` is a type-erased `KeyPath` that erases the `Value` type parameter.

As we've seen in the previous chapter, sometimes you want to have a `KeyPath` that does not require a `Value` type parameter. That is, what the `PartialKeyPath` is for. Its type signature is `PartialKeyPath<Root>`. As you can see, there is no `Value` type anymore. This `KeyPath`, again, is read-only. However, it is very useful because it allows you to be much more flexible when storing keypaths in arrays or writing functions that accept keypaths. Here is a quick example:

``` Swift
/// Value would be `String`
let a: PartialKeyPath<User> = \User.name

/// Value would be `Int`
let b: PartialKeyPath<User> = \User.age

/// Value would be `Address`
let c: PartialKeyPath<User> = \User.address
```

See how these totally different types (`KeyPath<User, String>, KeyPath<User, Int>, ...`) are actually stored with the same type, just `PartialKeyPath<User>`. We type-erase the `Value` parameter.

This is useful because it allows you to call the same function with different types of keypaths:

``` Swift
func acceptKeyPath(_ keyPath: PartialKeyPath<User>) {
  ...
}
acceptKeyPath(\User.age)
acceptKeyPath(\User.username)
```

More importantly, it allows us to solve the issue we had with the `DebugPrinter` in the [previous code](javascript:prev()). We can now implement is as follows:

``` Swift
/// Dynamically define a debug description for an object
class DebugPrinter<T> where T: AnyObject {
    var keyPaths: [(String?, PartialKeyPath<T>)] = []
    let reference: T
    let prefix: String

    init(_ prefixString: String, for instance: T) {
        reference = instance
        prefix = prefixString
    }

    func addLog(_ path: PartialKeyPath<T>, prefix: String? = nil) {
        keyPaths.append((prefix, path))
    }

    func log() {
        print(prefix, terminator: ": ")
        for entry in keyPaths {
          if let prefix = entry.0 { print(prefix, terminator: "") }
          print(reference[keyPath: entry.1], terminator: ", ")
        }
    }
}
```

Just by replacing `KeyPath<T, String>` with `PartialKeyPath<T>` we could fix the issue with this code, and now it can be used with all types.

Now, you're probably wondering whether there is a `KeyPath` type that also type-erases the `Root` type parameter, and in fact, there is! Next up, the appropriately named `AnyKeyPath`.
