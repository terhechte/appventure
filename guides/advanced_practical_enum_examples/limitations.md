[frontMatter]
title = "Limitations"
tags = []
created = "2019-03-01 16:31:41"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Limitations

## Tuples

The biggest issue is, Tuple support.
I love tuples, they make many things easier, but they\'re currently
under-documented and cannot be used in many scenarios. In terms of
enums, you can\'t have tuples as the enum value:

``` Swift
enum Devices: (intro: Int, name: String) {
  case iPhone = (intro: 2007, name: "iPhone")
  case appleTV = (intro: 2006, name: "Apple TV")
  case appleWatch = (intro: 2014, name: "Apple Watch")
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
  case mage(health: Int = 70, magic: Int = 100, strength: Int = 30)
  case warrior(health: Int = 100, magic: Int = 0, strength: Int = 100)
  case neophyte(health: Int = 50, magic: Int = 20, strength: Int = 80)
}
```

You could still create new cases with different values, but the default
settings for your character would be mapped.
