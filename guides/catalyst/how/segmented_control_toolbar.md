[frontMatter]
title = "How do I display a segmented control in the toolbar?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---



A segmented control is a convenient replacement for the iOS tabbar, as it also groups related segments and only allows one of them to be active.
It is basically just another type of `NSToolbarItem`. Thus, the process is very similar to [how you set up a toolbar with elements before](firststeps/toolbar.md).

1. Define a identifier
2. Return the identifiers
3. For the new identifier, return a segmented control
4. Set up an action and target for the segmented control

As a bonus point, you can tell the toolbar that the segmented control should be the centered item in the toolbar (much like with a tabbar).

[In this example, we also have a UITabBar that we're hiding](how/hide_tabbar_with_toolbar.md), so that the switching of the visible view controller is still handled by the hidden tabbar.

Here is the necessary code:

``` swift
class SceneDelegate: UIResponder, UIWindowSceneDelegate, NSToolbarDelegate {

    // We need a toolbar identifier
    static let SegmentedItemToolbarIdentifier = NSToolbarItem.Identifier(rawValue: "PrimaryGroup")

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        #if targetEnvironment(UIKitForMac)
        if let windowScene = scene as? UIWindowScene {
            if let titlebar = windowScene.titlebar {
                let toolbar = NSToolbar(identifier: "NerauToolbar")

                let rootViewController = window?.rootViewController as? UITabBarController
		// Hide the tabbasr
                rootViewController?.tabBar.isHidden = true

                toolbar.delegate = self

		// Our segmented control should be centered

                toolbar.centeredItemIdentifier = SceneDelegate.SegmentedItemToolbarIdentifier
                titlebar.titleVisibility = .hidden

                titlebar.toolbar = toolbar
            }
        }
        #endif
    }

    func toolbar(_ toolbar: NSToolbar, itemForItemIdentifier itemIdentifier: NSToolbarItem.Identifier, willBeInsertedIntoToolbar flag: Bool) -> NSToolbarItem? {
            if (itemIdentifier == SceneDelegate.SegmentedItemToolbarIdentifier) {
	        // Create a new group item that hosts two buttons
                let group = NSToolbarItemGroup(itemIdentifier: SceneDelegate.SegmentedItemToolbarIdentifier,
                                               titles: ["Startpage", "Categories"],
                                               selectionMode: .selectOne,
                                               labels: ["section1", "section2"],
                                               target: self,
                                               action: #selector(toolbarGroupSelectionChanged))

		// Set the initial selection
                group.setSelected(true, at: 0)

                return group
            }
    	return nil
    }

    @objc func toolbarGroupSelectionChanged(sender: NSToolbarItemGroup) {
        // This is called when the user changes the selection
	// Notice how we get the tab bar controller and change the selection there
        let rootViewController = window?.rootViewController as? UITabBarController
        rootViewController?.selectedIndex = sender.selectedIndex
    }

    func toolbarDefaultItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        return [SceneDelegate.SegmentedItemToolbarIdentifier,
                NSToolbarItem.Identifier.flexibleSpace]
    }

    func toolbarAllowedItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        return self.toolbarDefaultItemIdentifiers(toolbar)
    }
}
```
