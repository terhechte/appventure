[frontMatter]
title = "Enum values"
tags = ["enum"]
created = "2019-03-01 16:29:51"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Enum values

Sometimes may want to have a value assigned to each `enum` case.
This is useful if the `enum` itself indeed relates to something which
can be expressed in a different type. **C** allows you to assign numbers
to `enum cases`. Swift gives you much more flexibility here:

``` Swift
// A pretty useless enum
enum Binary {
  case zero = 0
  case one = 1
}

// You can also map to strings
enum House: String {
    case baratheon = "Ours is the Fury"
    case greyjoy = "We Do Not Sow"
    case martell = "Unbowed, Unbent, Unbroken"
    case stark = "Winter is Coming"
    case tully = "Family, Duty, Honor"
    case tyrell = "Growing Strong"
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
// mercury = 1, venus = 2, ... neptune = 8
enum Planet: Int {
    case mercury = 1, venus, earth, mars, jupiter, saturn, uranus, neptune
}

// north = "north", ... west = "west"
enum CompassPoint: String {
    case north, south, east, west
}
```

Swift supports the following types for the value of an enum:

-   Integer
-   Floating Point
-   String
-   Boolean

You can support more types [by implementing a specific protocol](lnk::enum-custom-data-types).

If you want to access the values, you can do so with the `rawValue`
property:

``` Swift
let bestHouse = House.stark
print(bestHouse.rawValue)
// prints "Winter is coming"
```

However, there may also be a situation where you want to construct an
`enum case` from an existing raw value. In that case, there\'s a special
initializer for enums:

``` Swift
enum Movement: Int {
    case left = 0
    case right = 1
    case top = 2
    case bottom = 3
}
// creates a movement.Right case, as the raw value for that is 1
let rightMovement = Movement(rawValue: 1)
```

If you use the `rawValue` initializer, keep in mind that it is a
[failable
initializer](lnk::failable-initializer),
i.e. you get back an
[Optional](lnk::optional),
as the value you\'re using may not map to any case at all, say if you
were to write `Movement(rawValue: 42)`.
