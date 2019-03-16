[frontMatter]
title = "Methods and Properties"
tags = ["enum", "property", "method"]
created = "2019-03-01 16:29:51"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Methods and Properties

Swift `enum` types can have methods and properties attached to them. This works exactly like you'd do it for
`class` or `struct` types. Here is a very simple example:

``` Swift
enum Transportation {
  case car(Int)
  case train(Int)

  func distance() -> String {
    switch self {
      case .car(let miles): return "\(miles) miles by car"
      case .train(let miles): return "\(miles) miles by train"
    }
  }
}
```

The main difference to `struct` or `class` types is that you can `switch` on `self` within the method
in order to calculate the output.

Here is another, more involved, example where we use the `enum values` to determine the numerical attributes of a character in a method.

``` Swift
enum Wearable {
    enum Weight: Int {
        case light = 1
    }
    enum Armor: Int {
        case light = 2
    }
    case helmet(weight: Weight, armor: Armor)

    func attributes() -> (weight: Int, armor: Int) {
       switch self {
         case .helmet(let w, let a): 
            return (weight: w.rawValue * 2, armor: a.rawValue * 4)
       }
    }
}
let woodenHelmetProps = Wearable.helmet(weight: .light, armor: .light)
    .attributes()
```

### Properties

Enums don't allow for adding stored properties. This means the following does not work:

``` Swift
enum Device {
  case iPad
  case iPhone
  
  let introduced: Int
}
```

Here, we'd like to store an Apple device together with the year when
it was introduced. However, this does not compile.

Even though you can\'t add actual stored properties to an `enum`, you
can still create computed properties. Their contents, of course, can be
based on the **enum value** or **enum associated value**. They're read-only though.

``` Swift
enum Device {
  case iPad,
  case iPhone

  var introduced: Int {
    switch self {
        case .iPhone: return 2007
        case .iPad: return 2010
     }
  }
}
```

This works great as the year of the introduction of an Apple device never changes.
You couldn't use this if you'd like to store mutable / changing information. In those cases
you'd always use `associated values`:

``` Swift
enum Character {
  case wizard(name: String, level: Int)
  case warior(name: String, level: Int)
}
```

Also, you can always still add properties for easy retrieval of the `associated value`:

``` Swift
extension Character {
  var level: Int {
    switch self {
      case .wizard(_, let level): return level
      case .warior(_, let level): return level
    }
  }
}
```

### Static Methods

You can also have static methods on `enums`, i.e. in order to create an
`enum` from a non-value type. 

Static methods are methods you can call on the name of the type instead of
a specific instance of the type. In this example we add a static method
to our `enum Device` which returns the most recently released device:

``` Swift
enum Device {
  static var newestDevice: Device {
    return .appleWatch
  }

  case iPad,
  case iPhone
  case appleWatch
}
```

### Mutating Methods

Methods can be declared `mutating`. They\'re then allowed to change the
`case` of the underlying `self` parameter. Imagine a lamp that has three states:
`off`, `low`, `bright` where `low` is low light and `bright` a very strong light.
We want a function called `next` that switches to the next state:

``` Swift
enum TriStateSwitch {
    case off, low, bright
    mutating func next() {
        switch self {
        case .off:
            self = low
        case .low:
            self = .bright
        case high:
            self = off
        }
    }
}
var ovenLight = TriStateSwitch.low
ovenLight.next()
// ovenLight is now equal to .bright
ovenLight.next()
// ovenLight is now equal to .off
```

Before we look at advanced `enum` usage, we'll do a brief recap of what we've 
learned in this section so far.
