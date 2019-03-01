[frontMatter]
title = "Methods and Properties"
tags = []
created = "2019-03-01 16:29:51"
description = ""
published = false

---

# Methods and Properties

You can also define methods on an `enum` like so:

``` Swift
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

``` Swift
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

``` Swift
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

``` Swift
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

``` Swift
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
