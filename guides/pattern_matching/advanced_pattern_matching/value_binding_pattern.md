[frontMatter]
title = "Value-Binding Pattern"
tags = ["pattern matching", "switch", "where"]
created = "2019-02-15 20:40:47"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Value-Binding Pattern

This is the very same as binding values to variables via `let` or `var`.
Only in a switch statement. You\'ve already seen this before, so I\'ll
provide a very short example:

``` Swift
switch (4, 5) {
  case let (x, y): print("\(x) \(y)")
}
```

The `let (x, y)` in the example above will take the values of our `(4, 5)` [tuple](lnk::tuple) and write them into two new variables named `x` and `y`.

We can easily combine this with the other pattern matching operations to develop very powerful patterns. Imagine you have a function that returns an optional tuple `(username: String, password: String)?`. You'd like to match it and make sure if the password is correct:

First, our fantastic function (just a prototype):

``` Swift
func usernameAndPassword() 
    -> (username: String, password: String)? {... }
```

Now, the `switch` example:

``` Swift
switch usernameAndPassword() {
  case let (_, password)? where password == "12345": login()
  default: logout()
}
```

See how we combined multiple Swift features here, we will go through them step by step:

1. We use `case let` to create new variables
2. We use the `?` operator to **only** match if the optional return value from the
   `usernameAndPassword` function is not empty.
3. We ignore the `username` part via `_`, because we're only interested in the `password`
4. We use `where` to make sure our highly secure password is correct
5. We use `default` for all the other cases that fail.
