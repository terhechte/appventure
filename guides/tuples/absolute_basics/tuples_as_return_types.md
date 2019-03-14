[frontMatter]
title = "Tuples as Return Types"
tags = ["tuples", "destructure"]
created = "2019-03-01 17:35:30"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Tuples as Return Types

Probably the next-best tuple use case is using them to return one-time
structures. Tuples as return types makes sense when you need to return
multiple return types.

The following function is required to return a `User` from our database.
However, in order to speed up processing, the user may be loaded from the
cache instead of a query. If that's the case, the caller of the function
should also receive the information that the `User` was cached, and how
long it was since the last update from the database. We can easily do this
with tuples:

``` Swift
func userFromDatabase(id: Int) -> (user: User, cached: Bool, updated: Date) {
   ...
}
```

This function returns three values, the actual user `user`, whether the user is
cached `cached` and when the user was lasted `updated`.

This also saves you from introducing a new `struct` type.

Since tuples can also be deconstructed on the fly, this even allows re-introducing
the variables at the call site:

``` Swift
let (user, cached, lastUpdated) = userFromDatabase()
```

This will create three new variables in the current scope: `user`, `cached`, and `lastUpdated`.
We will describe this `destructuring` in more detail in the next chapter.
