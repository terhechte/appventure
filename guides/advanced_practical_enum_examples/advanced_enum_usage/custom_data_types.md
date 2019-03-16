[frontMatter]
title = "Custom Data Types"
tags = ["enum", "literal", "ExpressibleByStringLiteral"]
created = "2019-03-01 16:29:51"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Custom Data Types

If we neglect `associated values`, then the value of an enum can only be
an Integer, Floating Point, String, or Boolean. If you need to support
something else, you can do so by implementing the
`ExpressibleByStringLiteral` protocol which allows the type in question to
be serialized to and from String.

As an example, imagine you\'d like to store the different screen sizes
of iOS devices in an enum:

``` Swift
enum Devices: CGSize {
   case iPhone3GS = CGSize(width: 320, height: 480)
   case iPhone5 = CGSize(width: 320, height: 568)
   case iPhone6 = CGSize(width: 375, height: 667)
   case iPhone6Plus = CGSize(width: 414, height: 736)
}
```

However, this doesn\'t compile because `CGSize` is not a `literal` and can\'t be
used as an enum value. Instead, what you need to do is add a type
extension for the `ExpressibleByStringLiteral` protocol. 

The protocol
requires us to implement an initializer that receives a `String`. Next, we need to
take this `String` an convert it into a `CGSize`. Not any `String` can be a `CGSize`.
So if the value is wrong, we will crash with an error as this code will be executed
by Swift during application startup. Our string format for sizes is: `width,height`

``` Swift
extension CGSize: ExpressibleByStringLiteral {
    public init(stringLiteral value: String) {
        let components = rawValue.split(separator: ",")
        guard components.count == 2,
            let width = Int(components[0]),
            let height = Int(components[1])
            else { return fatalError("Invalid Format \(value)") }
        self.init(width: size.width, height: size.height)
    }
}
```

Now, we can write our `enum`, with one downside though: The initial
values have to be written as a String, since that\'s what the enum will
use (remember, we complied with `ExpressibleByStringLiteral`, so that the
**String** can be converted to our `CGSize` type.

``` Swift
enum Devices: CGSize {
   case iPhone3GS = "320,480"
   case iPhone5 = "320,568"
   case iPhone6 = "375,667"
   case iPhone6Plus = "414,736"
}
```

This, finally, allows us to use our `CGSize` enum. Keep in mind that in
order to get the actual `CGSize` value, we have to access the `rawValue`
of the enum.

``` Swift
let a = Devices.iPhone5
let b = a.rawValue
print("the phone size string is \(a), width is \(b.width), height is \(b.height)")
```

This works, because we explicitly told Swift that a `CGSize` can be created
from any `String`. 

A different option to hook into custom types it the `RawRepresentable` protocol, we will tackle this next.

