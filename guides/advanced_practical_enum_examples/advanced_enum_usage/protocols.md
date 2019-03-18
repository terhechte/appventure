[frontMatter]
title = "Protocols"
tags = ["protocol", "enum"]
created = "2019-03-01 16:29:51"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Protocols

We already mentioned the similarity between the `struct` and `enum` types. In
addition to the ability to add methods, Swift also allows you to use
**Protocols** and **Protocol Extensions** with enums.

Swift protocols define an interface that types can
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
   case buy, sell
   var description: String {
       switch self {
       case .buy: return "We're buying something"
       case .sell: return "We're selling something"
       }
   }
}
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
  case empty
  case funds(remaining: Int)
  case credit(amount: Int)

  var remainingFunds: Int {
    switch self {
    case .empty: return 0
    case .funds(let remaining): return remaining
    case .credit(let amount): return amount
    }
  }
}
```

To keep things clean, we can then define the required protocol functions
in a protocol extension on the `enum`:

``` Swift
extension Account: AccountCompatible {

  mutating func addFunds(amount: Int) {
    var newAmount = amount
    if case let .funds(remaining) = self {
      newAmount += remaining
    }
    if newAmount < 0 {
      self = .credit(newAmount)
    } else if newAmount == 0 {
      self = .empty
    } else {
      self = .funds(remaining: newAmount)
    }
  }

  mutating func removeFunds(amount: Int) throws {
    try self.addFunds(amount * -1)
  }

}

var account = Account.funds(remaining: 20)
try? account.addFunds(amount:10)
try? account.removeFunds(amount:15)
```

As you can see, we implemented all the protocol requirements by storing
our values within our `enum cases`. A very nifty side effect of this is,
that now you can test for an empty account with a simple pattern match
all over your code base. You don\'t have to see whether the
`remainingFunds` are zero.

We're also implementing the protocol in an extension. We'll learn more about
extensions on `enum` types in the next chapter.
