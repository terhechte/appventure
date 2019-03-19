[frontMatter]
title = "Stringly Typed Code"
tags = []
created = "2019-03-01 16:31:41"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Stringly Typed Code

In bigger Xcode projects, you\'re quickly accumulating lots of resources
which are accessed by string. We\'ve already mentioned reuse identifiers
and storyboard identifiers above, but there\'s also: Images, Segues,
Nibs, Fonts, and other resources. Oftentimes, those resources can be
grouped into several distinct sets. If that\'s the case, a `String`
typed `enum` is a good way of having the compiler check this for you.

``` Swift
enum DetailViewImages: String {
  case background = "bg1.png"
  case sidebar = "sbg.png"
  case actionButton1 = "btn1_1.png"
  case actionButton2 = "btn2_1.png"
}
```

For iOS users, [there\'s also R.swift which auto generates `structs` for
most of those use cases.](https://github.com/mac-cain13/R.swift)
Sometimes you may need more control though (or you may be on a Mac [^8])
