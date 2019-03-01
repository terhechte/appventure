[frontMatter]
title = "Observer Pattern"
tags = []
created = "2019-03-01 16:31:41"
description = ""
published = false

---

# Observer Pattern

There\'re various ways of modelling observation in Swift. If you include
`@objc` compatibility, you can use `NSNotificationCenter` or **KVO**.
Even if not, the `didSet` syntax makes it easy to implement simple
observation. Enums can be used here in order to make the type of change
that happens to the observed object clearer. Imagine collection
observation. If we think about it, we only have a couple of possible
cases: One or more items are inserted, one or more items are deleted,
one or more items are updated. This sounds like a job for an enum:

``` Swift
enum Change {
     case Insertion(items: [Item])
     case Deletion(items: [Item])
     case Update(items: [Item])
}
```

Then, the observing object can receive the concrete information of what
happened in a very clean way. This could easily be extended by adding
**oldValue** and **newValue**, too.
