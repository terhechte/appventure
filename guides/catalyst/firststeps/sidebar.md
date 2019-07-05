[frontMatter]
title = "How do I create a sidebar?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---



Sidebars are a staple of macOS. Many apps on macOS have sidebars and use them to support a huge variety of usage scenarios. Apple added sidebar support right into Catalyst. By default, any Master-Detail view implemented using the `UISplitViewController` will inhibit macOS sidebar behaviour. However, if you just do that, the sidebar contents (that is, the Master part of the Master Detail View) will look strangely out of place. The rows still look like normal UIKit Rows:

![Sidebars](/img-content/catalyst/sidebars.jpeg)

Thankfully, this can easily be fixed. Apple offers a new property on the `UISplitViewController`:

``` swift
// The background style of the primary view controller.
@available(iOS 13.0, *)
open var primaryBackgroundStyle: UISplitViewController.BackgroundStyle
```

If you're on Catalyst, you can set this to `.sidebar` in order to get the macOS native sidebar look and feel from the right side of the screenshot above:

``` swift
primaryBackgroundStyle = .sidebar
```
