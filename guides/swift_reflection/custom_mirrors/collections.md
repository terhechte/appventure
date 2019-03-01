[frontMatter]
title = "Collections"
tags = []
created = "2019-03-01 11:47:01"
description = ""
published = false

---

# Collections

The first special `init` is tailor-made for collections:

``` Swift
public init<T, C : CollectionType where C.Generator.Element == Child>
  (_ subject: T, children: C, 
   displayStyle: Mirror.DisplayStyle? = default, 
   ancestorRepresentation: Mirror.AncestorRepresentation = default)
```

Compared to the `init(reflecting:)` initializer above, this one allows
us to define much more details about the reflection process.

-   It only works for collections
-   We can set the subject to be reflected **and** the children of the
    subject (the collection contents)
