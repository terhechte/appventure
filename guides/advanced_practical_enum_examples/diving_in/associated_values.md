[frontMatter]
title = "Associated Values"
tags = []
created = "2019-03-01 16:29:51"
description = ""
published = false

---

# Associated Values

Associated values are a fantastic way of attaching additional
information to an `enum case`. Say you\'re writing a trading engine, and
there\'re two different possible trade types. `Buy` and `Sell`. Each of
them would be for a specific stock and amount:

### Simple Example

``` Swift
enum Trade {
    case Buy
    case Sell
}
func trade(tradeType: Trade, stock: String, amount: Int) {}
```

However, the stock and amount clearly belong to the trade in question,
having them as separate parameters feels unclean. You could embed it
into a `struct`, but associated values allow for a much cleaner
solution:

``` Swift
enum Trade {
    case Buy(stock: String, amount: Int)
    case Sell(stock: String, amount: Int)
}
func trade(type: Trade) {}
```

### Pattern Matching

If you want to access this information, again, [pattern matching comes
to the
rescue](http://appventure.me/2015/08/20/swift-pattern-matching-in-detail/):

``` Swift

let trade = Trade.Buy(stock: "AAPL", amount: 500)
if case let Trade.Buy(stock, amount) = trade {
    print("buy \(amount) of \(stock)")
}

```

### Labels

Associated values do not require labels:

``` Swift
enum Trade {
   case Buy(String, Int)
   case Sell(String, Int)
}
```

If you add them, though, you\'ll have to type them out when creating
your enum cases.

### Tuples as Arguments

What\'s more, the Swift internal associated information is just a
`Tuple`, so you can do things like this:

``` Swift

let tp = (stock: "TSLA", amount: 100)
let trade = Trade.Sell(tp)

if case let Trade.Sell(stock, amount) = trade {
    print("buy \(amount) of \(stock)")
}
// Prints: "buy 100 of TSLA"
```

This syntax allows you to take `Tuples` as a simple data structure and
later on automatically elevate them into a higher type like an
`enum case`. Imagine an app where a user can configure a Desktop that he
wants to order:

``` Swift
typealias Config = (RAM: Int, CPU: String, GPU: String)

// Each of these takes a config and returns an updated config
func selectRAM(_ config: Config) -> Config {return (RAM: 32, CPU: config.CPU, GPU: config.GPU)}
func selectCPU(_ config: Config) -> Config {return (RAM: config.RAM, CPU: "3.2GHZ", GPU: config.GPU)}
func selectGPU(_ config: Config) -> Config {return (RAM: config.RAM, CPU: config.CPU, GPU: "NVidia")}

enum Desktop {
   case Cube(Config)
   case Tower(Config)
   case Rack(Config)
}

let aTower = Desktop.Tower(selectGPU(selectCPU(selectRAM((0, "", "") as Config))))
```

Each step of the configuration updates a `tuple` which is handed in to
the `enum` at the end. This works even better if we take a hint from
**functional programming** apply [^2]:

``` Swift

infix operator <^> { associativity left }

func <^>(a: Config, f: (Config) -> Config) -> Config { 
    return f(a)
}
```

Finally, we can thread through the different configuration steps. This
is particularly helpful if you have many of those steps.

``` Swift

let config = (0, "", "") <^> selectRAM  <^> selectCPU <^> selectGPU
let aCube = Desktop.Cube(config)

```

### Use Case Examples {#basicexamples}

Associated Values can be used in a variety of ways. As code can tell
more than a thousand words, what follows is a list of short examples in
no particular order.

``` Swift
// Cases can have different values
enum UserAction {
  case OpenURL(url: NSURL)
  case SwitchProcess(processId: UInt32)
  case Restart(time: NSDate?, intoCommandLine: Bool)
}

// Or imagine you're implementing a powerful text editor that allows you to have
// multiple selections, like Sublime Text here:
// https://www.youtube.com/watch?v=i2SVJa2EGIw
enum Selection {
  case None
  case Single(Range<Int>)
  case Multiple([Range<Int>])
}

// Or mapping different types of identifier codes
enum Barcode {
    case UPCA(numberSystem: Int, manufacturer: Int, product: Int, check: Int)
    case QRCode(productCode: String)
}

// Or, imagine you're wrapping a C library, like the Kqeue BSD/Darwin notification
// system: https://www.freebsd.org/cgi/man.cgi?query=kqueue&sektion=2
enum KqueueEvent {
    case UserEvent(identifier: UInt, fflags: [UInt32], data: Int)
    case ReadFD(fd: UInt, data: Int)
    case WriteFD(fd: UInt, data: Int)
    case VnodeFD(fd: UInt, fflags: [UInt32], data: Int)
    case ErrorEvent(code: UInt, message: String)
}

// Finally, all user-wearable items in an RPG could be mapped with one
// enum, that encodes for each item the additional armor and weight
// Now, adding a new material like 'Diamond' is just one line of code and we'll have the option to add several new Diamond-Crafted wearables.
enum Wearable {
    enum Weight: Int {
        case Light = 1
        case Mid = 4
        case Heavy = 10
    }
    enum Armor: Int {
        case Light = 2
        case Strong = 8
        case Heavy = 20
    }
    case Helmet(weight: Weight, armor: Armor)
    case Breastplate(weight: Weight, armor: Armor)
    case Shield(weight: Weight, armor: Armor)
}
let woodenHelmet = Wearable.Helmet(weight: .Light, armor: .Light)
```
