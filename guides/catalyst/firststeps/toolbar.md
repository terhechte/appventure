[frontMatter]
title = "create a toolbar?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# How do I create a toolbar firststeps/toolbar.md

## Preparations

Note that in *Beta 2* you need to manually import a special bridging header if you want to use `NSToolbar`. [Here's how to do it](firststeps/bridgingheader.md).

The best way to insert toolbars is to use the new `UIScene` API that Apple introduced with iOS 13. The gist is that you use a `SceneDelegate` and in the `scene:willConnectToSession:options` method, you can modify a window scene's `titlebar` by setting a new `NSToolbar` on it.

If your project doesn't have a `SceneDelegate` yet, [here's a brief primer on how to set it up.](firststeps/scene_delegate.md). This delegate is - as far as I'm aware - required to support toolbars.

## Modifying the Scene

The first step is to modify the `scene(willConnectTo:options:)` method in your `SceneDelegate` to check if we're running `UIKitForMac` - after all, iOS doesn't have toolbars - and then make sure that our scene is actually a `UIWindowScene`:

``` swift
 func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = (scene as? UIWindowScene) else { return }
        #if targetEnvironment(UIKitForMac)
	#endif
}
```

[`UIWindowScene`](https://developer.apple.com/documentation/uikit/uiwindowscene) objects have a `titlebar` property on macOS. These `UITitleBar` objects are currently not documented, but the headers expose a `toolbar` property that you can use to assign a `NSToolbar` to your window:

``` swift
 func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = (scene as? UIWindowScene) else { return }
        #if targetEnvironment(UIKitForMac)
	// Create a new toolbar (see below)
	let newToolbar = makeMyFancyToolbar()

	// Insert it into the titlebar
	windowScene.titlebar.toolbar = self

	// Hide the window title, looks nicer
	windowScene.titlebar.titleVisibility = .hidden
	#endif
}
```

So this is how we insert an actual toolbar into our window. The last remaining step is to create such a toolbar, so how does that work?

## Creating a Toolbar

This is actually a multi-step process as toolbars are quit versatile. You begin by instantiating a new toolbar and configuring it accordingly:

``` swift
// Create the toolbar
let toolbar = NSToolbar(identifier: "MyFancyToolbar")

// Assign the delegate
toolbar.delegate = self
```

As you can see, the configuration is just two lines of code (for now) but toolbars employ a delegate that you can leverage to configure them in much more detail. Lets see how.

## Implementing the NSToolbarDelegate protocol

First, you need an object that can conform to your toolbar delegate. For simplicity, lets just take our `SceneDelegate`. However, this can be any object and for more complex setups could be, for example, your own `MyToolbarController` class.

``` swift
#if targetEnvironment(UIKitForMac)
extension SceneDelegate: NSToolbarDelegate {
}
#endif
```

Again, make sure this code only compiles on macOS. Next, lets implement the bare minimum needed to display a toolbar.


Toolbars are versatile and allow your users to configure them and modify their contents. Our toolbar will just display a button on the right side. Toolbars identify their contents via toolbar identifiers of type `NSToolbarItem.Identifier`. Each item in the toolbar has a custom identifier. This makes it easy for the system to understand which items are in the toolbar, which can be customized, removed, etc. So in order for us to add a button, we need an identifier for our button:

``` swift
private let OurButtonToolbarIdentifier = NSToolbarItem.Identifier(rawValue: "OurButton")

#if targetEnvironment(UIKitForMac)
extension SceneDelegate: NSToolbarDelegate {
}
#endif
```

Next, we need to implement two methods that are called on the delegate to figure out what to display in the toolbar:

1. `toolbarDefaultItemIdentifiers`: This returns the identifiers for the items that should be in the toolbar *by default*
2. `toolbarAllowedItemIdentifiers`: This returns the identifiers that are *currently* allowed in the toolbar

We will implement default first:

``` swift
extension SceneDelegate: NSToolbarDelegate {
    func toolbarDefaultItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        return [NSToolbarItem.Identifier.flexibleSpace,
                OurButtonToolbarIdentifier]
    }
}
```

Here, we're returning an array of two items. The *last* is our `OurButtonToolbarIdentifier`. The *first* is a "flexible space" identifier that will consume as much horizontal space as possible, thus pushing our button all the way to the right.

For simplicity, the second method, `toolbarAllowedItemIdentifiers` just calls the first one.

``` swift
extension SceneDelegate: NSToolbarDelegate {
    func toolbarDefaultItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        return [NSToolbarItem.Identifier.flexibleSpace,
                OurButtonToolbarIdentifier]
    }
    func toolbarAllowedItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        return toolbarDefaultItemIdentifiers(toolbar)
    }
}
```

Now that we told the toolbar how to display itself, we just need to create those items (in our case just our button):

``` swift
extension SceneDelegate: NSToolbarDelegate {
    func toolbar(_ toolbar: NSToolbar, itemForItemIdentifier itemIdentifier: NSToolbarItem.Identifier, willBeInsertedIntoToolbar flag: Bool) -> NSToolbarItem? {
        if (itemIdentifier == OurButtonToolbarIdentifier) {
	    let barButtonItem = UIBarButtonItem(barButtonSystemItem: UIBarButtonItem.SystemItem.add,
	                          target: self,
				  action: #selector(self.myFancyAction(sender:)))
            let button = NSToolbarItem(itemIdentifier: itemIdentifier, barButtonItem: barButtonItem)
            return button
        }
        return nil
    }
```

Again, this is simple enough. We just create a `UIBarButtonItem`, wrap it into a `NSToolbarItem` and return it. There're a lot of options here that we will not go into, but reading the headers and the documentation will help you along if you need more complex setups.

[If you want to hide your existing iOS / UIKit toolbar, too, have a look at this section.](how/hide_tabbar_with_toolbar.md)

If you want to display a nice segmented control your toolbar, like this:

![](/img-content/catalyst/segmentedcontrol_toolbar.png)

[There's an explanation on how to do this in the following section.](how/segmented_control_toolbar.md)

Here's the whole code `SceneDelegate` in one section:

``` swift
import UIKit

class SceneDelegate: UIResponder, UIWindowSceneDelegate {

    var window: UIWindow?

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = (scene as? UIWindowScene) else { return }

        #if targetEnvironment(UIKitForMac)
        if let titlebar = windowScene.titlebar {
            titlebar.titleVisibility = .hidden
            titlebar.toolbar = makeMyFancyToolbar()
        }
        #endif
    }

    private func makeMyFancyToolbar() -> NSToolbar {
        let toolbar = NSToolbar(identifier: "MyToolbar")
        toolbar.delegate = self
        return toolbar
    }

    @objc func myFancyAction(sender: UIBarButtonItem) {
        print("Button Pressed")
    }
}

#if targetEnvironment(UIKitForMac)

private let OurButtonToolbarIdentifier = NSToolbarItem.Identifier(rawValue: "OurButton")

extension SceneDelegate: NSToolbarDelegate {
    func toolbar(_ toolbar: NSToolbar, itemForItemIdentifier itemIdentifier: NSToolbarItem.Identifier, willBeInsertedIntoToolbar flag: Bool) -> NSToolbarItem? {
        if (itemIdentifier == OurButtonToolbarIdentifier) {
            let barButton = UIBarButtonItem(barButtonSystemItem: .add, target: self, action: #selector(myFancyAction(sender:)))
            let button = NSToolbarItem(itemIdentifier: itemIdentifier, barButtonItem: barButton)
            return button
        }
        return nil
    }

    func toolbarDefaultItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        return [NSToolbarItem.Identifier.flexibleSpace, OurButtonToolbarIdentifier]
    }

    func toolbarAllowedItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        return toolbarDefaultItemIdentifiers(toolbar)
    }
}
#endif
```
