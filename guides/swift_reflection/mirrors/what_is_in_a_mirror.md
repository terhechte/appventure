[frontMatter]
title = "What is in a Mirror"
tags = ["reflection", "mirror"]
created = "2019-03-01 11:47:01"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# What is in a Mirror

The `Mirror struct` contains several `types` to help you identify the
information you\'d like to query.

The first one is the `DisplayStyle` `enum` which tells you the type of
the subject:

``` Swift
public enum DisplayStyle {
    case `struct`
    case `class`
    case `enum`
    case tuple
    case optional
    case collection
    case dictionary
    case set
}
```

Those are the supported types of the reflection API. As we saw earlier,
reflection only requires an `Any` type, and there\'re many things in the
Swift standard library that are of type `Any` but aren\'t listed in the
`DisplayStyle` enum above. What happens when you try to reflect over one
of those, say a closure?

``` Swift
let closure = { (a: Int) -> Int in return a * 2 }
let aMirror = Mirror(reflecting: closure)
```

In this case, you\'d get a mirror, but the `DisplayStyle` would be nil
[^2]

There\'s also a `typealias` for the child elements of a `Mirror`:

``` Swift
public typealias Child = (label: String?, value: Any)
```

So each child consists out of an optional **label** and a **value** of
type `Any`. Why would the label be an `Optional`? If you think about it,
it makes sense, not all of the structures that are supported by
reflection have children with names. A `struct` has the property\'s name
as the label, but a Collection only has indexes, not names. Tuples are a
little bit special. In Swift values in tuple could have optional labels.
Doesn\'t matter if value in tupple is labeled or not, in reflection
tuple will have labels \".0\", \".1\" and so on.

Next up is the `AncestorRepresentation` `enum`:

``` Swift
public enum AncestorRepresentation {
    /// Generate a default mirror for all ancestor classes.  This is the
    /// default behavior.
    case generated
    /// Use the nearest ancestor's implementation of `customMirror()` to
    /// create a mirror for that ancestor.      
    case customized(@escaping () -> Mirror)
    /// Suppress the representation of all ancestor classes.  The
    /// resulting `Mirror`'s `superclassMirror()` is `nil`.
    case suppressed
}
```

This `enum` is used to define how superclasses of the reflected subject
should be reflected. I.e. this is only used for subjects of type
`class`. The default (as you can see) is that Swift generates an
additional mirror for each superclass. However, if you need more
flexibility here, you can use the `AncestorRepresentation enum` to
define how superclasses are being mirrored. 

