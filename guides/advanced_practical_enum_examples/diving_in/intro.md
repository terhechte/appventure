[frontMatter]
title = "Diving In: Basic Enums"
tags = ["enum"]
created = "2019-03-01 16:29:51"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Diving In

A short overview of how to define and use enums.

We\'re working on a game, and the player can move in four directions. So
our player movement is restricted. He can only go right or left. You could model
that in the following manner:

``` Swift
if movement == "left" { ... }
else if movement == "right" { ...}
```

However this is dangerous, what if we have a typo in our code and
`movement` is neither `left` nor `right` but `leeft`?. Wouldn't it be cool
if the compiler would point out if we have a typo like that? You could just write:

``` Swift
let moveLeft = 0
let moveRight = 1
if movement == moveLeft { ... }
else if movement == moveRight { ... }
```

This would solve our problem of typos in the code, but if we had more movements,
it would be an easy bug to forget to handle all the movements. Imagine somebody
extends the code in a couple of months and adds two new movements:

``` Swift
let moveUp = 0
let moveDown = 1
```

This developer forgets to update the `if` logic, though, so now we have more
movements but we forgot to handle them. Wouldn't it be great if the compiler would
tell us if we forgot to handle all the cases of our movements? That's what the `enum`
type is for:

## Defining Basic Enums

`Enum`s tell Swift that a particular set of `cases` belong together. Our movement
`enum` could look like this:

``` Swift
enum Movement {
case left
case right
}
```

It is considered proper style in Swift to always use lowercase for the enum `case` name

Swift's [switch](apv::switch) allows you to handle all the states of an `enum`:

``` Swift
let myMovement = Movement.left
switch myMovement {
  case Movement.left: player.goLeft()
  case Movement.right: player.goRight()
}
```

If we would add another `case` (such as `up`), then the compiler would complain.

There's also a really nice shortcut in Swift. Since the compiler knows that `myMovement` is
of type `Movement` you don't have to write that out explicitly. This also works:

``` Swift
switch myMovement {
  case .left: player.goLeft()
  case .right: player.goRight()
}
```

It is considered good style to not write out the `enum` name. Theyre may be situations where you have to do it in order to please the Compiler though.

## Handling Enums

Besides the `switch` statement above, Swift also offers many more ways of handling `enum` types. Many of which can be found in our [Pattern Matching Guide](apv::switch), some of the will also be handled in this guide on `enum`.
