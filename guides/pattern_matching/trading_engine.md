[frontMatter]
title = "A Trading Engine"
tags = ["pattern matching", "switch"]
created = "2019-02-15 20:40:47"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# A Trading Engine

So a Wall Street company contacts you, they need a new trading platform running
on iOS devices. As it is a trading platform, you define an `enum` for
trades.

## First Draft

``` Swift
enum Trades {
    case buy(stock: String, amount: Int, stockPrice: Float)
    case sell(stock: String, amount: Int, stockPrice: Float)
}
```

You were also handed the following API to handle trades. **Notice how
sell orders are just negative amounts**. 

``` Swift
/**
 - parameter stock: The stock name
 - parameter amount: The amount, negative number = sell, positive = buy
*/
func process(stock: String, _ amount: Int) {
    print ("\(amount) of \(stock)")
}
```

The next step is to process those trades. You see the potential for
using pattern matching and write this:

``` Swift
let aTrade = Trades.buy(stock: "APPL", amount: 200, stockPrice: 115.5)

switch aTrade {
case .buy(let stock, let amount, _):
    process(stock, amount)
case .sell(let stock, let amount, _):
    process(stock, amount * -1)
}
// Prints "buy 200 of APPL"
```

Swift lets us conveniently only destructure / extract the information
from the `enum` that we really want. In this case only the stock and the
amount.

Awesome, you visit Wall Street to show of your fantastic trading
platform. However, as always, the reality is much more cumbersome than
the beautiful theory. Trades aren\'t trades you learn.

-   You have to calculate in a fee which is different based on the
    trader type.
-   The smaller the institution the higher the fee.
-   Also, bigger institutions get a higher priority.

They also realized that you\'ll need a new API for this, so you were
handed this:

``` Swift
func processSlow(stock: String, _ amount: Int, _ fee: Float) { print("slow") }
func processFast(stock: String, _ amount: Int, _ fee: Float) { print("fast") }
```

## Trader Types

So you go back to the drawing board and add another `enum`. The trader
type is part of every trade, too.

``` Swift
enum TraderType {
case singleGuy
case company
} 

enum Trades {
    case buy(stock: String, amount: Int, stockPrice: Float, type: TraderType)
    case sell(stock: String, amount: Int, stockPrice: Float, type: TraderType)
}

```

So, how do you best implement this new restriction? You could just have
an `if` / `else` switch for buy and for sell, but that would lead to
nested code which quickly lacks clarity - and who knows maybe these Wall
Street guys come up with further complications. So you define it instead
as additional requirements on the pattern matches:

``` Swift

let aTrade = Trades.sell(stock: "GOOG", amount: 100, stockPrice: 666.0, type: TraderType.company)

switch aTrade {
case let .buy(stock, amount, _, TraderType.singleGuy):
    processSlow(stock, amount, 5.0)
case let .sell(stock, amount, _, TraderType.singleGuy):
    processSlow(stock, -1 * amount, 5.0)
case let .buy(stock, amount, _, TraderType.company):
    processFast(stock, amount, 2.0)
case let .sell(stock, amount, _, TraderType.company):
    processFast(stock, -1 * amount, 2.0)
}
```

The beauty of this is that there\'s a very succinct flow describing the
different possible combinations. Also, note how we changed
`.buy(let stock, let amount)` into `let .buy(stock, amount)` in order to
keep things simpler. This will destructure the `enum` just as before,
only with less syntax.

## Guards! Guards!

Once again you present your development to your Wall Street customer,
and once again a new issue pops up (you really should have asked for a
more detailed project description).

-   Sell orders exceeding a total value of \$1.000.000 do always get
    fast handling, even if it\'s just a single guy.
-   Buy orders under a total value of \$1.000 do always get slow
    handling.

With traditional nested `if` syntax, this would already become a bit
messy. Not so with `switch`. Swift includes guards for `switch cases`
which allow you to further restrict the possible matching of those
cases.

You only need to modify your `switch` a little bit to accommodate for
those new changes

``` Swift

let aTrade = Trades.buy(stock: "GOOG", amount: 1000, stockPrice: 666.0, type: TraderType.singleGuy)

switch aTrade {
case let .buy(stock, amount, _, TraderType.singleGuy):
    processSlow(stock, amount, 5.0)
case let .sell(stock, amount, price, TraderType.singleGuy)
    where price*Float(amount) > 1000000:
    processFast(stock, -1 * amount, 5.0)
case let .sell(stock, amount, _, TraderType.singleGuy):
    processSlow(stock, -1 * amount, 5.0)
case let .buy(stock, amount, price, TraderType.company)
    where price*Float(amount) < 1000:
    processSlow(stock, amount, 2.0)
case let .buy(stock, amount, _, TraderType.company):
    processFast(stock, amount, 2.0)
case let .sell(stock, amount, _, TraderType.company):
    processFast(stock, -1 * amount, 2.0)
}
```

This code is quite structured, still rather easy to read, and wraps up
the complex cases quite well.

That\'s it, we\'ve successfully implemented our trading engine. However,
this solution still has a bit of repetition; we wonder if there\'re
pattern matching ways to improve upon that. So, let\'s look into pattern
matching a bit more.

