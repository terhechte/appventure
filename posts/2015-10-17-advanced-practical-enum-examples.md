[frontMatter]
description = "When and how to use enums in Swift? This is a detailed practical overview of all the possibilities enums can offer you."
title = "Advanced & Practical Enum usage in Swift"
created = "2015-10-17"
published = true
keywords = ["feature", "swift", "enum", "algebraic", "caseclass", "union", "case", "switch", "pattern", "simple", "practical", "advanced", "example"]
slug = "2015-10-17-advanced-practical-enum-examples.html"
tags = ["swift", "cocoa", "ios"]
---

<h6><a href="http://swift.gg/2015/11/20/advanced-practical-enum-examples/">This post is also available in <b>🇨🇳Chinese</b></a><span> Thanks to </span><a href="http://swift.gg/tags/APPVENTURE/">SwiftGG</a></h6>

When and how to use enums in Swift? This is a detailed practical
overview of all the possibilities enums can offer you.

Similarly to the [`switch`
statement](http://appventure.me/2015/08/20/swift-pattern-matching-in-detail/),
`enum`\'s in Swift may at first glance look like a slightly improved
variant of the well known **C** `enum` statement. I.e. a type that
allows you to define that something is \"one of something more
general\". However, upon close introspection, the particular design
decisions behind Swift\'s enums allow it to be used in a much wider
range of practical scenarios than plain **C** enums. In particular,
they\'re great tools to clearly manifest the intentions of your code.

In this post, we\'ll first look at the syntax and possibilities of using
`enum`, and will then use them in a variety of (hopefully) practical,
real world scenarios to give a better idea of how and when to use them.
We\'ll also look a bit at how enums are being used in the Swift Standard
library.

Before we dive in, here\'s a definition of what `enums` can be. We\'ll
revisit this definition later on:

\"Enums declare types with finite sets of possible states and
accompanying values. With nesting, methods, associated values, and
pattern matching, however, enums can define any hierarchically organized
data.\"

# Diving In

A short overview of how to define and use enums.

## Defining Basic Enums

We\'re working on a game, and the player can move in four directions. So
our player movement is restricted. Obviously, we can use an enum for
that.

``` {.swift noweb-ref="movementenum"}
enum Movement {
case Left
case Right
case Top
case Bottom
}
```

You can then use [various pattern matching
constructs](http://appventure.me/2015/08/20/swift-pattern-matching-in-detail/)
to retrieve the value of a `Movement`, or act upon a specific case:

``` {.swift noweb="strip-export"}
<<movementenum>>
let aMovement = Movement.Left

switch aMovement {
case .Left: print("left")
default: ()
}

if case .Left = aMovement { print("left") }

if aMovement == .Left { print("left") }
```

Note that you don\'t have to specify the actual name of the `enum` (i.e.
`case Movement.Left: print("Left")` in this case. The type checker
figures that out automatically. This is extremely helpful for some of
those convoluted **UIKit** or **AppKit** enums.

## Enum Values

Of course, you may want to have a value assigned to each `enum` case.
This is useful if the `enum` itself indeed relates to something which
can be expressed in a different type. **C** allows you to assign numbers
to `enum cases`. Swift gives you much more flexibility here:

``` {.swift noweb-ref="enumsimplevalues"}
// Mapping to Integer
enum Movement: Int {
    case Left = 0
    case Right = 1
    case Top = 2
    case Bottom = 3
}

// You can also map to strings
enum House: String {
    case Baratheon = "Ours is the Fury"
    case Greyjoy = "We Do Not Sow"
    case Martell = "Unbowed, Unbent, Unbroken"
    case Stark = "Winter is Coming"
    case Tully = "Family, Duty, Honor"
    case Tyrell = "Growing Strong"
}

// Or to floating point (also note the fancy unicode in enum cases)
enum Constants: Double {
    case π = 3.14159
    case e = 2.71828
    case φ = 1.61803398874
    case λ = 1.30357
}
```

For `String` and `Int` types, you can even omit the values and the Swift
compiler will do the right thing:

``` {.swift}
// Mercury = 1, Venus = 2, ... Neptune = 8
enum Planet: Int {
    case Mercury = 1, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune
}

// North = "North", ... West = "West"
enum CompassPoint: String {
    case North, South, East, West
}
```

Swift supports the following types for the value of an enum:

-   Integer
-   Floating Point
-   String
-   Boolean

So you won\'t be able[^1] to use, say, a CGPoint as the value of your
enum.

If you want to access the values, you can do so with the `rawValue`
property:

``` {.swift noweb="strip-export"}
<<enumsimplevalues>>
let bestHouse = House.Stark
print(bestHouse.rawValue)
// prints "Winter is coming"
```

However, there may also be a situation where you want to construct an
`enum case` from an existing raw value. In that case, there\'s a special
initializer for enums:

``` {.swift noweb="strip-export"}
enum Movement: Int {
    case Left = 0
    case Right = 1
    case Top = 2
    case Bottom = 3
}
// creates a movement.Right case, as the raw value for that is 1
let rightMovement = Movement(rawValue: 1)
```

If you use the `rawValue` initializer, keep in mind that it is a
[failable
initializer](https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/Swift_Programming_Language/Declarations.html#//apple_ref/doc/uid/TP40014097-CH34-ID376),
i.e. you get back an
[Optional](http://appventure.me/2014/06/13/swift-optionals-made-simple/),
as the value you\'re using may not map to any case at all, say if you
were to write `Movement(rawValue: 42)`.

This is a very useful feature in case you want to encode low level C
binary representations into something much more readable. As an example,
have a look as this encoding of the **VNode Flags** for [the BSD kqeue
library](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man2/kqueue.2.html):

``` {.swift}
enum VNodeFlags : UInt32 {
    case Delete = 0x00000001
    case Write = 0x00000002
    case Extended = 0x00000004
    case Attrib = 0x00000008
    case Link = 0x00000010
    case Rename = 0x00000020
    case Revoke = 0x00000040
    case None = 0x00000080
}
```

This allows you to use the much nicer looking **Delete** or **Write**
cases, and later on hand the raw value into the **C** function only when
it is really needed.

## Nesting Enums

If you have specific sub type requirements, you can also logically nest
enums in an enum. This allows you to contain specific information on
your enum case within the actual enum. Imagine a character in an RPG.
Each character can have a weapon, all characters have access to the same
set of weapons. All other instances in the game do not have access to
those weapons (they\'re trolls, they just have clubs).

``` {.swift}
enum Character {
  enum Weapon {
    case Bow
    case Sword
    case Lance
    case Dagger
  }
  enum Helmet {
    case Wooden
    case Iron
    case Diamond
  }
  case Thief
  case Warrior
  case Knight
}
```

Now you have a hierachical system to describe the various items that
your character has access to.

``` {.swift}
let character = Character.Thief
let weapon = Character.Weapon.Bow
let helmet = Character.Helmet.Iron
```

## Containing Enums

In a similar vein, you can also embed enums in `structs` or `classes`.
Continuing with our previous example:

``` {.swift}
struct Character {
   enum CharacterType {
    case Thief
    case Warrior
    case Knight
  }
  enum Weapon {
    case Bow
    case Sword
    case Lance
    case Dagger
  }
  let type: CharacterType
  let weapon: Weapon
}

let warrior = Character(type: .Warrior, weapon: .Sword)
```

This, again, helps in keeping related information together.

## Associated Values

Associated values are a fantastic way of attaching additional
information to an `enum case`. Say you\'re writing a trading engine, and
there\'re two different possible trade types. `Buy` and `Sell`. Each of
them would be for a specific stock and amount:

### Simple Example

``` {.swift}
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

``` {.swift noweb-ref="tradetype"}
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

``` {.swift noweb="strip-export"}
<<tradetype>>

let trade = Trade.Buy(stock: "APPL", amount: 500)
if case let Trade.Buy(stock, amount) = trade {
    print("buy \(amount) of \(stock)")
}

```

### Labels

Associated values do not require labels:

``` {.swift}
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

``` {.swift noweb="strip-export"}
<<tradetype>>

let tp = (stock: "TSLA", amount: 100)
let trade = Trade.Sell(tp)

if case let Trade.Sell(stock, amount) = trade {
    print("buy \(amount) of \(stock)")
}
// Prints: "buy 100 of TSLA"
```

This syntax allows you to take `Tuples` as a simple data structure and
later on automatically elevate them into a higher type like a
`enum case`. Imagine an app where a user can configure a Desktop that he
wants to order:

``` {.swift noweb-ref="tupleargs"}
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

``` {.swift noweb="strip-export" noweb-ref="tuplefunc"}
<<tupleargs>>

infix operator <^> { associativity left }

func <^>(a: Config, f: (Config) -> Config) -> Config { 
    return f(a)
}
```

Finally, we can thread through the different configuration steps. This
is particularly helpful if you have many of those steps.

``` {.swift noweb="strip-export"}
<<tuplefunc>>

let config = (0, "", "") <^> selectRAM  <^> selectCPU <^> selectGPU
let aCube = Desktop.Cube(config)

```

### Use Case Examples {#basicexamples}

Associated Values can be used in a variety of ways. As code can tell
more than a thousand words, what follows is a list of short examples in
no particular order.

``` {.swift prologue=""import Foundation""}
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

## Methods and Properties

You can also define methods on an `enum` like so:

``` {.swift}
enum Wearable {
    enum Weight: Int {
        case Light = 1
    }
    enum Armor: Int {
        case Light = 2
    }
    case Helmet(weight: Weight, armor: Armor)
    func attributes() -> (weight: Int, armor: Int) {
       switch self {
         case .Helmet(let w, let a): return (weight: w.rawValue * 2, armor: a.rawValue * 4)
       }
    }
}
let woodenHelmetProps = Wearable.Helmet(weight: .Light, armor: .Light).attributes()
print (woodenHelmetProps)
// prints "(2, 8)"
```

Methods on enums exist for every `enum case`. So if you want to have
specific code for specific cases, you need a branch or a switch to
determine the correct code path.

``` {.swift}
enum Device { 
    case iPad, iPhone, AppleTV, AppleWatch 
    func introduced() -> String {
       switch self {
         case .AppleTV: return "\(self) was introduced 2006"
         case .iPhone: return "\(self) was introduced 2007"
         case .iPad: return "\(self) was introduced 2010"
         case .AppleWatch: return "\(self) was introduced 2014"
       }
    }
}
print (Device.iPhone.introduced())
// prints: "iPhone was introduced 2007"
```

### Properties

Even though you can\'t add actual stored properties to an `enum`, you
can still create computed properties. Their contents, of course, can be
based on the **enum value** or **enum associated value**.

``` {.swift}
enum Device {
  case iPad, iPhone
  var year: Int {
    switch self {
        case .iPhone: return 2007
        case .iPad: return 2010
     }
  }
}
```

### Static Methods

You can also have static methods on `enums`, i.e. in order to create an
`enum` from a non-value type. In this example we want to get the proper
Apple Device for the wrong name that\'s sometimes used by people.

``` {.swift}
enum Device { 
    case AppleWatch 
    static func fromSlang(term: String) -> Device? {
      if term == "iWatch" {
          return .AppleWatch
      }
      return nil
    }
}
print (Device.fromSlang(term:"iWatch")!)
```

### Mutating Methods

Methods can be declared `mutating`. They\'re then allowed to change the
`case` of the underlying `self` parameter [^3]:

``` {.swift}
enum TriStateSwitch {
    case Off, Low, High
    mutating func next() {
        switch self {
        case .Off:
            self = .Low
        case .Low:
            self = .High
        case High:
            self = .Off
        }
    }
}
var ovenLight = TriStateSwitch.Low
ovenLight.next()
// ovenLight is now equal to .High
ovenLight.next()
// ovenLight is now equal to .Off
```

## To Recap

We\'ve finished our overview of the basic use cases of Swift\'s `enum`
syntax. Before we head into the advanced usage, lets have another look
at the explanation we gave at the beginning and see if it became clearer
now.

> Enums declare types with finite sets of possible states and
> accompanying values. With nesting, methods, associated values, and
> pattern matching, however, enums can define any hierarchically
> organized data.

The definition is a lot clearer now. Indeed, if we add associated values
and nesting, an `enum case` is like a closed, simplified `struct`. The
advantage over structs being the ability to encode categorization and
hierachy:

``` {.swift}
// Struct Example
struct Point { let x: Int, y: Int }
struct Rect { let x: Int, y: Int, width: Int, height: Int }

// Enum Example
enum GeometricEntity {
   case Point(x: Int, y: Int)
   case Rect(x: Int, y: Int, width: Int, height: Int)
}
```

The addition of methods and static methods allow us to attach
functionality to an `enum` without having to resort to free functions
[^4]

``` {.swift}
// C-Like example
enum Trade {
   case Buy
   case Sell
}
func order(trade: Trade)

// Swift Enum example
enum Trade {
   case Buy
   case Sell
   func order() {}
}
```

# Advanced Enum Usage

## Protocols

I already mentioned the similarity between the `structs` and `enums`. In
addition to the ability to add methods, Swift also allows you to use
**Protocols** and **Protocol Extensions** with enums.

Swift protocols define an interface or type that other structures can
conform to. In this case our `enum` can conform to it. For a start,
let\'s take a protocol from the Swift standard library.

`CustomStringConvertible` is a type with a customized textual
representation suitable for printing purposes:

``` {.swift}
protocol CustomStringConvertible {
  var description: String { get }
}
```

It has only one requirement, namely a **getter** for a string. We can
implement this on an enum quite easily:

``` {.swift}
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

``` {.swift noweb-ref="accountcompatible"}
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

``` {#feature-image .swift noweb="strip-export" noweb-ref="accountthing" export-image="true" export-template="template4"}
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

``` {.swift noweb="strip-export"}
<<accountcompatible>>
<<accountthing>>
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

## Extensions

As we just saw, enums can also be extended. The most apparent use case
for this is keeping `enum cases` and `methods` separate, so that a
reader of your code can easily digest the `enum` and after that move on
to the methods:

``` {.swift noweb-ref="entities"}
enum Entities {
    case Soldier(x: Int, y: Int)
    case Tank(x: Int, y: Int)
    case Player(x: Int, y: Int)
}
```

Now, we can extend this `enum` with methods:

``` {.swift noweb="strip-export" prologue=""import CoreGraphics""}
<<entities>>
extension Entities {
   mutating func move(dist: CGVector) {}
   mutating func attack() {}
}
```

You can also write extensions to add support for a specific protocol:

``` {.swift noweb="strip-export"}
<<entities>>
extension Entities: CustomStringConvertible {
  var description: String {
    switch self {
       case let .Soldier(x, y): return "\(x), \(y)"
       case let .Tank(x, y): return "\(x), \(y)"
       case let .Player(x, y): return "\(x), \(y)"
    }
  }
}
```

## Generic Enums

Enums can also be defined over generic parameters. You\'d use them to
adapt the associated values of an enum. The simplest example comes
straight from the Swift standard library, namely the `Optional` type.
You probably mostly use it with **optional chaining** (`?`), `if let`,
`guard let`, or `switch`, but syntactically you can also use Optionals
like so:

``` {.swift}
let aValue = Optional<Int>.some(5)
let noValue = Optional<Int>.none
if noValue == Optional.none { print("No value") }
```

This is the direct usage of an Optional without any of the syntactic
sugar that Swift adds in order to make your life a tremendous amount
easier. If you look at the code above, you can probably guess that
internally the `Optional` is defined as follows [^5]:

``` {.swift}
// Simplified implementation of Swift's Optional
enum MyOptional<T> {
  case Some(T)
  case None
}
```

What\'s special here is, that the enum\'s **associated values** take the
type of the generic parameter `T`, so that optionals can be built for
any kind you wish to return.

Enums can have multiple generic parameters. Take the well-known
**Either** type which is not part of Swift\'s standard library but
implemented in many open source libraries as well as prevalent in other
functional programming languages like Haskell or F\#. The idea is that
instead of just returning a value or no value (née Optional) you\'d
return either the successful value or something else (probably an error
value).

``` {.swift}
// The well-known either type is, of course, an enum that allows you to return either
// value one (say, a successful value) or value two (say an error) from a function
enum Either<T1, T2> {
  case Left(T1)
  case Right(T2)
}
```

Finally, all the type constraints that work on classes and structs in
Swift also work on enums.

``` {.swift}
// Totally nonsensical example. A bag that is either full (has an array with contents)
// or empty.
enum Bag<T: Sequence> where T.Iterator.Element==Equatable {
    case Empty
    case Full(contents: T)
}
```

## Recursive / Indirect Types

Indirect types are a new addition that came with Swift 2.0. They allow
you to define enums where the associated value of a `case` is the very
same enum again. As an example, consider that you want to define a file
system representations with files and folders containing files. If
**File** and **Folder** were enum cases, then the **Folder** case would
need to have an array of **File** cases as it\'s associated value. Since
this is a recursive operation, the compiler has to make special
preparations for it. Quoting from the Swift documentation:

> Enums and cases can be marked indirect, which causes the associated
> value for the enum to be stored indirectly, allowing for recursive
> data structures to be defined.

So to implement our **FileNode** `enum`, we\'d have to write it like
this:

``` {.swift}
enum FileNode {
  case File(name: String)
  indirect case Folder(name: String, files: [FileNode])
}
```

The `indirect` keyword tells the compiler to handle this `enum case`
indirectly. You can also add the keyword for the whole enum. [As an
example imagine mapping a binary
tree](http://airspeedvelocity.net/2015/07/22/a-persistent-tree-using-indirect-enums-in-swift/):

``` {.swift}
indirect enum Tree<Element: Comparable> {
    case Empty
    case Node(Tree<Element>,Element,Tree<Element>)
}
```

This is a very powerful feature that allows you to map complex
relationships in a very clean way with an enum.

## Using Custom Data Types as Enum Values

If we neglect associated values, then the value of an enum can only be
an Integer, Floating Point, String, or Boolean. If you need to support
something else, you can do so by implementing the
`StringLiteralConvertible` protocol which allows the type in question to
be serialized to and from String.

As an example, imagine you\'d like to store the different screen sizes
of iOS devices in an enum:

``` {.swift noweb="strip-export" prologue=""import Foundation""}
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

``` {.swift prologue=""import Foundation; import UIKit"" noweb-ref="cgsizenum"}
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

``` {.swift noweb-ref="cgsizeenum2" prologue=""import Foundation""}
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

``` {.swift noweb="strip-export" prologue=""import Foundation; func CGSizeFromString(a: String) -> CGSize { return NSSizeFromString(a)}""}
<<cgsizenum>>
<<cgsizeenum2>>
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

``` {.swift}
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

## Custom Initializers

In the context of **static methods** on enums, we already mentioned that
they can be used as a way to conveniently create an enum from different
data. The example we had was for returning the proper Apple device for
the wrong worded version that the press sometimes uses:

``` {.swift}
enum Device { 
    case AppleWatch 
    static func fromSlang(term: String) -> Device? {
      if term == "iWatch" {
          return .AppleWatch
      }
      return nil
    }
}
```

Instead of using a static method for this, we can also use a custom
initializer. The main difference compared to a Swift `struct` or `class`
is that within an `enum` initializer, you need to set the implicit
`self` property to the correct case.

``` {.swift}
enum Device { 
    case AppleWatch 
    init?(term: String) {
      if term == "iWatch" {
          self = .AppleWatch
      } else {
          return nil
      }
    }
}
```

In the above example, we used a failable initializer. However, normal
initializers work just as well:

``` {.swift}
enum NumberCategory {
   case Small
   case Medium
   case Big
   case Huge
   init(number n: Int) {
        if n < 10000 { self = .Small }
        else if n < 1000000 { self = .Medium }
        else if n < 100000000 { self = .Big }
        else { self = .Huge }
   }
}
let aNumber = NumberCategory(number: 100)
print(aNumber)
// prints: "Small"
```

## Iterating over Enum Cases

One particularly often asked question with regards to enums is how to
iterate over all cases. Sadly, enums do not conform to the
`SequenceType` protocol, so there is no official way to do this.
Depending on the type of enum that you have, it might be easier or more
difficult to implement a way of iterating over all cases. [There\'s a
very good overview in this StackOverflow
thread.](http://stackoverflow.com/questions/24007461/how-to-enumerate-an-enum-with-string-type)
Also, there\'s so much variation in the replies that it wouldn\'t to
listing only some of the examples here. On the other hand, listing all
the examples would be too much.

## Objective-C support

Integer-based enums such as
`enum Bit: Int { case Zero = 0; case One = 1}` can be bridged to
Objective-c via the `@objc` flag. However once you venture away from
integers (say `String`) or start using **associated values** you can\'t
use enums from within Objective-C.

[There\'s a hidden protocol called `_ObjectiveCBridgeable` which
apparently](http://nshint.io/blog/2015/10/07/easy-cast-with-_ObjectiveCBridgeable/?utm_campaign%3DSwift%252BSandbox&utm_medium%3Demail&utm_source%3DSwift_Sandbox_11)
allows defining the proper methods so that Swift can convert things back
and forth from Objective-C, but I suppose there\'s a reason why it is
hidden. Nevertheless, theoretically it should allow you to add support
for bridging an `enum` (including associated values) to Objective-C.

You don\'t have to do it that way though. Add two methods to your
`enum`, define a type replacement on the `@objc` side, and you can move
`enums` back and forth just fine, without having to conform to private
protocols:

``` {.swift prologue=""import Foundation""}
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

## Enum Internals

[Erica Sadun wrote a great blog post explaining the
internals](http://ericasadun.com/2015/07/12/swift-enumerations-or-how-to-annoy-tom/)
of `enums` when you look at the bits and bytes behind the glossy syntax.
This is something you should never do in production code, but still
interesting to know. We\'ll only mention one of her findings here, but
go and read her original article for more.

> Enums are typically one byte long. \[...\] If you want to get very
> very silly, you can build an enumeration with hundreds of cases, in
> which case the enum takes up 2 or more bytes depending on the minimum
> bit count needed.

# Enums in the Swift Standard Library

Before we go on and explore various use cases for enums in your
projects, it might be tempting to see some of the enums being used in
the Swift standard library, so let\'s have a look.

[**Bit**](https://developer.apple.com/library/watchos/documentation/Swift/Reference/Swift_Bit_Enumeration/index.html#//apple_ref/swift/enum/s:OSs3Bit)
The `Bit` enum can have two possible values, **One**, and **Zero**. It
is used as the `Index` type for `CollectionOfOne<T>`.

[**FloatingPointClassification**](https://developer.apple.com/library/watchos/documentation/Swift/Reference/Swift_FloatingPointClassification_Enumeration/index.html#//apple_ref/swift/enumelt/FloatingPointClassification/s:FOSs27FloatingPointClassification12SignalingNaNFMS_S_)
This enum defines the set of possible IEEE 754 \"classes\", like
`NegativeInfinity`, `PositiveZero`, or `SignalingNaN`.

[**Mirror.AncestorRepresentation**](https://developer.apple.com/library/watchos/documentation/Swift/Reference/Swift_Mirror-AncestorRepresentation_Enumeration/index.html#//apple_ref/swift/enum/s:OVSs6Mirror22AncestorRepresentation),
and
[**Mirror.DisplayStyle**](https://developer.apple.com/library/watchos/documentation/Swift/Reference/Swift_Mirror-DisplayStyle_Enumeration/index.html#//apple_ref/swift/enum/s:OVSs6Mirror12DisplayStyle)
These two are used in the context of the Swift Reflection API.

[**Optional**](https://developer.apple.com/library/watchos/documentation/Swift/Reference/Swift_Optional_Enumeration/index.html#//apple_ref/swift/enum/s:Sq)
Not much to say here

[**Process**](https://developer.apple.com/library/watchos/documentation/Swift/Reference/Swift_Process_Enumeration/index.html#//apple_ref/swift/enum/s:OSs7Process)
The Process enum contains the command line arguments of the current
process (`Process.argc`, `Process.arguments`). This is a particularly
interesting `enum` as it used to be a `struct` in Swift 1.0.

# Practical Use Cases

We\'ve already seen a couple of useful `enums` in the [previous feature
descriptions.](#basicexamples) Examples would be `Optional`, `Either`,
`FileNode`, or the binary tree. However, there\'re many more scenarios
where using an `enum` wins over a `struct` or `class`. Usually, if your
problem domain can be divided into a finite set of distinctive
categories, an `enum` may be the right choice. Even only two cases are a
perfectly valid scenario for an enum, as the Optional and Either types
show.

Here, then, are some more examples of practical `enum` usage to fuel
your creativity.

## Error Handling {#errortype}

One of the prime examples of Enum usage in Swift is, of course, the new
error handling in Swift 2.0. Your throwing function can throw anything
which conforms to the empty `ErrorType` protocol. As the Swift
documentation succinctly observes:

> Swift enumerations are particularly well suited to modeling a group of
> related error conditions, with associated values allowing for
> additional information about the nature of an error to be
> communicated.

As an example, have a look at the popular [JSON Decoding library
Argo](https://github.com/thoughtbot/Argo). When their JSON Decoding
fails, it can fail due to two primary reasons.

1.  The JSON Data lacks a key which the end model requires (say your
    model has a property `username` and somehow the JSON lacks that)
2.  There\'s a type mismatch. Say instead of a String the `username`
    property in the JSON contains an `NSNull` [^6].

In addition to that, Argo also includes a custom error for anything not
fitting in these two categories above. Their `ErrorType enum` looks like
this:

``` {.swift noweb-ref="argo"}
enum DecodeError: Error {
  case TypeMismatch(expected: String, actual: String)
  case MissingKey(String)
  case Custom(String)
}
```

All cases have associated values that contain additional information
about the error in question.

A more general `ErrorType` for complete HTTP / REST API handling could
look like this:

``` {.swift noweb="strip-export" prologue=""import Foundation""}
<<argo>>
enum APIError : Error {
    // Can't connect to the server (maybe offline?)
    case ConnectionError(error: NSError)
    // The server responded with a non 200 status code
    case ServerError(statusCode: Int, error: NSError)
    // We got no data (0 bytes) back from the server
    case NoDataError
    // The server response can't be converted from JSON to a Dictionary
    case JSONSerializationError(error: Error)
    // The Argo decoding Failed
    case JSONMappingError(converstionError: DecodeError)
}
```

This `ErrorType` implements the complete REST Stack up to the point
where your app would get the completely decoded native `struct` or
`class` object.

If you look closely, you\'ll see that within the `JSONMappingError`,
we\'re wrapping the **Argo** `DecodeError` into our `APIError` type as
we\'re still using Argo for the actual JSON decoding.

More information on `ErrorType` and more `enum` examples in this context
can be found in the official documentation
[here](https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/Swift_Programming_Language/ErrorHandling.html).

## Observer Pattern

There\'re various ways of modelling observation in Swift. If you include
`@objc` compatibility, you can use `NSNotificationCenter` or **KVO**.
Even if not, the `didSet` syntax makes it easy to implement simple
observation. Enums can be used here in order to make the type of change
that happens to the observed object clearer. Imagine collection
observation. If we think about it, we only have a couple of possible
cases: One or more items are inserted, one or more items are deleted,
one or more items are updated. This sounds like a job for an enum:

``` {.swift}
enum Change {
     case Insertion(items: [Item])
     case Deletion(items: [Item])
     case Update(items: [Item])
}
```

Then, the observing object can receive the concrete information of what
happened in a very clean way. This could easily be extended by adding
**oldValue** and **newValue**, too.

## Status Codes

If you\'re working with an outside system which uses status codes (or
error codes) to convey information, like HTTP Status Codes, enums are
obviously a great way to encode the information. [^7]

``` {.swift}
enum HttpError: String {
  case Code400 = "Bad Request"
  case Code401 = "Unauthorized"
  case Code402 = "Payment Required"
  case Code403 = "Forbidden"
  case Code404 = "Not Found"
}
```

## Map Result Types

Enums are also frequently used to map the result of JSON parsing into
the Swift type system. Here\'s a short example of this:

``` {.swift}
enum JSON {
    case JSONString(Swift.String)
    case JSONNumber(Double)
    case JSONObject([String : JSONValue])
    case JSONArray([JSONValue])
    case JSONBool(Bool)
    case JSONNull
}
```

Similarly, if you\'re parsing something else, you may use the very same
structure to convert your parsing results into Swift types. This also
makes perfect sense to only do it during the parsing / processing step
and then taking the `JSON enum` representation and converting it into
one of your application\'s internal `class` or `struct` types.

## UIKit Identifiers

Enums can be used to map reuse identifiers or storyboard identifiers
from stringly typed information to something the type checker can
understand. Imagine a UITableView with different prototype cells:

``` {.swift}
enum CellType: String {
    case ButtonValueCell = "ButtonValueCell"
    case UnitEditCell = "UnitEditCell"
    case LabelCell = "LabelCell"
    case ResultLabelCell = "ResultLabelCell"
}
```

## Units

Units and unit conversion are another nice use case for enums. You can
map the units and their respective values and then add methods to do
automatic conversions. Here\'s an oversimplified example.

``` {.swift}
enum Liquid: Float {
  case ml = 1.0
  case l = 1000.0
  func convert(amount: Float, to: Liquid) -> Float {
      if self.rawValue < to.rawValue {
         return (self.rawValue / to.rawValue) * amount
      } else {
         return (self.rawValue * to.rawValue) * amount
      }
  }
}
// Convert liters to milliliters
print (Liquid.l.convert(amount: 5, to: Liquid.ml))
```

Another example of this would be Currency conversion. Also, mathematical
symbols (such as degrees vs radians) can benefit from this.

## Games

Enums are a great use case for games, where many entities on screen
belong to a specific family of items (enemies, obstacles, textures,
...). In comparison to native iOS or Mac apps, games oftentimes are a
tabula rasa. Meaning you invent a new world with new relationships and
new kinds of objects, whereas on iOS or OSX you\'re using a well-defined
world of UIButtons, UITableViews, UITableViewCells or NSStackView.

What\'s more, since Enums can conform to protocols, you can utilize
protocol extensions and protocol based programming to add functionality
to the various enums that you defined for your game. Here\'s a short
example that tries to display such a hierarchy:

``` {.swift}
enum FlyingBeast { case Dragon, Hippogriff, Gargoyle }
enum Horde { case Ork, Troll }
enum Player { case Mage, Warrior, Barbarian }
enum NPC { case Vendor, Blacksmith }
enum Element { case Tree, Fence, Stone }

protocol Hurtable {}
protocol Killable {}
protocol Flying {}
protocol Attacking {}
protocol Obstacle {}

extension FlyingBeast: Hurtable, Killable, Flying, Attacking {}
extension Horde: Hurtable, Killable, Attacking {}
extension Player: Hurtable, Obstacle {}
extension NPC: Hurtable {}
extension Element: Obstacle {}
```

## Battling stringly typed code

In bigger Xcode projects, you\'re quickly accumulating lots of resources
which are accessed by string. We\'ve already mentioned reuse identifiers
and storyboard identifiers above, but there\'s also: Images, Segues,
Nibs, Fonts, and other resources. Oftentimes, those resources can be
grouped into several distinct sets. If that\'s the case, a `String`
typed `enum` is a good way of having the compiler check this for you.

``` {.swift}
enum DetailViewImages: String {
  case Background = "bg1.png"
  case Sidebar = "sbg.png"
  case ActionButton1 = "btn1_1.png"
  case ActionButton2 = "btn2_1.png"
}
```

For iOS users, [there\'s also R.swift which auto generates `structs` for
most of those use cases.](https://github.com/mac-cain13/R.swift)
Sometimes you may need more control though (or you may be on a Mac [^8])

## API Endpoints

Rest APIs are a great use case for enums. They\'re naturally grouped,
they\'re limited to a finite set of APIs, and they may have additional
query or named parameters which can be modelled through associated
values.

Take, for example, a look at a simplified version of the [**Instagram
API**](https://instagram.com/developer/endpoints/media/)

``` {.swift}
enum Instagram {
  enum Media {
    case Popular
    case Shortcode(id: String)
    case Search(lat: Float, min_timestamp: Int, lng: Float, max_timestamp: Int, distance: Int)
  }
  enum Users {
    case User(id: String)
    case Feed
    case Recent(id: String)
  }
}
```

[Ash Furrow\'s **Moya** library](https://github.com/Moya/Moya) is based
around this idea of using `enums` to map rest endpoints.

## Linked Lists

[Airspeed Velocity has a great writeup on how to implement a Linked List
with an `enum`.](http://airspeedvelocity.net/tag/swift/) Most of the
code in his post goes far beyond enums and touches a lot of interesting
topics [^9], but the basis of his linked list looks kinda like this (I
simplified it a bit):

``` {.swift}
enum List {
    case End
    indirect case Node(Int, next: List)
}
```

Each `Node case` points to the next case, and by using an `enum` instead
of something else, you don\'t have to use an optional for the `next`
value to signify the termination of the list.

Airspeed Velocity also wrote a great post about the implementation of a
red black tree with indirect Swift enums, so while you\'re already
reading his blog, [you may just as well also read this
one.](http://airspeedvelocity.net/2015/07/22/a-persistent-tree-using-indirect-enums-in-swift/)

## Settings Dictionaries {#settingsdics}

[This is a very, very smart solution that Erica Sadun came up
with](http://ericasadun.com/2015/10/19/sets-vs-dictionaries-smackdown-in-swiftlang/?utm_campaign%3DSwift%252BSandbox&utm_medium%3Demail&utm_source%3DSwift_Sandbox_12).
Basically whenever you\'d use a dictionary of attribute keys as a way to
configure an item, you\'d instead use a `Set` of enums with associated
values. That way, the type checker can confirm that your configuration
values are of the correct type.

[For more details, and proper examples, check out her original blog
post.](http://ericasadun.com/2015/10/19/sets-vs-dictionaries-smackdown-in-swiftlang/?utm_campaign%3DSwift%252BSandbox&utm_medium%3Demail&utm_source%3DSwift_Sandbox_12)

# Limitations

We\'re ending this post, again, with a list of things that don\'t work
yet with enums.

## Retrieving Associated Values

[David Owens makes the case that the current way of associated value
retrieval is
unwieldy.](http://owensd.io/2015/09/15/associated-enum-cases-as-types.html)
I encourage you to follow the link and read the post, but here\'s the
gist: In order to retrieve the associated values from an enum, you have
to use pattern matching. However, associated values are effectively
tuples which were attached to the enum case. Tuples, on the other hand,
can be deconstructed in a much simpler way simply by using
`.keyword or .0`. i.e:

``` {.swift}
// Enums
enum Ex { case Mode(ab: Int, cd: Int) }
if case Ex.Mode(let ab, let cd) = Ex.Mode(ab: 4, cd: 5) {
    print(ab)
}
// vs tuples:
let tp = (ab: 4, cd: 5)
print(tp.ab)
```

If you also feel that this is how we should be able to deconstruct
enums, there\'s a rdar for you:
[rdar://22704262](http://openradar.me/22704262)

## Equatable

Enums with associated values do not conform to the equatable protocol.
That\'s a pity because it makes a lot of things much more cumbersome and
verbose than they need to be. The underlying reason is probably that
associated values are just tuples internally and tuples do not conform
to equatable. However, for a limited subset of cases, namely those where
all associated value / tuple types conform to equatable, I think the
default case should be that the compiler automatically also generates
the equatable extension.

``` {.swift}
// Int and String are Equatable, so case Ex should also be equatable.
enum Ex { case Mode(ab: Int, cd: String) }

// Swift could auto-generate this func
func == (lhs: Ex.Mode, rhs: Ex.Mode) -> Bool {
    switch (lhs, rhs) {
       case (.Mode(let a, let b), .Mode(let c, let d)):
           return a == c && b == d
       default:
           return false
    }
}
```

## Tuples

The biggest issue is, [again, Tuple
support](http://appventure.me/2015/07/19/tuples-swift-advanced-usage-best-practices/).
I love tuples, they make many things easier, but they\'re currently
under-documented and cannot be used in many scenarios. In terms of
enums, you can\'t have tuples as the enum value:

``` {.swift}
enum Devices: (intro: Int, name: String) {
  case iPhone = (intro: 2007, name: "iPhone")
  case AppleTV = (intro: 2006, name: "Apple TV")
  case AppleWatch = (intro: 2014, name: "Apple Watch")
}
```

This may not look like the best example, but once you start using enums,
you\'ll often end up in situations where you\'d like to be able to do
something like the above.

## Enumerating Enum Cases

We\'ve already discussed this above. There\'s currently no good way to
get a collection of all the cases in an enum so you can iterate over
them.

## Default Associated Values

Another thing which you may run into is that associated values are
always types but you can\'t set a default value for those types. Imagine
such an example:

``` {.swift}
enum Characters {
  case Mage(health: Int = 70, magic: Int = 100, strength: Int = 30)
  case Warrior(health: Int = 100, magic: Int = 0, strength: Int = 100)
  case Neophyte(health: Int = 50, magic: Int = 20, strength: Int = 80)
}
```

You could still create new cases with different values, but the default
settings for your character would be mapped.

# Changes

****10/26/2015****

-   Added additional limitation examples (Equatable & Retrieving
    associated values)
-   *Added Erica Sadun\'s Set with Associated Enums example*

****10/22/2015****

-   Incorporated PR [\#6 from
    @mabidakun](https://github.com/terhechte/appventure-blog/pull/6).
-   Added internal links
-   Split up the account example into two easier to digest snippets.

****10/21/2015****

-   Incorporated PR [\#4 from
    @blixt](https://github.com/terhechte/appventure-blog/pull/4) and
    [\#2 from
    @kandelvijayavolare](https://github.com/terhechte/appventure-blog/pull/2)
    and [\#3 from
    @sriniram](https://github.com/terhechte/appventure-blog/pull/3) and
    [\#5 from
    @SixFiveSoftware](https://github.com/terhechte/appventure-blog/pull/5)
-   Added calling code for the Account example.
-   Added `ErrorType` example

[^1]: Except by jumping through some hoops, see below

[^2]: This is a simplified implementation for demo purposes. In reality
    you\'d write this with optionals and a reverse argument order. Have
    a look at popular functional programming libraries like
    [Swiftz](https://github.com/typelift/Swiftz) or
    [Dollar](https://github.com/ankurp/Dollar.swift)

[^3]: This example stems straight [from Apple\'s Swift
    documentation](https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/Swift_Programming_Language/Methods.html#//apple_ref/doc/uid/TP40014097-CH15-ID234)

[^4]: Which make it oftentimes very difficult to discover them

[^5]: This is a simplified version, of course. Swift adds a lot of sugar
    for you

[^6]: If you ever used JSON in an app, you may well have run into this
    issue once

[^7]: Btw. You can\'t use only numbers as enum case names, so `case 400`
    does not work

[^8]: Although Mac support for R.swift seems to be forthcoming

[^9]: Translated: Go there, read it