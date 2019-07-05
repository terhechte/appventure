[frontMatter]
title = "How do I hide my iOS tabbar when I display a macOS toolbar?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---



If you want to hide your iOS tabbar, just as you're displaying your macOS toolbar, this is what you can do in your `SceneDelegate`:

``` swift
    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        #if targetEnvironment(UIKitForMac)
        if let windowScene = scene as? UIWindowScene {
            if let titlebar = windowScene.titlebar {
                let toolbar = NSToolbar(identifier: "NerauToolbar")

                let rootViewController = window?.rootViewController as? UITabBarController
                rootViewController?.tabBar.isHidden = true

                toolbar.delegate = self
                titlebar.titleVisibility = .hidden

                titlebar.toolbar = toolbar
            }
        }
        #endif
    }
```
