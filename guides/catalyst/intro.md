[frontMatter]
title = "Catalyst Guide Introduction"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---

Catalyst is one of the major new features of iOS 13 and macOS 15. It allows you to take your iPad app, and, with the activation of a single checkbox, add a macOS target.

![](/img-content/catalyst/catalyst_checkbox.png)

For very simple projects, this works great, but there are multiple issues that might run in to. Here is a brief selection:


- Deprecated iOS classes, such as `AddressBookUI` or `UIWebView` are not supported anymore
- Some iOS classes, such as ARKit are not available on macOS
- Some iOS classes, such as StoreKit, have slightly different API
- The macOS API integrations such as `NSToolBar` or `NSMenuBar` are currently quite limited
- Problems with signing

This guide is a very detailed developer explanation of Catalyst and all the issues that you can run into in the current beta. It will be updated as new macOS betas are released.

## Contents of this Guide

This guide will initially [give a short introduction into Catalyst](rel::intro.md) Next, [we will iterate over the first steps to support the various features that make an iPad app a good macOS citizen](rel::firststeps/intro.md). Finally, we will [go through a long *How Do I ...* list](rel::how/intro.md) of not-so-obvious things you might run into while working on Catalyst. As a sort of Appendix, [we have a list of currently known issues](rel::issues/issues.md) you might run into. This is helpful to keep you from trying to hunt down a bug that's not yours.


