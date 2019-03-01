[frontMatter]
title = "Custom Data Types"
tags = []
created = "2019-03-01 16:29:51"
description = ""
published = false

---

# Custom Data Types

If we neglect associated values, then the value of an enum can only be
an Integer, Floating Point, String, or Boolean. If you need to support
something else, you can do so by implementing the
`StringLiteralConvertible` protocol which allows the type in question to
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

However, this doesn\'t compile. CGSize is not a literal and can\'t be
used as an enum value. Instead, what you need to do is add a type
extension for the `StringLiteralConvertible` protocol. The protocol
requires us to implement three **initializers** each of them is being
called with a `String`, and we have to convert this string into our
receiver type (`CGSize`)

``` Swift
extension CGSize: ExpressibleByStringLiteral {
    public init(stringLiteral value: String) {
        let size = CGSizeFromString(value)
        self.init(width: size.width, height: size.height)
    }

    public init(extendedGraphemeClusterLiteral value: String) {
        let size = CGSizeFromString(value)
        self.init(width: size.width, height: size.height)
    }

    public init(unicodeScalarLiteral value: String) {
        let size = CGSizeFromString(value)
        self.init(width: size.width, height: size.height)
    }
}
```

Now, we can write our `enum`, with one downside though: The initial
values have to be written as a String, since that\'s what the enum will
use (remember, we complied with StringLiteralConvertible, so that the
**String** can be converted to our `CGSize` type.

``` Swift
enum Devices: CGSize {
   case iPhone3GS = "{320, 480}"
   case iPhone5 = "{320, 568}"
   case iPhone6 = "{375, 667}"
   case iPhone6Plus = "{414, 736}"
}
```

This, finally, allows us to use our `CGSize` enum. Keep in mind that in
order to get the actual CGSize value, we have to access the `rawvalue`
of the enum.

``` Swift
let a = Devices.iPhone5
let b = a.rawValue
print("the phone size string is \(a), width is \(b.width), height is \(b.height)")
// prints : the phone size string is iPhone5, width is 320.0, height is 568.0
```

The String serialization requirement makes it a bit difficult to use any
kind of type, but for some specific use cases, this can work well (such
as **NSColor** / **UIColor**). However, you can also use this with your
custom types obviously.

## Comparing Enums with associated values

Enums, by nature, are easily comparable by equality. A simple
`enum T { case a, b}` implementation supports the proper equality tests
`T.a == T.a, T.b != T.a`.

If you add associated values though, Swift cannot correctly infer the
equality of two enums, and you have to implement the `==` operator
yourself. This is simple though:

``` Swift
enum Trade {
    case Buy(stock: String, amount: Int)
    case Sell(stock: String, amount: Int)
}
func ==(lhs: Trade, rhs: Trade) -> Bool {
   switch (lhs, rhs) {
     case let (.Buy(stock1, amount1), .Buy(stock2, amount2))
           where stock1 == stock2 && amount1 == amount2:
           return true
     case let (.Sell(stock1, amount1), .Sell(stock2, amount2))
           where stock1 == stock2 && amount1 == amount2:
           return true
     default: return false
   }
}
```

As you can see, we\'re comparing the two possible `enum cases` via a
switch, and only if the cases match (i.e. .Buy & .Buy) will we compare
the actual associated values.

