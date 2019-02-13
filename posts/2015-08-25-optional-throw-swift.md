[frontMatter]
description = "Swift 2.0 b6 includes a new way of handling exceptions via the =try?= keyword. This is a quick post to explain the basics, and why this is cool."
title = "Optional throw via try? in Swift 2 beta 6"
created = "2015-08-25"
published = true
keywords = ["swift", "error", "throw", "result", "either", "rethrow", "try", "syntax", "swift2"]
slug = "2015-08-25-optional-throw-swift.html"
tags = ["swift"]
---

<h6><a href="http://swift.gg/2015/09/11/optional-throw-swift/">This post is also available in <b>🇨🇳Chinese</b></a><span> Thanks to </span><a href="http://swift.gg/tags/APPVENTURE/">SwiftGG</a></h6>

Swift 2.0 b6 includes a new way of handling exceptions via the `try?`
keyword. This is a quick post to explain the basics, and why this is
cool.

In Swift 1.x, all we had for error handling were optionals and
`NSError`. Which is [why many people adopted `Either` / `Result`
types](https://github.com/antitypical/Result) as they can be found in
[other](https://hackage.haskell.org/package/base-4.8.1.0/docs/Data-Either.html)
[programming](http://www.scala-lang.org/api/2.9.3/scala/Either.html)
languages:

``` Swift
let success = Result<String, NSError>.Success("success")
```

With Swift 2 and the introduction of `try / catch` exception handling.
Internally, this doesn\'t use expensive stack unwinding, as other (say,
Objective-C or Java) do it, but instead seems to pretty much return
something akin to `Either` or `Result`. Only the syntax hides this from
the user in order to make it simpler to use[^1].

# Swift 2 b5 and earlier

However, once you start using the new `do / try / catch` more, what
happens from time to time is that you start nesting code into messy
branches because `do` is (was) incompatible with the other major way of
handling potentially unknown states: optionals. Here\'s a particular
ugly piece of code. Observe how we\'re nesting `if let` with `let` with
`do` with `let` [^2].

``` Swift

if let uid = loggedInUser() {
    do {
        let username = try getUserName(uid)
        if let data = imagePostForUserName(username, imageURL: nil) {
            do {
                let success = try postImage(data)
                if success {
                    print ("Submitted")
                }  
            } catch {
                // more error handling
            }
        }
    } catch {
        // todo: error handling
    }
}

```

One reason why this is difficult to simplify is that the `do` forces a
break in any multi `guard` or multi `let` [^3].

# Swift 2 b6

With beta 6, we get a new keyword, `try?` which performs a throwing
operation and returns optional `None` in case of failure and optional
`Some` in case of success. [Quoting straight from the
changelog:](http://adcdownload.apple.com/Developer_Tools/Xcode_7_beta_6/Xcode_7_beta_6_Release_Notes.pdf)

> A new keyword \'try?\' has been added to Swift. \'try?\' attempts to
> perform an operation that may throw. If the operation succeeds, the
> result is wrapped in an optional; if it fails (I.e. if an error is
> thrown), the result is \'nil\' and the error is discarded. 'try?' is
> particularly useful when used in conjunction with "if let" and
> "guard".

This makes it possible to retrieve the value of a potential throwing
operation as an optional. If we apply this to our code above, we can
simplify it quite a bit:

``` Swift

if let uid = loggedInUser(),
   username = try? getUserName(uid),
   data = imagePostForUserName(username, imageURL: nil),
   success = try? postImage(data)
   where success == true {
      print ("Submitted")
}

```

This is, of course a bit of a contrived example, engineered to explain
`try?`. But still, that\'s definitely less code. We\'re, of course,
loosing a lot of possibly valuable error information that would
otherwise be available in the `catch`.

# Which to choose?

`try?` can help you write terser code at the expense of loosing
insights. Using `try?` only returns an optional without further
information on the particular cause of the error / exception. The
benefit, of course, is beautiful composability with **a lot** of the
other Swift syntax, like `map`, `flatmap`, `switch`, `guard`, `if let`,
`for case`, and others.

The non-optional `try` works great for distinct task where you\'re not
dependant on earlier or later possible optional results.

The aforementioned `Result` type, on the other hand offers both; either
the requested value, or a possible error. You can just continue using
`Result`, which also has support for wrapping throws and much more,
however keep in mind that this is not the direction Swift seems to
intend to go [^4]. Otherwise, we\'d have a full blown Result or Either
type in Swift 2.

I\'m really happy about the introduction of `try?` as it will make many
snippets, particularly when interacting with the Cocoa API, easier to
solve.

[^1]: Much like the lifting into / out of monads in Swift optionals is
    hidden via the `?` syntax

[^2]: There\'re ways to improve this code without `try?`, of course, but
    it makes for a nice example

[^3]: Another is, of course, that I\'m using raw NSRegularExpression
    here, instead of a simplifying library

[^4]: Also, you\'ll always need to add additional dependencies to your
    project
