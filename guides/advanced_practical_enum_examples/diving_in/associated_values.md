[frontMatter]
title = "Associated Values"
tags = ["enum", "associated"]
created = "2019-03-01 16:29:51"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Associated Values

Associated values are a fantastic way of attaching additional
information to an `enum case`. Say you\'re writing a trading engine, and
there\'re two different possible trade types. `buy` and `sell`. Each of
them would be for a specific stock and amount:

### Simple Example

``` Swift
enum Trade {
    case buy
    case sell
}
func trade(tradeType: Trade, stock: String, amount: Int) {}
```

However, the stock and amount clearly belong to the trade in question,
having them as separate parameters feels unclean. You could embed it
into a `struct`, but associated values allow for a much cleaner
solution:

``` Swift
enum Trade {
    case buy(stock: String, amount: Int)
    case sell(stock: String, amount: Int)
}
func trade(type: Trade) {}
```

This defines two cases, `buy` and `sell`. Each of these cases has additional
values attached to it: The `stock` and amount to buy / sell. These cases cannot exist
without these additional values. You can't do this:

``` Swift
let trade = Trade.buy
```

You always have to initialize these cases **with the associated** values:

``` Swift
let trade = Trade.buy("APPL", 500)
```

### Pattern Matching

If you want to access this information, again, [pattern matching comes
to the
rescue](apv::switch):

``` Swift
let trade = Trade.buy(stock: "AAPL", amount: 500)

if case let Trade.buy(stock, amount) = trade {
    print("buy \(amount) of \(stock)")
}
```

Here, you're telling the Swift compiler the following:
"If the `trade` is of type `Trade.buy` with the two values `stock` and `amount`, then `let` those
two variables exist with the values". You kinda have to read this `if` line from right to left.

There's an alternative way of writing this with two `let` statements:

``` Swift
if case Trade.buy(let stock, let amount) = trade {
  ...
}
```

### Labels

Associated values do not require labels. You can just denote the types you'd like to see in your `enum case`.

``` Swift
enum Trade {
   case buy(String, Int)
   case sell(String, Int)
}

// Initialize without labels
let trade = Trade.sell("APPL", 500)
```

If you don't add labels, you also don't write them out when creating a case. 
If you add them, though, you\'ll have to always type them out when creating
your enum cases.

### Use Case Examples

Associated Values can be used in a variety of ways. What follows is a list of short examples in
no particular order.

``` Swift
// Cases can have different values
enum UserAction {
  case openURL(url: NSURL)
  case switchProcess(processId: UInt32)
  case restart(time: NSDate?, intoCommandLine: Bool)
}

// Or imagine you're implementing a powerful text editor that allows you to have
// multiple selections, like Sublime Text here:
// https://www.youtube.com/watch?v=i2SVJa2EGIw
enum Selection {
  case none
  case single(Range<Int>)
  case multiple([Range<Int>])
}

// Or mapping different types of identifier codes
enum Barcode {
    case UPCA(numberSystem: Int, manufacturer: Int, product: Int, check: Int)
    case QRCode(productCode: String)
}

// Or, imagine you're wrapping a C library, like the Kqeue BSD/Darwin notification
// system: https://www.freebsd.org/cgi/man.cgi?query=kqueue&sektion=2
enum KqueueEvent {
    case userEvent(identifier: UInt, fflags: [UInt32], data: Int)
    case readFD(fd: UInt, data: Int)
    case writeFD(fd: UInt, data: Int)
    case vnodeFD(fd: UInt, fflags: [UInt32], data: Int)
    case errorEvent(code: UInt, message: String)
}

// Finally, all user-wearable items in an RPG could be mapped with one
// enum, that encodes for each item the additional armor and weight
// Now, adding a new material like 'Diamond' is just one line of code and we'll have the option to add several new Diamond-Crafted wearables.
enum Wearable {
    enum Weight: Int {
        case light = 1
        case mid = 4
        case heavy = 10
    }
    enum Armor: Int {
        case light = 2
        case strong = 8
        case heavy = 20
    }
    case helmet(weight: Weight, armor: Armor)
    case breastplate(weight: Weight, armor: Armor)
    case shield(weight: Weight, armor: Armor)
}
let woodenHelmet = Wearable.helmet(weight: .light, armor: .light)
```
