[frontMatter]
title = "Introduction"
tags = []
created = "2019-02-15 20:40:47"
description = ""
published = false

---

# Introduction

Among the new features that Swift offers to Objective-C programmers is
one that disguises itself like a boring old man while it offers huge
potential for forming elegant solutions to otherwise unwieldy sets of
nested branches. I\'m, of course talking about the `switch` statement
that many Objective-C programmers probably consider as a clunky syntax
device which is most entertaining when used as [Duff\'s
Device](http://en.wikipedia.org/wiki/Duff's_device), yet usually offers
little to no advantages over multiple if statements.

The `Switch` statement in Swift can do much more though. In the
following tutorial, I will try to explain the various usages for these
new features in more detail. I\'ll mostly ignore those solutions where
there\'s no benefit over how `switch` works in Objective-C or C. The
basics of this post were actually written in July 2014, but so many of
my patterns crashed the compiler back then that I postponed writing it
until there\'s better support.

# Diving In

The main feature of `switch` is of course pattern matching, the ability
to destructure values and match different switch cases based on correct
match of the values to the cases.

``` Swift
// Example of the worst binary -> decimal converter in history
let bool1 = 1
let bool2 = 0
switch (bool1, bool2) {
   case (0, 0): print("0")
   case (0, 1): print("1")
   case (1, 0): print("2")
   case (1, 1): print("3")
}
```

Pattern matching has long existed in other languages like Haskell,
Erlang, Scala, or Prolog. This is a boon, because it allows us to have a
look at how those languages utilize pattern matching in order to solve
their problems. We can even have a look at their examples to find the
most practical ones that offer real world adaptability.
