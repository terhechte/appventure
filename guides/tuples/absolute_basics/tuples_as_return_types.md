[frontMatter]
title = "Tuples as Return Types"
tags = []
created = "2019-03-01 17:35:30"
description = ""
published = false

---

# Tuples as Return Types

Probably the next-best tuple use case. Since tuples can be constructed
on the fly, they\'re a great way to easily return multiple values from a
function.

``` Swift
func abc() -> (Int, Int, String) {
    return (3, 5, "Carl")
}
```
