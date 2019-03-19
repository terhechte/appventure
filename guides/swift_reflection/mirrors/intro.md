[frontMatter]
title = "Mirrors"
tags = ["reflection", "mirror"]
created = "2019-03-01 11:47:01"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Mirrors

Swift\'s reflection capabilities are based around a `struct` called
**Mirror**. You create a mirror for a particular `subject` and the
mirror will then let you query it.

Before we look at the API, let\'s define a simple data structure that we can experiment on.

``` Swift
import Foundation

public class Store {
    let storesToDisk: Bool = true
}
public class BookmarkStore: Store {
    let itemCount: Int = 10
}
public struct Bookmark {
   enum Group {
      case tech
      case news
   }
   private let store = {
       return BookmarkStore()
   }()
   let title: String?
   let url: URL
   let keywords: [String]
   let group: Group
}

let aBookmark = Bookmark(title: "Appventure", url: URL(string: "appventure.me")!, keywords: ["Swift", "iOS", "OSX"], group: .tech)
```

So, we have a `Bookmark`. Bookmarks can have titles, urls, keywords, and bookmarks can belong to a `Group`. There is also a `BookmarkStore` and a more general `Store`. So, how do we query this data structure at runtime?

