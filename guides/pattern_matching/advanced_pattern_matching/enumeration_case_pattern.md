[frontMatter]
title = "Enumeration Case Pattern"
tags = []
created = "2019-02-15 20:40:47"
description = ""
published = false

---

# Enumeration Case Pattern

As you saw in our trading example, pattern matching works **really
great** with Swift\'s `enums`. That\'s because `enum cases` are like
sealed, immutable, destructable structs. Much like with `tuples`, you
can unwrap the contents of an individual case right in the match and
only extract the information you need [^2].

Imagine you\'re writing a game in a functional style and you have a
couple of entities that you need to define. You could use `structs` but
as your entities will have very little state, you feel that that\'s a
bit of an overkill.

``` Swift
enum Entities {
    case Soldier(x: Int, y: Int)
    case Tank(x: Int, y: Int)
    case Player(x: Int, y: Int)
}
```

Now you need to implement the drawing loop. Here, we only need the X and
Y position:

``` Swift
for e in entities() {
    switch e {
    case let .Soldier(x, y):
      drawImage("soldier.png", x, y)
    case let .Tank(x, y):
      drawImage("tank.png", x, y)
    case let .Player(x, y):
      drawImage("player.png", x, y)
    }
}
```
