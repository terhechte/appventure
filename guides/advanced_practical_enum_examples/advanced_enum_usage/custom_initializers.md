[frontMatter]
title = "Custom Initializers"
tags = []
created = "2019-03-01 16:29:51"
description = ""
published = false

---

# Custom Initializers

In the context of **static methods** on enums, we already mentioned that
they can be used as a way to conveniently create an enum from different
data. The example we had was for returning the proper Apple device for
the wrong worded version that the press sometimes uses:

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
```

Instead of using a static method for this, we can also use a custom
initializer. The main difference compared to a Swift `struct` or `class`
is that within an `enum` initializer, you need to set the implicit
`self` property to the correct case.

``` Swift
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

``` Swift
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

