[frontMatter]
title = "Linked Lists"
tags = []
created = "2019-03-01 16:31:41"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Linked Lists

[Airspeed Velocity has a great writeup on how to implement a Linked List
with an `enum`.](http://airspeedvelocity.net/tag/swift/) Most of the
code in his post goes far beyond enums and touches a lot of interesting
topics [^9], but the basis of his linked list looks kinda like this (I
simplified it a bit):

``` Swift
enum List {
    case end
    indirect case node(Int, next: List)
}
```

Each `node case` points to the next case, and by using an `enum` instead
of something else, you don\'t have to use an optional for the `next`
value to signify the termination of the list.

Airspeed Velocity also wrote a great post about the implementation of a
red black tree with indirect Swift enums, so while you\'re already
reading his blog, [you may just as well also read this
one.](http://airspeedvelocity.net/2015/07/22/a-persistent-tree-using-indirect-enums-in-swift/)
