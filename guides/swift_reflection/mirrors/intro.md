[frontMatter]
title = "Mirrors"
tags = []
created = "2019-03-01 11:47:01"
description = ""
published = false

---

# Mirrors

Swift\'s reflection capabilities are based around a `struct` called
**Mirror**. You create a mirror for a particular `subject` and the
mirror will then let you query it.

Before we do that, let\'s define a simple data structure that we can use
as our subject.

``` Swift
import Foundation.NSURL

public class Store {
    let storesToDisk: Bool = true
}
public class BookmarkStore: Store {
    let itemCount: Int = 10
}
public struct Bookmark {
   enum Group {
      case Tech
      case News
   }
   private let store = {
       return BookmarkStore()
   }()
   let title: String?
   let url: NSURL
   let keywords: [String]
   let group: Group
}

let aBookmark = Bookmark(title: "Appventure", url: NSURL(string: "appventure.me")!, keywords: ["Swift", "iOS", "OSX"], group: .Tech)
```
