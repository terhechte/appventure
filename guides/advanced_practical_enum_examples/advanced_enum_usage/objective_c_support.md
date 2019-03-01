[frontMatter]
title = "Objective-C Support"
tags = []
created = "2019-03-01 16:29:51"
description = ""
published = false

---

# Objective-C Support

Integer-based enums such as
`enum Bit: Int { case Zero = 0; case One = 1}` can be bridged to
Objective-c via the `@objc` flag. However once you venture away from
integers (say `String`) or start using **associated values** you can\'t
use enums from within Objective-C.

There is a manual way though. Add two methods to your
`enum`, define a type replacement on the `@objc` side, and you can move
`enums` back and forth just fine, without having to conform to private
protocols:

``` Swift
enum Trade {
    case Buy(stock: String, amount: Int)
    case Sell(stock: String, amount: Int)
}

// This type could also exist in Objective-C code.
@objc class OTrade: NSObject {
    var type: Int
    var stock: String
    var amount: Int
    init(type: Int, stock: String, amount: Int) {
        self.type = type
        self.stock = stock
        self.amount = amount
    }
}

extension Trade  {

    func toObjc() -> OTrade {
        switch self {
        case let .Buy(stock, amount):
            return OTrade(type: 0, stock: stock, amount: amount)
        case let .Sell(stock, amount):
            return OTrade(type: 1, stock: stock, amount: amount)
        }
    }

    static func fromObjc(source: OTrade) -> Trade? {
        switch (source.type) {
        case 0: return Trade.Buy(stock: source.stock, amount: source.amount)
        case 1: return Trade.Sell(stock: source.stock, amount: source.amount)
        default: return nil
        }
    }
}
```

This still has the downside that you need to mirror your `enum` via an
`NSObject` based type on the Objective-C side (or you could just go and
use an `NSDictionary`), but if you ever end up in a situation where you
**need** to access an enum with associated values from Objective-C, this
is a way to do it.
