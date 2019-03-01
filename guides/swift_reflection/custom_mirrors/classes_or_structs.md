[frontMatter]
title = "Classes or Structs"
tags = []
created = "2019-03-01 11:47:01"
description = ""
published = false

---

# Classes or Structs

The second can be used for a `class` or a `struct`.

``` Swift
public init<T>(_ subject: T, 
  children: DictionaryLiteral<String, Any>, 
  displayStyle: Mirror.DisplayStyle? = default, 
  ancestorRepresentation: Mirror.AncestorRepresentation = default)
```

Interesting to note, here, is that you provide the children (i.e.
properties) of your subject as a `DictionaryLiteral` which is a bit like
a dictionary only that it can be used directly as function parameters.
If we implement this for our `Bookmark struct`, it looks like this:

``` Swift
extension Bookmark: CustomReflectable {
    func customMirror() -> Mirror {
        let children = DictionaryLiteral<String, Any>(dictionaryLiteral: 
        ("title", self.title), ("pagerank", self.pagerank), 
        ("url", self.url), ("created", self.created), 
        ("keywords", self.keywords), ("group", self.group))

        return Mirror.init(Bookmark.self, children: children, 
            displayStyle: Mirror.DisplayStyle.Struct, 
            ancestorRepresentation:.Suppressed)
    }
}
```
