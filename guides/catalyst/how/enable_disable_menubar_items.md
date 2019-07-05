[frontMatter]
title = "How do I enable / disable menubar items based on whats visible on screen?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---



Catalyst, just like Cocoa, uses the [responder chain](how/responder_chain.md) to figure out whether an action in a menu can be performed. [Remember, that a menu bar on iOS is composed out of `UIAction`, `UICommand`, and `UIMenu` objects.](firststeps/modify_menubar.md)

The way that works is as follows:

1. When you open a menu in the menu bar with your mouse
2. UIKit will have a look at the first responder and call
3. [`canPerformAction(_:withSender:)`](https://developer.apple.com/documentation/uikit/uiresponder/1621105-canperformaction) to figure out if the first responder has a matching `@IBAction someMethod` that fits the selector from the menubar item in question
4. If the first responder returns no, it will ask the next responder
5. If a responder returns yes, then this menu bar entry will be enabled (clickable) and this responder (i.e. object or view controller) will be set as the current `target` of the menu bar entry.
6. If the next responder is nil - that is, it UIKit reached the end of the responder chain - it will stop and the menu bar entry will be disabled.

This process happens for each item in the menubar.

If you want to influence how a menu bar item becomes enabled / disabled based on the particulars of your view controller, you can override `canPerformAction` and write custom logic. Here is a quick example. Here, we imagine that a menubar action should only be enabled if we have actual text in our textField.

``` swift
override func canPerformAction(_ action: Selector, withSender sender: Any?) -> Bool {
  guard !(textField.text ?? "").isEmpty else { return false }
  return super.canPerformAction(action, withSender: sender)
}
```
