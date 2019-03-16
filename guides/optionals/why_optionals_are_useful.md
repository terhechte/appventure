[frontMatter]
title = "Why Optionals are useful"
tags = ["optionals", "enum"]
created = "2019-03-02 16:04:26"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Why Optionals are useful

Optionals aim to solve a problem related to something called "null pointers". We don't want to go too much into the history here, instead, we will showcase a typical situation where optionals are needed.

Imagine that you write your own User Defaults. We want to store a value `String` for a key `String` . We will ignore almost everything except for the one function `get` that allows us to get a `String` from the defaults.

``` swift

struct MyDefaults {
  ...
  /// A function that returns a `String`
  func get(key: String) -> String {
  }
}

```

The problem is what do we do when we don't have that value in our defaults? What would we return? Now, we could return an "Empty" string, but that wouldn't be right, would it? Imagine you'd save the username in the defaults. Next time the user starts his app he'd see an empty username. 

What you really want to do is express the notifion of "Nothing". We kinda want to write something like the following:

``` swift
func get(key: String) -> String or Nothing {
}

```

This either gives us back a string or it gives us back nothing. This is fundamentally what optionals are good for. They explain to the Swift type system *and* to the user that a value can either be Something or Nothing. The implementation is also really simple. It is just an `enum` with two cases: `some` and `none`. Some, has the actual value. Here's a simplified version:

``` Swift
enum MyOptional {
  case some(String)
  case none
}
```

That's it. Now, the actual Swift Optional is not limited to Strings, instead it uses `generics` in order to provide support for any kind of type. It kinda looks like this:

``` Swift
enum Optional<Wrapped>
  case some(Wrapped)
  case none
```

So what do we do if we call a function that returns an optional? Since optionals are just simple enums, we can just use Swift's normal `enum` handling for this:

``` Swift
let optionalValue = functionReturningOptional()
switch optionalValue {
  case .some(value): print(value)
  case .none: print("Nothing")
}
```

## The types of Optionals

Thankfully, we don't have to spell out the long `Optional.some` all the time. Instead, Swift offers us a very brief alternative, which is just adding a questionmark `?` to a type. This will tell Swift that this type is an `Optional`. This means that the following two are equal:

``` Swift
let one: Optional<Int> = Optional.some(5)
let two: Int? = 5
```

This is usually the default Syntax for `Optionals` in Swift. You'll hardly see the other Syntax, but it is still good to know as you might stumble upon it from time to time.

Also, if you want to create an empty optional, you can just use `nil` as a shorthand for the empty optional. Again, the following two lines are equal:

``` Swift
let one: Int? = Optional.none
let two: Int? = nil
```

You can only use `nil` if Swift can somehow infer the type of the Optional, so the next example does not work because Swift does not know what kind of `Optional` this is. Is this a `Int?` or a `Float?` or a `String?`. Swift can't find out:

``` Swift
let doesNotWork = nil
```

Swift offers many ways of handling `Optional` types. Lets look at them next.
