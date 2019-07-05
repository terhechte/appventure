[frontMatter]
title = "write code that only runs on macOS?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# How do I write code that only runs on macOS?

You can implement conditional code via the new `targetEnvironment(UIKitForMac` directive:

## Compile code only on the macOS target

``` swift
#if targetEnvironment(UIKitForMac)
  let toolbar = NSToolbar(identifier: "MyToolbar")
#endif
```

## Compile code only on the iOS target

``` swift
#if !targetEnvironment(UIKitForMac)
  import ARKit
#endif
```
