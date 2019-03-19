[frontMatter]
title = "Comparing Enums"
tags = ["enum", "equatable", "associated"]
created = "2019-03-01 16:29:51"
description = ""
published = true

[meta]
swift_version = "5.0"
new = "3/2019"
---

# Comparing Enums

Just like need to compare strings (`"world" == "hello"`) or numbers you sometimes also need to compare enums. For very simple ones, like the following, this is easy as Swift takes care of it:

``` Swift
enum Toggle {
  case on, off
}

Toggle.on == Toggle.off
```

But what if you have a more complex `enum` with `associated values` like this one?

``` Swift
enum Character {
  case warrior(name: String, level: Int, strength: Int)
  case wizard(name: String, magic: Int, spells: [String])
}
```

If you'd try to compare to instances of `Character` Swift would complain. By default, it doesn't know how to compare `enum` types that have `associated values`. However, you can explicitly tell Swift to just compare all the values of each `case` and if they're the same, then the types are `equal`. To do that, you'd just add an empty conformance to the `Equatable` protocol:

``` Swift
enum Character: Equatable {
  case warrior(name: String, level: Int, strength: Int)
  case wizard(name: String, magic: Int, spells: [String])
}
```

Just this one addition `Equatable` will allow you to compare your types. This only works if all the values in your cases are also `Equatable`. This works in our example as `Int`, `String` and arrays of `String` are `Equatable` by default.

If you have a custom type that doesn't conform to `Equatable`, the above will not work:

``` Swift
struct Weapon { 
  let name: String 
}

enum Character: Equatable {
  case warrior(name: String, level: Int, strength: Int, weapon: Weapon)
  case wizard(name: String, magic: Int, spells: [String])
}
```

In this case, Swift will complain that `Character` does not conform to `Equatable`. So the solution here is to also conform `Weapon` to `Equatable`. 

If that is not an option, you an always implement a custom `Equatable` conformance:

``` Swift
// Not Equatable Stock
struct Stock { ... }
enum Trade {
    case buy(stock: Stock, amount: Int)
    case sell(stock: Stock, amount: Int)
}
func ==(lhs: Trade, rhs: Trade) -> Bool {
   switch (lhs, rhs) {
   case let (.buy(stock1, amount1), .buy(stock2, amount2))
         where stock1 == stock2 && amount1 == amount2:
         return true
   case let (.sell(stock1, amount1), .sell(stock2, amount2))
         where stock1 == stock2 && amount1 == amount2:
         return true
   default: return false
   }
}
```

As you can see, we\'re comparing the two possible `enum cases` via a
switch, and only if the cases match (i.e. .buy & .buy) will we compare
the actual associated values.

