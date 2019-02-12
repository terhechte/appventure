[frontMatter]
description = "Three quick examples for how you can use guard to write shorter and simpler code"
title = "Three tips for concise Swift using the Guard statement"
created = "2016-03-29"
published = true
keywords = ["swift", "mac", "cocoa", "guard", "let", "enum", "pattern", "matching", "patterns"]
slug = "2016-03-29-three-tips-for-clean-swift-code.html"
tags = ["swift", "cocoa", "ios"]
---

This will be a shorter post compared to some of my previous ones, but I
wanted to share three useful `guard` tips for structuring your functions
in such a way that you end up with code that is more concise and also
easier to understand[^1]. This is **not** a post about general coding
styles or coding guidelines, but more about how `guard` can help you
simplify your code.

Some of this might also have appeared in one of my larger posts on
[enums](https://appventure.me/2015/10/17/advanced-practical-enum-examples/)
or [pattern
matching](https://appventure.me/2015/08/20/swift-pattern-matching-in-detail/),
but for different use cases. Let\'s dive right in:

# Binding and Condition Combination

## Nesting

The first example concerns the use of pattern matching in order to
let[^2] bind variables into the current scope. One thing I really like
about this syntax (compared to, say `if let`) is that it keeps a golden
code path, **guarding**[^3] you from the all-too common **skyscraper of
death**. Compare:

``` {.swift}
// Lots of nonsensical code to show how nested code structures look confusing
if let a = a() {
  let x = b(a)
  x.fn()
  if let u = x.nxt() {
    let ux = u.brm()
    if let uxt = ux.nxt() {
       perform(uxt)
    }
  }
}
```

with:

``` {.swift}
guard let a = a() else { return }
let x = b(a)
x.fn()
guard let u = x.nxt() else { return }
let ux = u.brm()
guard let uxt = ux.nxt() else { return }

perform(uxt)
```

Now these are awful examples of how not to structure an internal API,
but they exist more to drive a point home. `Guard` is great because it
binds the result into the current scope instead of the nested scope. In
larger functions, this makes all the difference between having huge,
difficult-to-grasp deeply-nested functions and clean versions which look
almost like lists of commands.

## Pattern Binding

The above works even better, if your input is an `enum`. Consider how
we\'re handling the following usecase:

``` {.swift}
protocol NotificationListener {
  func handleNotification(notification: Notification)
}
enum Notification {
  case UserLoggedIn(user: String, date: NSDate, domain: String)
  case FileUploaded(file: String, location: String, size: Int, user: String)
}

struct FileUploadHandler: NotificationListener {
  /**
    Implement the notification handling to move uploaded files to temporary folder
  */
  func handleNotification(notification: Notification) {
    guard case .FileUploaded(let file, let location, _, let user) = notification
    else { return }

    if user == self.currentUser {
       self.moveFile(file, atLocation: location)
    }
  }
}
```

The binding in the `guard case` line achieves two things for us:

1.  It makes sure `handleNotifications` only works for `FileUploaded`
    notifications, and not for `UserLoggedIn` notifications.
2.  It binds all the `associated values` of the enum into the current
    scope, making it easy for us to use the data.

## Where Clauses

However, with the power of `guard`, we can even simplify the example. Lo
and behold:

``` {.swift}

struct FileUploadHandler: NotificationListener {
  /**
    Implement the notification handling to move uploaded files to temporary folder
  */
  func handleNotification(notification: Notification) {
    guard case .FileUploaded(let file, let location, _, let user) = notification
    where user == self.currentUser
    else { return }
    self.moveFile(file, atLocation: location)
  }
}

```

Now, the code is even shorter as the `where` clause of the `guard`
expression does the correct matching for us.

You can have multiple `where` clauses in your `guard` statement:

``` {.swift}
import Foundation

func confirmPath(pathObject: AnyObject) -> Bool {
  guard let url = pathObject as? NSURL,
  let components = url.pathComponents
    where components.count > 0,
  let first = components.dropFirst().first
    where first == "Applications",
  let last = components.last
    where last == "MyApp.app"
  else { return false }
  print("valid folder", last)
  return true
}
print(confirmPath(NSURL(fileURLWithPath: "/Applications/MyApp.app")))
// : valid folder MyApp.app
// : true
```

As you can see here, we\'re combining multiple `let` bindings with
related `where` clauses which makes it easy to handle all the
preconditions in one bigger guard statement instead of having to break
it up into multiple singular statements.

## Nested Enums

The above even works for nested enums. This may sound like a far-fetched
example, but I do actually have a project where I\'m using a nested
enum. In this example, we have a list of different items in the sidebar
of an Instagram client. Those can be headlines, seperators, or folders:

``` {.swift}
enum SidebarEntry {
  case Headline(String)
  case Item(String)
  case Seperator
}
```

A sidebar could be defined by an array like this:

``` {.swift}
[.Headline("Global"),
 .Item("Dashboard"),
 .Item("Popular"),
 .Seperator,
 .Headline("Me"),
 .Item("Pictures"),
 .Seperator,
 .Headline("Folders"),
 .Item("Best Pics 2013"),
 .Item("Wedding")
]
```

Here, each `Item` would have to have a different action: I.e. clicking
\"Dashboard\" should do something different compared to clicking
\"Pictures\", or the \"Wedding\" folder. The solution I chose was to
have another, nested, enum within the `Item` enum:

``` {.swift}
enum Action {
  case .Popular
  case .Dashboard
  case .Pictures
  case .Folder(name: String)
}

enum SidebarEntry {
  case Headline(String)
  case Item(name: String, action: Action)
  case Seperator
}

[.Headline("Global"),
 .Item(name: "Dashboard", action: .Dashboard),
 .Item(name: "Popular", action: .Popular),
 .Item(name: "Wedding", action: .Folder("fo-wedding")]
```

Now, if we want publish a folder (to the cloud) we\'d like to really
make sure that we were called with a folder and not a headline or a
Popular item:

``` {.swift}
func publishFolder(entry: SidebarEntry)  {
  guard case .Item(_, .Folder(let name)) = entry 
  else { return }
  Folders.sharedFolders().byName(name).publish()
}
```

This is a great way to model complex hierarchies but still be able to
match even intricate, nested types.

# One-Line Guard Return

This is a short one. When you end up in the `else` case, you may want to
perform an action before you return:

``` {.swift}
guard let a = b() else {
   print("wrong action")
   return
}
// or
guard let a = b() else {
   self.completion(items: nil, error: "Could not")
   return
}
```

As long as your command returns `void`, you can actually combine these
into one:

``` {.swift}
guard let a = b() else {return print("wrong action")}
// or
guard let a = b() else {
   return self.completion(items: nil, error: "Could not")
}
```

I find this much easier on the eyes and better to read. However, it may
reduce readability in a complex project when another developer runs into
this and wonders what kind of type is being returned here.

Alternatively, you can also use the semicolon in these cases[^4]:

``` {.swift}
guard let a = b() else {
  print("argh"); return
}
```

# `try?` in guards

Finally, in cases where you\'d need to perform [a `throwable`
function](https://appventure.me/2015/08/25/optional-throw-swift/), and
you don\'t care about the error result, you can still happily use
`guard` just by utilizing the `try?` syntax, which converts the result
of your throwing call into an optional, depending on whether it worked
or not:

``` {.swift}
guard let item = item,
   result = try? item.perform()
else { return print("Could not perform") }
```

The neat thing about this is that it allows us to combine various Swift
mechanics into one safe call to make sure that our code can safely
proceed.

# Wrapping Up

Everything combined into one long example. This also shows how you can
combine `case` and `let` in one `guard`.

``` {#feature-image .swift export-image="true" export-template="template4"}
guard let messageids = overview.headers["message-id"],
    messageid = messageids.first,
    case .MessageId(_, let msgid) = messageid
    where msgid == self.originalMessageID
    else { return print("Unknown Message-ID:", overview) }
```

That\'s it. For more detailed information, I recommend reading my much
larger articles on [pattern
matching](https://appventure.me/2015/08/20/swift-pattern-matching-in-detail/)
and
[enums](https://appventure.me/2015/10/17/advanced-practical-enum-examples/).

[^1]: In my humble opinion, that is

[^2]: Or `var` bind

[^3]: Hint Hint

[^4]: After leaving Objective-C behind, you\'ll probably have to search
    your keyboard to find the key for it again ;)
