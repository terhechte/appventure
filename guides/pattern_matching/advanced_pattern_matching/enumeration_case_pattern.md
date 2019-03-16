[frontMatter]
title = "Enumeration Case Pattern"
tags = ["pattern matching", "switch", "enum"]
created = "2019-02-15 20:40:47"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Enumeration Case Pattern

As you saw in our trading example, pattern matching works **really
great** with Swift\'s `enums`. That\'s because `enum cases` are like
sealed, immutable, destructable structs. Much like with `tuples`, you
can unwrap the contents of an individual case right in the match and
only extract the information you need.

Imagine you\'re writing a game in a functional style and you have a
couple of entities that you need to define. You could use `structs` but
as your entities will have very little state, you feel that that\'s a
bit of an overkill.

``` Swift
enum Entities {
    case soldier(x: Int, y: Int)
    case tank(x: Int, y: Int)
    case player(x: Int, y: Int)
}
```

Now you need to implement the drawing loop. Here, we only need the X and
Y position:

``` Swift
for e in entities() {
    switch e {
    case let .soldier(x, y):
      drawImage("soldier.png", x, y)
    case let .tank(x, y):
      drawImage("tank.png", x, y)
    case let .player(x, y):
      drawImage("player.png", x, y)
    }
}
```

This is the gist of it. The `enumeration case pattern` is really just
using `enum` cases in the `switch` statement.
