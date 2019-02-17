[frontMatter]
title = "Fallthrough, Break and Labels"
tags = []
created = "2019-02-15 20:40:47"
description = ""
published = false

---

# Fallthrough, Break and Labels

The following is not directly related to pattern matching but only
affects the `switch` keyword, so I\'ll keep it brief. By default, and
unlike C/C++/Objective-C, `switch` `cases` do not fall through into the
next case which is why in Swift, you don\'t need to write `break` for
every case. You can opt into traditional fallthrough behaviour with the
`fallthrough` keyword.

``` Swift
switch 5 {
   case 5:
    print("Is 5")
    fallthrough
   default:
    print("Is a number")
}
// Will print: "Is 5" "Is a number"
```

Alternatively, you can use `break` to break out of a switch statement
early. Why would you do that if there\'s no default fallthrough? For
example if you can only realize within the `case` that a certain
requirement is not met and you can\'t execute the `case` any further:

``` Swift
let userType = "system"
let userID = 10
switch (userType, userID)  {
   case ("system", _):
     guard let userData = getSystemUser(userID) else { break }
     print("user info: \(userData)")
     insertIntoRemoteDB(userData)
   default: ()
}
... more code that needs to be executed
```

Here, we don\'t want to call `insertIntoRemoteData` when the result from
`getSystemUser` is `nil`. Of course, you could just use an `if let`
here, but if multiple of those cases come together, you quickly end up
with a bunch of horrifyingly ugly nested `if lets`.

But what if you execute your switch in a `while` loop and you want to
break out of the loop, not the `switch`? For those cases, Swift allows
you to define `labels` to `break` or `continue` to:

``` Swift
gameLoop: while true {
  switch state() {
     case .Waiting: continue gameLoop
     case .Done: calculateNextState()
     case .GameOver: break gameLoop
  }
}
```

We\'ve discussed the syntax and implementation details of `switch` and
pattern matching. Now, let us have a look at some interesting (more or
less) real world examples.
