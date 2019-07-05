[frontMatter]
title = "configure the macOS sandbox?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# How do I configure the macOS sandbox how/sandbox.md

The macOS sandbox is a system that allows you to define which operating system services your app target is allowed to use. Here's a list of the available options:

- Incoming Connections: Your app is a server
- Outgoing Connections: Your app is a client (i.e. read anything from network)
- Camera access
- Audio Input
- USB
- Printing
- Bluetooth
- Accessing the users' Contacts
- Accessing the users' Location
- Accessing the users' Calendar
- File access to various user locations

If you do not set these entitlements on your app, then you code is not allowed to access these services, and the app will crash or error when you try to do so.

The sandbox is enabled automatically once you enable a Catalyst target on your iPad app. The settings can be found in the "Signing & Capabilities" section and look like this:

![](/img-content/catalyst/sandbox.png)

Please note that the sandbox is not mandatory on macOS. You can disable it and then your app has much more leeway in what it can do on a users system. However, it is required if you want to ship your app on the macOS App Store.
