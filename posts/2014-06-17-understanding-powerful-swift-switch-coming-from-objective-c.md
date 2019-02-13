[frontMatter]
description = "FIXME FIXME FIXME"
title = "Understanding the powerful Switch statement in Swift"
created = "2014-06-17"
published = false
keywords = ["lisp", "swift", "optional", "scala", "simple", "optionals", "switch", "chaining"]
slug = "2014-06-17-understanding-powerful-swift-switch-coming-from-objective-c.html"
tags = ["swift", "ios", "cocoa"]
---

Among the new features that Swift offers to Objective-C programmers is
one that disguises itself like a boring old man while it offers huge
potential for forming elegant solutions to otherwise unwieldy sets of
nested branches. I\'m of course talking about the `switch` statement
that many Objective-C programmers probably consider as a clunky syntax
device that is most entertaining when used as [Duff\'s
Device](http://en.wikipedia.org/wiki/Duff's_device), but usually offers
little to no advantages over multiple if statements.

In this short tutorial, I will try to give you a deeper introduction
into the Swift Switch statement. I\'ll ignore these use cases, where
switch is effectively being used just like the Objective-C namesake.

### The Switch statement

If you read my [explanation of how optionals
work,](http://appventure.me/2014/06/13/swift-optionals-made-simple/)
you\'ll already have seen how the Switch statement can easily be used to
unwrap an Optional. If you haven\'t, you should. Nevertheless, let me
start this post with a small reminder of how this works:

``` Swift
var result: String? = secretMethod()
switch result {
case .None:
    println("is nothing")
case let a:
    println("\(a) is a value")
}
```

As you can see, `result` could be a string, but it could also be nil.
It\'s an optional. By switching on result, we can figure out whether it
is `.None` or whether it is an actual value. Even more, if it is a
value, we can also bind this value to variable right away. In this case
`a`. What\'s beautiful here, is the clearly visible distinction between
the two states, that the variable `result` can be in.

### Breaking down data

Oftentimes, when you get data from an external source, like a library,
or an API, it is not only good practige but usually even required that
you check the data for consistency before interpreting it. You need to
make sure that all keys exists or that the data is of the correct type,
or the arrays have the required length. Not doing so can lead from buggy
behaviour (missing key) to crash of the app (indexing non-existent array
items). The classic way to do this is by nesting `if` statements.

Let\'s imagine an API that returns a user. However, there\'re two types
of users: System users - like the administrator, or the postmaster - and
local users - like \"John B\", \"Bill Gates\", etc. Due to the way the
system was designed and grew, there\'re a couple of nuisances that API
consumers have to deal with:

-   `system` and `local` users come via the same API call.
-   `the department` key may not exist, since early versions of the db
    did not have that field and early employees never had to fill it
    out.
-   the `name` array contains either 4 items (username, firstname,
    middlename, lastname) or 2 items (username, full name) depending on
    when the user was created.
-   age may be a string, in which case it is the date when the user was
    born, or a number, in which case it is the current age[^1].

``` Objective-C
// Example:
// may return: {type: @"system", department: ..., age: ..., name: [username, firstname, middlename, lastname]}
NSArray *user = [api userWithId:4]; 
```

Let\'s try parsing such a dictionary in the traditional way. I\'m using
Objective-C examples as this will better display just how much more
concise the Swift / Switch way is.

``` Objective-C
// Example:
// may return: {type: @"system", department: ..., age: ..., name: [username, firstname, middlename, lastname]}
NSArray *user = [api userWithId:4]; 
if ([user["type"] isEqualToString: @"system"]) {
}
```

[^1]: You may say that this is a contrieved example, but especially when
    you\'re working with internal, home-grown API\'s in the B2B area,
    there\'s a lot of weird structures. Even the Facebook API had lots
    of such atrocities, back before they started cleaning it up and
    incorportated breaking changes.
