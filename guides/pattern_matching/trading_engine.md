[frontMatter]
title = "A Trading Engine"
tags = []
created = "2019-02-15 20:40:47"
description = ""
published = false

---

# A Trading Engine

So Wall Street contacted you, they need a new trading platform running
on iOS devices. As it is a trading platform, you define an `enum` for
trades.

## First Draft

``` Swift
enum Trades {
    case Buy(stock: String, amount: Int, stockPrice: Float)
    case Sell(stock: String, amount: Int, stockPrice: Float)
}
```

You were also handed the following API to handle trades. **Notice how
sell orders are just negative amounts**. And you\'re told the stock
price is not important, their engine will take an internal one anyway.

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
let aTrade = Trades.Buy(stock: "APPL", amount: 200, stockPrice: 115.5)

switch aTrade {
case .Buy(let stock, let amount, _):
    process(stock, amount)
case .Sell(let stock, let amount, _):
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
case SingleGuy
case Company
} 

enum Trades {
    case Buy(stock: String, amount: Int, stockPrice: Float, type: TraderType)
    case Sell(stock: String, amount: Int, stockPrice: Float, type: TraderType)
}

```

So, how do you best implement this new restriction? You could just have
an `if` / `else` switch for buy and for sell, but that would lead to
nested code which quickly lacks clarity - and who knows maybe these Wall
Street guys come up with further complications. So you define it instead
as additional requirements on the pattern matches:

``` Swift

let aTrade = Trades.Sell(stock: "GOOG", amount: 100, stockPrice: 666.0, type: TraderType.Company)

switch aTrade {
case let .Buy(stock, amount, _, TraderType.SingleGuy):
    processSlow(stock, amount, 5.0)
case let .Sell(stock, amount, _, TraderType.SingleGuy):
    processSlow(stock, -1 * amount, 5.0)
case let .Buy(stock, amount, _, TraderType.Company):
    processFast(stock, amount, 2.0)
case let .Sell(stock, amount, _, TraderType.Company):
    processFast(stock, -1 * amount, 2.0)
}
```

The beauty of this is that there\'s a very succinct flow describing the
different possible combinations. Also, note how we changed
`.Buy(let stock, let amount)` into `let .Buy(stock, amount)` in order to
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

let aTrade = Trades.Buy(stock: "GOOG", amount: 1000, stockPrice: 666.0, type: TraderType.SingleGuy)

switch aTrade {
case let .Buy(stock, amount, _, TraderType.SingleGuy):
    processSlow(stock, amount, 5.0)
case let .Sell(stock, amount, price, TraderType.SingleGuy)
    where price*Float(amount) > 1000000:
    processFast(stock, -1 * amount, 5.0)
case let .Sell(stock, amount, _, TraderType.SingleGuy):
    processSlow(stock, -1 * amount, 5.0)
case let .Buy(stock, amount, price, TraderType.Company)
    where price*Float(amount) < 1000:
    processSlow(stock, amount, 2.0)
case let .Buy(stock, amount, _, TraderType.Company):
    processFast(stock, amount, 2.0)
case let .Sell(stock, amount, _, TraderType.Company):
    processFast(stock, -1 * amount, 2.0)
}
```

This code is quite structured, still rather easy to read, and wraps up
the complex cases quite well.

That\'s it, we\'ve successfully implemented our trading engine. However,
this solution still has a bit of repetition; we wonder if there\'re
pattern matching ways to improve upon that. So, let\'s look into pattern
matching a bit more.

