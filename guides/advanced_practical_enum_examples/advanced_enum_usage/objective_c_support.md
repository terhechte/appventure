[frontMatter]
title = "Objective-C Support"
tags = ["objc", "enum"]
created = "2019-03-01 16:29:51"
description = ""
published = false

---

# Objective-C Support

Integer-based enums such as can be bridged to Objective-c via the `@objc` attribute:

``` Swift
@objc enum Bit: Int { 
  case zero = 0 
  case one = 1
}
```

However once you venture away from
integers (say `String`) or start using `associated values` you can\'t
use enums from within Objective-C.

There is a manual way though. Add two methods to your
`enum`, define a type replacement on the `@objc` side, and you can move
`enums` back and forth just fine, without having to conform to private
protocols:

``` Swift
enum Trade {
    case buy(stock: String, amount: Int)
    case sell(stock: String, amount: Int)
}

// This type could also exist in Objective-C code.
@objc class ObjcTrade: NSObject {
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

    func toObjc() -> ObjcTrade {
        switch self {
        case let .buy(stock, amount):
            return ObjcTrade(type: 0, stock: stock, amount: amount)
        case let .sell(stock, amount):
            return ObjcTrade(type: 1, stock: stock, amount: amount)
        }
    }

    static func fromObjc(source: ObjcTrade) -> Trade? {
        switch (source.type) {
        case 0: return Trade.buy(stock: source.stock, amount: source.amount)
        case 1: return Trade.sell(stock: source.stock, amount: source.amount)
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
