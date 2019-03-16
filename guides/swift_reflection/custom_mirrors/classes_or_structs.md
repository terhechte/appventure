[frontMatter]
title = "Classes or Structs"
tags = ["reflection", "mirror"]
created = "2019-03-01 11:47:01"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Classes or Structs

The second can be used for a `class` or a `struct`.

``` Swift
init<Subject>(_ subject: Subject, children: KeyValuePairs<String, Any>, displayStyle: Mirror.DisplayStyle? = nil, ancestorRepresentation: Mirror.AncestorRepresentation = .generated)
```

Interesting to note, here, is that you provide the children (i.e.
properties) of your subject as a `KeyValuePairs<String, Any>` which is a bit like
a dictionary only that it can be used directly as function parameters.
