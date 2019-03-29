[frontMatter]
title = "First Steps"
tags = ["keypath"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# KeyPaths 101

We will start with a very, very simple example. Below, we create a `User` type that has just one property, the username. Then, we initialize the user as `firstUser` and want to print out `firstUser`s `username`. Normally, we would do `print(firstUser.username)` but instead we're doing something else. Have a look:

``` Swift
struct User {
  var username: String
}

let firstUser = User(username: "Player 1")

print(firstUser[keyPath: \User.username])
```

You'll easily see the difference. Instead of using `firstUser.username` we're using a very weird syntax:

``` Swift
firstUser[keyPath: \User.username]
```

This tells Swift that we want to access the contents of the property `username` of the type `User` on the instance `firstUser`. It is a bit like dictionary access `dict["Hello"]`, only that you don't use `String` types but something else. The type of `\User.username` is `KeyPath` because `\User.username` is a Swift KeyPath.

At first glance, this looks like an overly verbose version of direct access, so what else can it do? For one, we can abstract the access away. We can store the `KeyPath` in a variable:

``` Swift
let userKeyPath = \User.username

print(firstUser[keyPath: \User.username])
```

Here, we suddenly introduced a generic abstraction between the property and the type. Before we see how this can be used, it is necessary to understand the type of this KeyPath. This is how the full type signature for this particular KeyPath looks:

``` Swift
let keyPath: KeyPath<User, String> = \User.username
```

`KeyPath` has two generic types:

1. The `Root`. It is the `struct`, `class`, or `enum` whose property you want to have a `KeyPath` to. A `Person`, a `UIViewController`, a `String`, or something else
2. This is the `Value`. It is a property on the `Root` type. For example a `Person`'s `name`, or a `UIViewController`'s `title`, or a `String`'s `count`.

So in our example, the `Root` is `User`, and the `Value` is `String` because `username` is of type `String`. Here is an overview.

![Setup](/img-content/keypaths_type_overview.gif)
