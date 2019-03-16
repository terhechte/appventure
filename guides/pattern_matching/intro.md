[frontMatter]
title = "Introduction"
tags = ["pattern matching", "switch", "destructure", "enum"]
created = "2019-02-15 20:40:47"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Introduction

Swift's `switch` statement bears little resemblance to the similarly named
equivalent in C or Objective-C. Even though they share the same name,
the Swift version can do much, much more.

In the
following guide, I will try to explain the various usages for these
new features in more detail. 

The main feature of `switch` is, of course, pattern matching: the ability
to destructure values and match different switch cases based on correct
match of the values to the cases.

## Destructure

Destructuring means to take something of a certain structure and destructure it
into smaller items again. Imagaine you had a `apv::tuple` variable `user` with the following value: `(firstname: "Harry", lastname: "Potter", age: 21, occupation: "Wizard")`

Destructuring means taking this tuple and converting it into individual variables:

``` Swift
let harry = (firstname: "Harry", lastname: "Potter", age: 21, occupation: "Wizard")

let (name, surname, age, occupation) = harry
print(surname)
```

Destructuring is a great method for handling the information in complex types. It is also a fundamental part of Swift's `switch` statement. The next step, then, is to have a look at `switch`:

## A simple example

We wrote a game where both players have to take a quiz. After each question we evaluate
who won or lost. There're four states: 

- Player 1 is correct
- Player 2 is correct
- Both were correct
- Both were wrong

We can model this logic very nicely with a `switch` statement such as the following:

``` Swift
let player1 = true
let player2 = false
switch (player1, player2) {
   case (true, false): print("Player 1 won")
   case (false, true): print("Player 2 won")
   case (true, true): print("Draw, both won")
   case (false, false): print("Draw, both lost")
}
```

Here, we create a tuple `(player1, player2)` and then match each of
the possible cases.

This was a very short introduction, now we will go into more detail.
