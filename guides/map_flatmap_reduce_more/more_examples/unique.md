[frontMatter]
title = "Unique"
tags = ["reduce", "unique"]
created = "2019-02-20 19:49:10"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Unique

Return a list with all duplicates removed. The better solution would be
to use a `Set`.

``` Swift
[1, 2, 5, 1, 7].reduce([], { (a: [Int], b: Int) -> [Int] in
  if a.contains(b) {
    return a
  } else {
    return a + [b]
  }
})
// prints: 1, 2, 5, 7
```
