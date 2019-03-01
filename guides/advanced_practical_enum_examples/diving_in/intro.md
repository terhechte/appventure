[frontMatter]
title = "Diving In: Basic Enums"
tags = []
created = "2019-03-01 16:29:51"
description = ""
published = false

---

# Diving In

A short overview of how to define and use enums.

## Defining Basic Enums

We\'re working on a game, and the player can move in four directions. So
our player movement is restricted. Obviously, we can use an enum for
that.

``` Swift
enum Movement {
case Left
case Right
case Top
case Bottom
}
```

You can then use [various pattern matching
constructs](http://appventure.me/2015/08/20/swift-pattern-matching-in-detail/)
to retrieve the value of a `Movement`, or act upon a specific case:

``` Swift
let aMovement = Movement.Left

switch aMovement {
case .Left: print("left")
default: ()
}

if case .Left = aMovement { print("left") }

if aMovement == .Left { print("left") }
```

Note that you don\'t have to specify the actual name of the `enum` (i.e.
`case Movement.Left: print("Left")` in this case. The type checker
figures that out automatically. This is extremely helpful for some of
those convoluted **UIKit** or **AppKit** enums.
