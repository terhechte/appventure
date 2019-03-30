[frontMatter]
title = "Laws of Composition"
tags = ["keypath", "composition"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Laws of composition

## Appending type-erased keypaths

There're some additional constraints that need to hold in order to allow joining keypaths. In general, you can combine any type of keypath with any other types, except for the following combinations:

### Impossible keypaths combinations

| **First**                | **Second**     |
|--------------------------|----------------|
| KeyPath                  | AnyKeyPath     |
| KeyPath                  | PartialKeyPath |
| WritableKeyPath          | AnyKeyPath     |
| WritableKeyPath          | PartialKeyPath |
| ReferenceWritableKeyPath | AnyKeyPath     |
| ReferenceWritableKeyPath | PartialKeyPath |

This is actually quite easy to remember. You can't append a `AnyKeyPath` or a `PartialKeyPath` to a non-type-erased `KeyPath` type. 

The rule is that the `KeyPath` to be appended has to have at least as many generic types as the type being appended to.

## Appending to type-erased keypaths

The second rule is that appending anything to a type-erased keypath will return an optional keypath:

### Keypaths combinations returning Optional

| **First**                | **Second**     |
|--------------------------|----------------|
| AnyKeyPath               | Anything       |
| PartialKeyPath           | Anything       |

## Appending invalid types

The third, and final, rule is that you can't append non-matching types. So, for example appending `KeyPath<User, String>` and `KeyPath<Address, Int>` will fail at compile time because the types don't match up.
