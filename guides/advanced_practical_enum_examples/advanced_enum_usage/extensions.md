[frontMatter]
title = "Extensions"
tags = ["enum", "extension"]
created = "2019-03-01 16:29:51"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Extensions

Take the following `enum`:

``` Swift
enum Entity {
    case soldier(x: Int, y: Int)
    case tank(x: Int, y: Int)
    case player(x: Int, y: Int)
}
```

As we just saw, enums can also be extended. There're two use cases for this.
You've already seen the first one: Conforming to a `protocol`.

``` Swift
extension Entity: CustomStringConvertible {
  var description: String {
    switch self {
    case let .soldier(x, y): return "\(x), \(y)"
    case let .tank(x, y): return "\(x), \(y)"
    case let .player(x, y): return "\(x), \(y)"
    }
  }
}
```

The other use case
is keeping `enum cases` and `methods` separate, so that a
reader of your code can easily digest the `enum` and afterwards 
read the methods.

``` Swift
extension Entity {
   mutating func move(dist: CGVector) {}
   mutating func attack() {}
}
```

## Extending 

Extensions also allow you to add useful code to existing `enum` types. Either from the Swift standard library, or from third party frameworks, or from yourself if you happen to have a big codebase.

For example, we can extend the standard library `Optional` type in order to add useful extensions. If you'd like to learn more about this, [we have an article that explains this in more detail.](lnk::optional)

``` Swift
extension Optional {
    /// Returns true if the optional is empty
    var isNone: Bool {
        return self == .none
    }
}
```

Another example would be addign a convenience extension to one of your own `enum` types that is `fileprivate` so that you'd use it only within a specific file:

``` Swift
fileprivate extension Entity {
  mutating func replace(to: Entity) {
    self = entity
  }
}
```

Here, we have an extension to your `Entity` that allows to replace it with a different entity. This would only be used deep within your game engine which is why the scope is limited to one file.
