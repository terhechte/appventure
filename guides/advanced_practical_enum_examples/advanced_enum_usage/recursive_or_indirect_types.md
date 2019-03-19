[frontMatter]
title = "Recursive / Indirect Types"
tags = ["enum", "indirect"]
created = "2019-03-01 16:29:51"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Recursive / Indirect Types

Indirect types allow
you to define enums where the associated value of a `case` is the very
same enum again. 

As an example, consider that you want to define a file
system representations with files and folders containing files. If
**File** and **Folder** were enum cases, then the **Folder** case would
need to have an array of **File** cases as it\'s `associated value`. Since
this is a recursive operation, the compiler has to make special
preparations for it. Quoting from the Swift documentation:

> Enums and cases can be marked indirect, which causes the associated
> value for the enum to be stored indirectly, allowing for recursive
> data structures to be defined.

So to implement our **FileNode** `enum`, we\'d have to write it like
this:

``` Swift
enum FileNode {
  case file(name: String)
  indirect case folder(name: String, files: [FileNode])
}
```

The `indirect` keyword tells the compiler to handle this `enum case`
indirectly. You can also add the keyword for the whole enum. [As an
example imagine mapping a binary
tree](http://airspeedvelocity.net/2015/07/22/a-persistent-tree-using-indirect-enums-in-swift/):

``` Swift
indirect enum Tree<Element: Comparable> {
    case empty
    case node(Tree<Element>,Element,Tree<Element>)
}
```

This is a very powerful feature that allows you to map complex
relationships in a very clean way with an enum.

