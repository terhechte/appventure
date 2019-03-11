[frontMatter]
title = "Equatable"
tags = ["box", "associated", "protocol", "equatable"]
created = "2019-03-01 11:01:50"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Make Your Types Equatable

The first solution for the archetypical problem is also a really simple
one. Instead of enforcing `Equatable` on your custom `protocol`, you can
simply require your full fledged, final, types to conform to the
`Equatable` protocol instead of your custom protocol. Consider the
previously defined `Bookmarkable` protocol:

``` Swift
protocol Bookmarkable {
}

struct Bookmark: Bookmarkable, Equatable {
  var identifier: Int
}

func ==(lhs: Bookmark, rhs: Bookmark) -> Bool {
  return lhs.identifier == rhs.identifier
}

var myBookmarks: [Bookmark] = []
```

In the example above, the `Equatable` requirement actually stems from
the `Bookmark` type conforming to the `Equatable` protocol, not the
`Bookmarkable` protocol itself. The actual `Equatable` information,
however, lies in the new `identifier` property, which has been added to
the `Bookmark` `struct`. As you can easily see, this also requires you
to make the `myBookmarks` array require only elements of type
`Bookmark`. A serious disgression if you\'re used to using protocols
like partially anonymous types. A better solution, if your design allows
for it, goes one step further by enforcing the new `property` which we
introduced in this example.

## Equatable Properties

Here, the idea is that we take one of the types that already implement
`Equatable` in a proper way (i.e. `Int`, `String`, ...) and add a new
`property` requirement to our `Bookmarkable` protocol. Then, we can use
this `property` to add `Equatable` support without actually implementing
`Equatable`:

``` Swift
protocol Bookmarkable {
    var identifier: Int { get }
}

struct Bookmark: Bookmarkable {
    var identifier: Int
}

var myBookmarks: [Bookmarkable] = []
```

The main change, compared to the code above, is that the
`var identifier` moved to the `Bookmarkable` protocol and that we
removed the `func ==`.

While this works better, it still has a major deficit. Since
`Bookmarkable` does not directly comply with `Equatable`, you will not
gain the standard library\'s methods that specifically deal with
`Equatable` types. So instead of being able to call `Array.contains`
like this:

``` Swift
let ourBookmark = Bookmark(identifier: 0)
let result = myBookmarks.contains(ourBookmark)
```

You will have to use the more verbose closure-based version:

``` Swift
let ourBookmark = Bookmark(identifier: 0)

let result = myBookmarks.contains { (bookmark) -> Bool in
    return bookmark.identifier == ourBookmark.identifier
}
```
