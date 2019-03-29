[frontMatter]
title = "Erase Types"
tags = ["keypath", "partialkeypath", "anykeypath", "erase", "type-erase"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# 1. Erase Types

We already saw this, but it is worth mentioning again. One reason why keypaths are so useful is because there're type-erased variants. As we saw in our practical example, the ability to temporarily go to `AnyKeyPath` offers many more opportunities. So, always remember these types:

``` Swift
KeyPath<A, B> = \User.age
PartialKeyPath<A> = \User.age
AnyKeyPath = \User.age
```
