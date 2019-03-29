[frontMatter]
title = "Dictionary Keys"
tags = ["keypath", "hashable", "key", "dictionary"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# 3. KeyPaths conform to `Hashable`

We did not see an example of this  yet, but it is one of my all-time favorite keypaths functions. Every `KeyPath` type is `Hashable` which means that it can be used as a key in a dictionary. One use case for this is storing meta information about properties in a dictionary. Here, we have a dictionary that maps from partial key paths to `String`. It stores to different keypaths (`username`, `age`) and their titles:

``` Swift
let meta: [PartialKeyPath<User>: String] = [
  \User.username: "Your Username",
  \User.age: "Your Age"
]
```

We can now write a function `renderTitle` that will retrieve this meta information and print it out alongside the actual value:

``` Swift
func renderTitle(on: User, keyPath: AnyKeyPath) {
  if let title = meta[keyPath] {
    print(title, terminator: ": ")
  }
  print(on[keyPath: keyPath])
}

let myUser = User(username: "Jon", age: 44)

renderTitle(on: myUser, keyPath: \User.age)
```

This would print `Your Age: 44`

This pattern can be used for many more situations. Whenever you have information about a type, you can utilize it to store the information. Another example would be input validation.
