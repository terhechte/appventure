[frontMatter]
title = "Custom Initializers"
tags = ["enum", "init"]
created = "2019-03-01 16:29:51"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Custom Initializers

Imagine you'd want to initialize an `enum` with custom data. In our example
we have a `Device` enum that represents Apple devices and we'd like to 
also initialize them with non-standard names. Here's the `enum`:

``` Swift
enum Device {
  case appleWatch
}
```

Now if a user accidentally enters `iWatch` as their device, we still want to map this
to the correct `AppleWatch` case. To do that, we will implement a custom initializer
that sets `self` to the correct type:

``` Swift
enum Device { 
    case appleWatch 
    init?(term: String) {
      if term == "iWatch" {
          self = .appleWatch
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
   case small
   case medium
   case big
   case huge

   init(number n: Int) {
        if n < 10000 { self = .small }
        else if n < 1000000 { self = .medium }
        else if n < 100000000 { self = .big }
        else { self = .huge }
   }
}
```

