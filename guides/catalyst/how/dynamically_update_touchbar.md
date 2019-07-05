[frontMatter]
title = "How do I dynamically update the touchbar?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---



The documentation states that you just need to call `setNeedsTouchBarUpdate()` in order for the touch bar to be updated. However, as of beta 2, this does not work yet. A reliable way of achieving this is to just reset the `touchBar` property on `UIResponder` subclasses (like `UIViewController`) with the updated touchbar:

```swift
    // Adding `self.` everywhere to make it clear where it lives in this example
    @objc func doChangeState(sender: Any) {
        self.state = self.state + 1
        self.touchBar = self.makeTouchBar()
    }
```
