[frontMatter]
title = "Identifier Pattern"
tags = ["pattern matching", "switch"]
created = "2019-02-15 20:40:47"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Identifier Pattern

Matches a concrete value. This is how things work in Objective-C\'s
`switch` implementation:

Here, we have a special case just for the number 5

``` Swift
let number = 4
switch number {
  case 5: print("it is a 5")
  default: print("it is something else")
}
```


We can also match strings, see our code below to greet people
in their native language.

``` Swift
let language = "Japanese"
switch name {
  case "Japanese": print("おはようございます")
  case "English": print("Hello!")
  case "German": print("Guten Tag")
}
```
