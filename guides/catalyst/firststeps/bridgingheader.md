[frontMatter]
title = "How do I use the touchbar or toolbar classes?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---



There is one issue on beta 2 which means that you need to add a *bridging header* to your project and import a header file in there if you want to use the `NSTouchbar` or `NSToolbar` APIs.

1. Add a new bridging header to your project, say `bridge-me.h` (If you don't have a bridging header yet)
2. In your target Build Settings set the `Objective-C Bridging Header` value to your new bridging header ("MyApp/bridge-me.h")

Make sure to have the right path for the bridging header.

## Then, insert the following code in your bridging header:

``` C
#import <Foundation/Foundation.h>
#import <UIKit/NSToolbar+UIKitAdditions.h>
#import <UIKit/NSTouchbar+UIKitAdditions.h>
```
