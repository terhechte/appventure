[frontMatter]
title = "How do I support multiple *different* windows?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---



## How do I setup the a new scene?

A new scene needs a new, different scene configuration. The creation of scene configurations

First, you have to define a user activity and tell your application in the `info.plist` to accept it by adding it to the list of user activities:

![](/img-content/catalyst/useractivity.png)

Then, you need to define a new scene configuration in your *plist*:

![](/img-content/catalyst/multiscene.png)

Here you have the chance to load a different storyboard. Because, after all, we want the new window to be a different window. So it should also be a different storyboard.

Next up, say we have a button that you can click in order to spawn the new window. This is what you do:

``` swift
let userActivity = NSUserActivity(activityType: "com.stylemac.nerau.openResult")

// If you need custom data for your new window initialization, you can
// put it into the userInfo here
userActivity.userInfo = ["userid": 1234]

UIApplication.shared.requestSceneSessionActivation(nil, userActivity: userActivity, options: nil) { (e) in
  // If we happen to have an error
  print("error", e)
}
```

So, what's happening here. We create a new user activity. We told `UIApplication` to initialize a new scene with that activity. The activity can include an additional payload for the new window (user id, etc)

Finally, we need to tell the system that this new scene that we're creating should use the other scene configuration. We can do that in our app delegate:

``` swift
  func application(_ application: UIApplication,
                   configurationForConnecting connectingSceneSession: UISceneSession,
                   options: UIScene.ConnectionOptions) -> UISceneConfiguration {
    if options.userActivities.first?.activityType == "com.stylemac.nerau.openResult" {
      // Load our new window configuration
      return UISceneConfiguration(name: "New Configuration", sessionRole: connectingSceneSession.role)
    }
    // Load our default configuration
    return UISceneConfiguration(name: "Default Configuration", sessionRole: connectingSceneSession.role)
  }
```

By doing it this way, you can create multiple, different windows. Note that in beta 2, sometimes the user activities disappear *on route* with Catalysts. So if your `options.userActivities` is empty, then wait for another beta .. or look at *Other Approaches* below.

## Other Approaches

Another, simpler approach to doing this is to just replace the `rootViewController` of the `UIWindow` in the `SceneDelegate`'s

``` swift
func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
  window?.rootViewController = MyCustomUIViewController()
}
```
