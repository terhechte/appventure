[frontMatter]
title = "Practical Example"
tags = []
created = "2019-03-01 11:47:01"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Structs to Core Data

Imagine we\'re working at the newest, hot, tech startup: **Books
Bunny**. We offer an Artificial Intelligence with a browser plugin that
automatically analyses all the sites that the user visits and
automatically bookmarks the relevant urls.

Our server backend is
obviously written in Swift. Since we have millions of site visits active
in our system at a time, we\'d like to use `structs` for the analysis
part of each site that a user visits. However, if our AI decides that
this is worthy of a bookmark, we\'d like to use CoreData to store this
type in a database.

Now, we don\'t want to write custom serialization to Core Data code
whenever we introduce a new `struct`. Rather, we\'d like to develop this
in a way so that we can utilize it for all future `structs` we develop.

So, how do we do that?
