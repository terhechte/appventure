[frontMatter]
title = "Collections"
tags = ["reflection"]
created = "2019-03-01 11:47:01"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Collections

In order to 

The first special `init` is tailor-made for collections:

``` Swift
init<Subject, C>(_ subject: Subject, children: C, displayStyle: Mirror.DisplayStyle? = nil, ancestorRepresentation: Mirror.AncestorRepresentation = .generated) where C : Collection, C.Element == Mirror.Child
```

Compared to the `init(reflecting:)` initializer above, this one allows
us to define much more details about the reflection process.

-   It only works for collections
-   We can set the subject to be reflected **and** the children of the
    subject (the collection contents)
