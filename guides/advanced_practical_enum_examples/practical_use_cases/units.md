[frontMatter]
title = "UIKit Identifiers"
tags = []
created = "2019-03-01 16:31:41"
description = ""
published = false

---

# Units

Units and unit conversion are another nice use case for enums. You can
map the units and their respective values and then add methods to do
automatic conversions. Here\'s an oversimplified example.

``` Swift
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
