[frontMatter]
title = "AnyKeyPath"
tags = ["keypath", "anykeypath", "root", "type-erase", "erase"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# AnyKeyPath

The last `KeyPath` type that we have to tackle is the `AnyKeyPath`. It doesn't have a type-parameter for either `Root` or `Value` as it is completely type-erased. If you read the chapter to `PartialKeyPath`, you will easily grep this one as well. This type is really useful once you intend to write code that just stores general keypaths from differently typed objects. Here is a small bit of example code:

``` Swift
let keyPaths: [AnyKeyPath] = [
  \User.username,
  \String.count,
  \Presentation.title
]
```

We will see more (and better!) usecases for this type later on in this guide, however here is a very simple example of where it could be useful.

You're writing a game and you have different entities / types: Animals, Monsters, Players, and Objects. Each of them have a `health` property (even objects. If you hit a tree long enough, it will break). You need an easy way to debug the health of all entities that are currently on screen. You can just collect them into an array of `AnyKeyPath` and print them out:

``` Swift
func observeHealth(entity: Any, _ keypath: AnyKeyPath) { ... }
observeHealth(entity: monster1, \Dragon.health)
observeHealth(entity: stone255, \Stone.integrity)
observeHealth(entity: player2, \Player.health)
```

This tackles the last one of our keypaths. You might have wondered though, what good are those type-erased keypaths given that you can't modify properties. After all they're all read-only! Not necessarily, because Swift allows you to type-cast them at runtime.
