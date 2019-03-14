[frontMatter]
title = "Fixed-Size Sequences"
tags = ["tuples"]
created = "2019-03-01 17:35:30"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Fixed-Size Sequences

Another area where tuples can be used is when you intend to constrain a
type to a fixed number of items. Imagine an object that calculates
various statistics for each month in a year. You need to store a certain
Integer value for each month separately. The solution that comes to mind
first would of course be:

``` Swift
var monthValuesArray: [Int]
```

However, in this case we don\'t know whether the property indeed
contains 12 elements. A user of our object could accidentally insert 13
values, or 11. We can\'t tell the type checker that this is a fixed size
array of 12 items. With a tuple, this specific constraint can easily
be put into place:

``` Swift
var monthValues: (Int, Int, Int, Int, Int, Int, Int, Int, Int, Int, Int, Int)
```

The alternative would be to have the constraining logic in the object\'s
functionality (say via a `guard` statement); however, this would be a
run time check. The tuple check happens at compile time; your code
won\'t even compile if you try to give 11 months to your object.
