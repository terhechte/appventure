[frontMatter]
title = "use the responder chain?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# How do I use the responder chain how/responder_chain.md

The responder chain is a event handling system at the heart of macOS and iOS.
Every touch event coming in, for example, uses this responder chain to reach the currently active `UIControl`. The main building block of the responder chain is the `UIResponder` class which is a superclass of `UIViewController` or `UIView`.

Apple has very useful information on this available:

- [iOS: Using Responders and the Responder Chain](https://developer.apple.com/documentation/uikit/touches_presses_and_gestures/using_responders_and_the_responder_chain_to_handle_events)
- [macOS: Event Architecture Overview](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/EventOverview/EventArchitecture/EventArchitecture.html)

Below, I'll quote the most important sections to understand the thing:

Responders receive the raw event data and must either handle the event or forward it to another responder object. When your app receives an event, UIKit automatically directs that event to the most appropriate responder object, known as the first responder.

Unhandled events are passed from responder to responder in the active responder chain.

Here's an image from the Apple Documentation:

![](/img-content/catalyst/responderchain.png)

Now imagine that you're entering text in the text field. The following will happen:

1. If the text field does not handle an event, UIKit sends the event to the text field’s parent UIView object
2. If that does not handle the event, it is forwarded to the next UIView.
3. If that does not handle the event, it is forwarded to the UIViewController (which is the root view controller of the window)
4. If the view controller is not handling the event, it is forwarded to the `UIApplication`
5. If the UIApplication is not handling the event, it is handled by the `UIApplicationDelegate`

This also means that if you really need to catch a certain event, you can always set up the required selector / method in your app delegate.

## Altering the Responder Chain

You can alter the responder chain by overriding the next property of your responder objects. When you do this, the next responder is the object that you return.
