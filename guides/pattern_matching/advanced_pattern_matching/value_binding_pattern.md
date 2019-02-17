[frontMatter]
title = "Value-Binding Pattern"
tags = []
created = "2019-02-15 20:40:47"
description = ""
published = false

---

# Value-Binding Pattern

This is the very same as binding values to variables via `let` or `var`.
Only in a switch statement. You\'ve already seen this before, so I\'ll
provide a very short example:

``` Swift
switch (4, 5) {
  case let (x, y): print("\(x) \(y)")
}
```
