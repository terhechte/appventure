[frontMatter]
title = "Protocols"
tags = []
created = "2019-03-01 16:29:51"
description = ""
published = false

---

# Protocols

I already mentioned the similarity between the `structs` and `enums`. In
addition to the ability to add methods, Swift also allows you to use
**Protocols** and **Protocol Extensions** with enums.

Swift protocols define an interface or type that other structures can
conform to. In this case our `enum` can conform to it. For a start,
let\'s take a protocol from the Swift standard library.

`CustomStringConvertible` is a type with a customized textual
representation suitable for printing purposes:

``` Swift
protocol CustomStringConvertible {
  var description: String { get }
}
```

It has only one requirement, namely a **getter** for a string. We can
implement this on an enum quite easily:

``` Swift
enum Trade: CustomStringConvertible {
   case Buy, Sell
   var description: String {
       switch self {
           case .Buy: return "We're buying something"
           case .Sell: return "We're selling something"
       }
   }
}

let action = Trade.Buy.description
print("this action is \(action)")
// prints: this action is We're buying something
```

Some protocol implementations may need internal state handling to cope
with the requirements. Imagine a protocol that manages a bank account:

``` Swift
protocol AccountCompatible {
  var remainingFunds: Int { get }
  mutating func addFunds(amount: Int) throws
  mutating func removeFunds(amount: Int) throws
}
```

You could easily fulfill this protocol with a `struct`, but in the
context of your application, an `enum` is the more sensible approach.
However, you can\'t add properties like `var remainingFunds: Int` to an
`enum`, so how would you model that? The answer is actually easy, you
can use associated values for this:

``` Swift
enum Account {
  case Empty
  case Funds(remaining: Int)

  enum Error: Swift.Error {
    case Overdraft(amount: Int)
  }

  var remainingFunds: Int {
    switch self {
    case .Empty: return 0
    case .Funds(let remaining): return remaining
    }
  }
}
```

To keep things clean, we can then define the required protocol functions
in a protocol extension on the `enum`:

``` Swift
extension Account: AccountCompatible {

  mutating func addFunds(amount: Int) throws {
    var newAmount = amount
    if case let .Funds(remaining) = self {
      newAmount += remaining
    }
    if newAmount < 0 {
      throw Error.Overdraft(amount: -newAmount)
    } else if newAmount == 0 {
      self = .Empty
    } else {
      self = .Funds(remaining: newAmount)
    }
  }

  mutating func removeFunds(amount: Int) throws {
    try self.addFunds(amount * -1)
  }

}

var account = Account.Funds(remaining: 20)
print("add: ", try? account.addFunds(amount:10))
print ("remove 1: ", try? account.removeFunds(amount:15))
print ("remove 2: ", try? account.removeFunds(amount:55))
// prints:
// : add:  Optional(())
// : remove 1:  Optional(())
// : remove 2:  nil
```

``` {.example}
add:  Optional(())
remove 1:  Optional(())
remove 2:  nil
```

As you can see, we implemented all the protocol requirements by storing
our values within our `enum cases`. A very nifty side effect of this is,
that now you can test for an empty account with a simple pattern match
all over your code base. You don\'t have to see whether the
remainingFunds are zero.

We\'re also nesting an `ErrorType` compatible `enum` in the **Account**
enum so that we can use Swift 2.0\'s new error handling. This is
explained in more detail in the [**Practical Use Cases**](#errortype)
section.
