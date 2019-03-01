[frontMatter]
title = "Limitations"
tags = []
created = "2019-03-01 16:31:41"
description = ""
published = false

---

# Limitations

## Tuples

The biggest issue is, [again, Tuple
support](http://appventure.me/2015/07/19/tuples-swift-advanced-usage-best-practices/).
I love tuples, they make many things easier, but they\'re currently
under-documented and cannot be used in many scenarios. In terms of
enums, you can\'t have tuples as the enum value:

``` Swift
enum Devices: (intro: Int, name: String) {
  case iPhone = (intro: 2007, name: "iPhone")
  case AppleTV = (intro: 2006, name: "Apple TV")
  case AppleWatch = (intro: 2014, name: "Apple Watch")
}
```

This may not look like the best example, but once you start using enums,
you\'ll often end up in situations where you\'d like to be able to do
something like the above.

## Default Associated Values

Another thing which you may run into is that associated values are
always types but you can\'t set a default value for those types. Imagine
such an example:

``` Swift
enum Characters {
  case Mage(health: Int = 70, magic: Int = 100, strength: Int = 30)
  case Warrior(health: Int = 100, magic: Int = 0, strength: Int = 100)
  case Neophyte(health: Int = 50, magic: Int = 20, strength: Int = 80)
}
```

You could still create new cases with different values, but the default
settings for your character would be mapped.
