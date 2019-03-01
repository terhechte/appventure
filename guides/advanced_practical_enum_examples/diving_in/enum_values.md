[frontMatter]
title = "Enum values"
tags = []
created = "2019-03-01 16:29:51"
description = ""
published = false

---

# Enum values

Of course, you may want to have a value assigned to each `enum` case.
This is useful if the `enum` itself indeed relates to something which
can be expressed in a different type. **C** allows you to assign numbers
to `enum cases`. Swift gives you much more flexibility here:

``` Swift
// Mapping to Integer
enum Movement: Int {
    case Left = 0
    case Right = 1
    case Top = 2
    case Bottom = 3
}

// You can also map to strings
enum House: String {
    case Baratheon = "Ours is the Fury"
    case Greyjoy = "We Do Not Sow"
    case Martell = "Unbowed, Unbent, Unbroken"
    case Stark = "Winter is Coming"
    case Tully = "Family, Duty, Honor"
    case Tyrell = "Growing Strong"
}

// Or to floating point (also note the fancy unicode in enum cases)
enum Constants: Double {
    case π = 3.14159
    case e = 2.71828
    case φ = 1.61803398874
    case λ = 1.30357
}
```

For `String` and `Int` types, you can even omit the values and the Swift
compiler will do the right thing:

``` Swift
// Mercury = 1, Venus = 2, ... Neptune = 8
enum Planet: Int {
    case Mercury = 1, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune
}

// North = "North", ... West = "West"
enum CompassPoint: String {
    case North, South, East, West
}
```

Swift supports the following types for the value of an enum:

-   Integer
-   Floating Point
-   String
-   Boolean

So you won\'t be able[^1] to use, say, a CGPoint as the value of your
enum.

If you want to access the values, you can do so with the `rawValue`
property:

``` Swift
let bestHouse = House.Stark
print(bestHouse.rawValue)
// prints "Winter is coming"
```

However, there may also be a situation where you want to construct an
`enum case` from an existing raw value. In that case, there\'s a special
initializer for enums:

``` Swift
enum Movement: Int {
    case Left = 0
    case Right = 1
    case Top = 2
    case Bottom = 3
}
// creates a movement.Right case, as the raw value for that is 1
let rightMovement = Movement(rawValue: 1)
```

If you use the `rawValue` initializer, keep in mind that it is a
[failable
initializer](https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/Swift_Programming_Language/Declarations.html#//apple_ref/doc/uid/TP40014097-CH34-ID376),
i.e. you get back an
[Optional](http://appventure.me/2014/06/13/swift-optionals-made-simple/),
as the value you\'re using may not map to any case at all, say if you
were to write `Movement(rawValue: 42)`.

This is a very useful feature in case you want to encode low level C
binary representations into something much more readable. As an example,
have a look as this encoding of the **VNode Flags** for [the BSD kqeue
library](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man2/kqueue.2.html):

``` Swift
enum VNodeFlags : UInt32 {
    case Delete = 0x00000001
    case Write = 0x00000002
    case Extended = 0x00000004
    case Attrib = 0x00000008
    case Link = 0x00000010
    case Rename = 0x00000020
    case Revoke = 0x00000040
    case None = 0x00000080
}
```

This allows you to use the much nicer looking **Delete** or **Write**
cases, and later on hand the raw value into the **C** function only when
it is really needed.
