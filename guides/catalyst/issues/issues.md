[frontMatter]
title = "Known Issues?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


This is a list of somehow known issues, i.e. bugs where enough people seem to have them that it seems it is not an issue in your app but instead related to the current beta. This list is helpful to keep you from trying to hunt down a bug that's not yours.

## My app crashes when I close a window

If you see this when closing a window:

``` bash
 *** Terminating app due to uncaught exception 'NSRangeException', reason: 'Cannot remove an observer <UISystemInputAssistantViewController 0x1010adcf0> for the key path "bounds" from <CALayer 0x600000295bc0> because it is not registered as an observer.'
```

That seems to be an issue in the current beta

## My app crashes with "another instance of this process was already running"

This seems to be a bug or a feature in Catalina. With AppKit apps, multiple instances of the same app (with the same bundle identifier) can be running without an issue. If you duplicate `Calculator.app` 5 times and start them all, you have 5 calculators running. This seems to not be the case with Catalyst apps. If a Catalyst apps crashes in a certain way, apparently the system thinks it is still running. Thus, you can't run it again. Currently the only solution I know of is to reboot Catalina. Congratulations. The full error is:

``` bash
Couldn't register uikitformac.com.stylemac.Nerau.gsEvents with the bootstrap server. Error: unknown error code (1100).
This generally means that another instance of this process was already running or is hung in the debugger.
```

## I get weird SwiftUIKit compiler errors

Could it be that your `Xcode-beta.app` is either not in `/Applications` or not named `Xcode-beta.app`? (I.e. `Xcode-Beta v11.app`. Then, Catalyst apps currently won't compile.

## When I create a new Window, the `NSUserActivity` disappears

This seems to be rather flaky currently.
