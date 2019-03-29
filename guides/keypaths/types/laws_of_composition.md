[frontMatter]
title = "Laws of composition"
tags = ["keypath", "composition"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Laws of composition

There're some additional constraints that need to hold in order to allow joining keypaths. In general, you can combine any type of keypath with any other types, except for the following combinations:

| **First**                | **Second**     |
| KeyPath                  | AnyKeyPath     |
| KeyPath                  | PartialKeyPath |
| WritableKeyPath          | AnyKeyPath     |
| WritableKeyPath          | PartialKeyPath |
| ReferenceWritableKeyPath | AnyKeyPath     |
| ReferenceWritableKeyPath | PartialKeyPath |

This is actually quite easy to remember. You can't append a `AnyKeyPath` or a `PartialKeyPath` to a non-type-erased `KeyPath` type. 

The rule is that the `KeyPath` to be appended has to have at least as many generic types as the type being appended to.
