[frontMatter]
title = "Creating and Accessing Tuples"
tags = []
created = "2019-03-01 17:35:30"
description = ""
published = false

---

# Creating and Accessing Tuples

``` Swift
// Constructing a simple tuple
let tp1 = (2, 3)
let tp2 = (2, 3, 4)

// Constructing a named tuple
let tp3 = (x: 5, y: 3)

// Different types
let tp4 = (name: "Carl", age: 78, pets: ["Bonny", "Houdon", "Miki"])

// Accessing tuple elements
let tp5 = (13, 21)
tp5.0 // 13
tp5.1 // 21

let tp6 = (x: 21, y: 33)
tp6.x // 21
tp6.y // 33

```
