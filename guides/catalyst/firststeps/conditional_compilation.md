[frontMatter]
title = "Conditional Compilation"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---

If you want to compile code that runs only on macOS, you can do that by using the following, new compile time attribute:

``` swift
#if targetEnvironment(UIKitForMac)
  let toolbar = NSToolbar(identifier: "MyToolbar")
#endif
```

Obviously, to do it the other way around, you just inverse it:

``` swift
#if !targetEnvironment(UIKitForMac)
  import ARKit
#endif
```
