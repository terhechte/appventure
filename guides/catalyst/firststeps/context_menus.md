[frontMatter]
title = "create context menus?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# How do I create context menus

Context Menus in Catalyst are implemented via the new [`UIContextMenuInteraction` API that Apple shipped on iOS as part of iOS 13.](https://developer.apple.com/documentation/uikit/uicontextmenuinteraction). [They work hand in hand with menu and shortcut system that is documented here](https://developer.apple.com/documentation/uikit/menus_and_shortcuts).

If you support context menus with `UIContextMenuInteraction`, they will automatically convert into right click context menus in your Catalyst app. Here's a simple example of how that works in action:

For simplicity, `UITableView` (and also `UICollectionView`) have new delegate methods that allow you to return a `UIContextMenuInteraction` instance that will be used for 3D touch or long presses on iOS or context menus on macOS. Here is an example of a very simple menu that has two entries "Move Priority Up" and "Move Priority Down":

``` swift
extension MyViewController: UITableViewDelegate {
    public override func tableView(_ tableView: UITableView, contextMenuConfigurationForRowAt indexPath: IndexPath, point: CGPoint) -> UIContextMenuConfiguration? {
        // Action providers are closures that generate action menus. They are called lazily only
	// when the menu is actually invoked.
        let actionProvider: ([UIMenuElement]) -> UIMenu? = { _ in
            let upAction = UIAction(__title: "Move Priority Up",
                                    image: UIImage(systemName: "square.and.arrow.up"))
            { [weak self] _ in
                self?.changePriority(.up, indexPath)
            }
            let downAction = UIAction(__title: "Move Priority Down",
                                      image: UIImage(systemName: "square.and.arrow.down"))
            { [weak self] _ in
                self?.changePriority(.down, indexPath)
            }

	    let actions = [upAction, downAction]

            // We generate a new menu with our two actions
            return UIMenu(__title: "Actions", image: nil, identifier: nil, children: actions)
        }

	// A context menu can have a `identifier`, a `previewProvider`,
	// and, finally, the `actionProvider that creates the menu
        return UIContextMenuConfiguration(identifier: nil,
                                          previewProvider: nil,
                                          actionProvider: actionProvider)
    }
}
```

That's all you need to support context menus in your tableView. [For more complex use cases, refer to the detailed documentation on menus:](https://developer.apple.com/documentation/uikit/menus_and_shortcuts), and on [`UIContextMenuInteraction`](https://developer.apple.com/documentation/uikit/uicontextmenuinteraction)
