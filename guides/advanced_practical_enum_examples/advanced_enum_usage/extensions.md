[frontMatter]
title = "Extensions"
tags = []
created = "2019-03-01 16:29:51"
description = ""
published = false

---

# Extensions

As we just saw, enums can also be extended. The most apparent use case
for this is keeping `enum cases` and `methods` separate, so that a
reader of your code can easily digest the `enum` and after that move on
to the methods:

``` Swift
enum Entities {
    case Soldier(x: Int, y: Int)
    case Tank(x: Int, y: Int)
    case Player(x: Int, y: Int)
}
```

Now, we can extend this `enum` with methods:

``` Swift
extension Entities {
   mutating func move(dist: CGVector) {}
   mutating func attack() {}
}
```

You can also write extensions to add support for a specific protocol:

``` Swift
extension Entities: CustomStringConvertible {
  var description: String {
    switch self {
       case let .Soldier(x, y): return "\(x), \(y)"
       case let .Tank(x, y): return "\(x), \(y)"
       case let .Player(x, y): return "\(x), \(y)"
    }
  }
}
```
