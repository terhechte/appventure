[frontMatter]
title = "Enums in the Standard Library"
tags = []
created = "2019-03-01 16:31:41"
description = ""
published = false

---

# Enums in the Standard Library

Before we go on and explore various use cases for enums in your
projects, it might be tempting to see some of the enums being used in
the Swift standard library, so let\'s have a look.

[**Bit**](https://developer.apple.com/library/watchos/documentation/Swift/Reference/Swift_Bit_Enumeration/index.html#//apple_ref/swift/enum/s:OSs3Bit)
The `Bit` enum can have two possible values, **One**, and **Zero**. It
is used as the `Index` type for `CollectionOfOne<T>`.

[**FloatingPointClassification**](https://developer.apple.com/library/watchos/documentation/Swift/Reference/Swift_FloatingPointClassification_Enumeration/index.html#//apple_ref/swift/enumelt/FloatingPointClassification/s:FOSs27FloatingPointClassification12SignalingNaNFMS_S_)
This enum defines the set of possible IEEE 754 \"classes\", like
`NegativeInfinity`, `PositiveZero`, or `SignalingNaN`.

[**Mirror.AncestorRepresentation**](https://developer.apple.com/library/watchos/documentation/Swift/Reference/Swift_Mirror-AncestorRepresentation_Enumeration/index.html#//apple_ref/swift/enum/s:OVSs6Mirror22AncestorRepresentation),
and
[**Mirror.DisplayStyle**](https://developer.apple.com/library/watchos/documentation/Swift/Reference/Swift_Mirror-DisplayStyle_Enumeration/index.html#//apple_ref/swift/enum/s:OVSs6Mirror12DisplayStyle)
These two are used in the context of the Swift Reflection API.

[**Optional**](https://developer.apple.com/library/watchos/documentation/Swift/Reference/Swift_Optional_Enumeration/index.html#//apple_ref/swift/enum/s:Sq)
Not much to say here

[**Process**](https://developer.apple.com/library/watchos/documentation/Swift/Reference/Swift_Process_Enumeration/index.html#//apple_ref/swift/enum/s:OSs7Process)
The Process enum contains the command line arguments of the current
process (`Process.argc`, `Process.arguments`). This is a particularly
interesting `enum` as it used to be a `struct` in Swift 1.0.
