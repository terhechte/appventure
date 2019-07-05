[frontMatter]
title = "add TouchBar support?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# How do I add TouchBar support?

## Preparations

Note that in *Beta 2* you need to manually import a special bridging header if you want to use touchbars. [Here's how to do it](firststeps/bridgingheader.md).

With that out of the way, lets have a brief look at touchbars. [Apple's documentation for the `NSTouchBar` class is fantastic](https://developer.apple.com/documentation/appkit/nstouchbar) and it would be a waste to try to replicate all that documentation here. Also, touchbars in Catalyst apps work just like the AppKit touchbars. So all the available `NSTouchBar` tutorials work just as well for your iPad app.

In brief, touchbars work as follows: Each controller in the [responder chain](how/responder_chain.md) is asked whether he has a touchbar that he wants to display via the `func makeTouchBar() -> NSTouchBar?` method on `UIResponder` (or `NSResponder`). The higher up items in the responder chain have priority. Within that method, you return a fully configured touchbar with a proper `NSTouchBarDelegate` set. The `NSTouchBarDelegate` allows you to configure the touchbar to your hearts contents. Here's a simple example:

Make sure to remember that touchbars only appear for objects that conform to `UIResponder` and are in the [responder chain](how/responder_chain.md). A good place for this code is your `UIViewController` that is currently being displayed.

``` swift
// Define the items we want to display in the touch bar via specific identifiers, so UIKit can track them
let MyButtonTouchBarIdentifier = NSTouchBarItem.Identifier(rawValue: "MyButton")

class MyViewController: UIViewController {
    override func makeTouchBar() -> NSTouchBar? {
        let touchBar = NSTouchBar()
        touchBar.delegate = self
        touchBar.defaultItemIdentifiers = [MyButtonTouchBarIdentifier,
                                           NSTouchBarItem.Identifier.otherItemsProxy]
        return touchBar
    }

    @objc func buttonPressed(sender: NSTouchBarItem) {
    }
}
extension MacSplitViewController: NSTouchBarDelegate {

    func touchBar(_ touchBar: NSTouchBar, makeItemForIdentifier identifier: NSTouchBarItem.Identifier) -> NSTouchBarItem? {
        switch identifier {
        case MyButtonTouchBarIdentifier:
            return NSButtonTouchBarItem.init(identifier: identifier,
                                             title: "Press Me",
                                             target: self,
                                             action: #selector(self.buttonPressed))
        default: return nil
        }
    }
}
```

## Using Apple HIG TouchBar Images

Apple has a very nice set of default touchbar images outlined here:

- https://developer.apple.com/design/human-interface-guidelines/macos/touch-bar/touch-bar-icons-and-images/
- https://developer.apple.com/documentation/appkit/nstouchbaritem?language=objc

These currently can't be used in Catalyst apps (FB6312494).
