[frontMatter]
title = "Type Casting Pattern"
tags = []
created = "2019-02-15 20:40:47"
description = ""
published = false

---

# Type Casting Pattern

As the name already implies, this pattern casts or matches types. It has
two different keywords:

-   `is` **type**: Matches the runtime type (or a subclass of it)
    against the right hand side. This performs a type cast but
    disregards the returned type. So your `case` block won\'t know about
    the matched type.
-   pattern `as` **type**: Performs the same match as the `is` pattern
    but for a successful match casts the type into the pattern specified
    on the left hand side.

Here is an example of the two.

``` Swift
let a: Any = 5 
switch a {
  // this fails because a is still anyobject
  // error: binary operator '+' cannot be applied to operands of type 'Any' and 'Int'
  case is Int: print (a + 1)
  // This works and returns '6'
  case let n as Int: print (n + 1)
  default: ()
}
```

Note that there is no `pattern` before the `is`. It matches directly
against `a`.
