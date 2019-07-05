[frontMatter]
title = "How do I modify the window?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---



## Preparations

Note that in *Beta 2* you need to manually import a special bridging header if you want to modify the title. [Here's how to do it](firststeps/bridgingheader.md).

The way to modify window titlebars is to use the `UIScene` API introduced with iOS 13. The gist is that you use a `SceneDelegate` and in the `scene:willConnectToSession:options` method, you can modify a window scene's `titlebar`.

If your project doesn't have a `SceneDelegate` yet, [here's a brief primer on how to set it up.](firststeps/scene_delegate.md). This delegate is - as far as I'm aware - required to support toolbars.

[`UIWindowScene`](https://developer.apple.com/documentation/uikit/uiwindowscene) objects have a `titlebar` property on macOS. These `UITitleBar` objects are currently not documented, but the headers expose several properties:

``` swift
 func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = (scene as? UIWindowScene) else { return }
        #if targetEnvironment(UIKitForMac)
	windowScene.titlebar.titleVisibility = .hidden
	#endif
}
```
