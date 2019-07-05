[frontMatter]
title = "nest touchbars?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# How do I nest touchbars?

If you have multiple view controllers in your [responder chain](how/responder_chain.md) that each want to insert something in your `NSTouchBar` you can simply define the outermost (highest priority) touchbar to host other touchbars alongside. You do that by adding the system default `NSTouchBarItem.Identifier.otherItemsProxy` to your list of `defaultItemIdentifiers`:

``` swift
    override func makeTouchBar() -> NSTouchBar? {
        let touchBar = NSTouchBar()
        touchBar.delegate = self
        touchBar.defaultItemIdentifiers = [MyButtonTouchBarIdentifier,
                                           NSTouchBarItem.Identifier.otherItemsProxy]
        return touchBar
    }
```

Now, if, say, a child view controller would also implement `makeTouchBar`, its touchbar would be displayed next to our `MyButtonTouchBarIdentifier` button.
