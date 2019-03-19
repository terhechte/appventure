[frontMatter]
title = "Recap"
tags = []
created = "2019-03-01 16:29:51"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Recap

Lets have another look at the explanation we gave at the beginning and see if it became clearer
now.

> Enums declare types with finite sets of possible states and
> accompanying values. With nesting, methods, associated values, and
> pattern matching, however, enums can define any hierarchically
> organized data.

The definition is a lot clearer now. Indeed, if we add associated values
and nesting, an `enum case` is like a closed, simplified `struct`. The
advantage over structs being the ability to encode categorization and
hierachy:

``` Swift
// Struct Example
struct Point { let x: Int, y: Int }
struct Rect { let x: Int, y: Int, width: Int, height: Int }

// Enum Example
enum GeometricEntity {
   case point(x: Int, y: Int)
   case rect(x: Int, y: Int, width: Int, height: Int)
}
```

The addition of methods and static methods allow us to attach
functionality to an `enum` without having to resort to free functions

``` Swift
// C-Like example
enum Trade {
   case buy
   case sell
}
func order(trade: Trade)

// Swift Enum example
enum Trade {
   case buy
   case sell
   func order() {}
}
```
