[frontMatter]
title = "Preface"
tags = ["swiftui"]
created = "2019-06-11 21:01:50"
description = "A brief introduction into the aim of this guide"
published = true

[meta]
feature_image = "/img-content/swiftui_article.jpg"

---

# Preface

When Apple released Swift in 2014 it was a tectonic shift for the Apple development community. One that few people had anticipated. Though while Swift was a much different language than Objective-C, the methods and function you'd call, the frameworks, kept unchanged. In fact, you could ignore the enums and associated types and write Swift that looked and felt much like Objective-C, utilising Foundation and UIKit just as before. This was important for Apple because the scope of UIKit and Foundation is much bigger than that of Swift.

With SwiftUI, all of this changes. While a Objective-C developer from the 80s would feel right at home with 2017 era Swift code employing target action or delegate mechanisms, a SwiftUI project would look much more alien to him. Apple moved past its development history (shared with NeXT) of the past ~30 years in a generational leap that will hopefully be the base for decades to come. In doing so, Apple also moved the goalpost of mobile application development:

- A shared framework for all Apple platforms (iOS, macOS, watchOS, etc)
- Declarative with live reload and live preview
- Type-Safe UI declarations
- Going beyond Interface Builder
- High level abstraction that will allow future compile time optimizations
- Fully compatible with UIKit / AppKit
- Automatic support for dark mode, dynamic text, and more
- Smart dependency injection via environments
- Combine framework for well thought-out bindings
- much more

However, don't throw away your old code just yet. While SwiftUI is very exciting (as all Shiny New Things tend to be), it is also a very early beta. Apple already shipped some watchOS apps with SwiftUI (Calculator is an example) but at the same time a calculator on the watch is a different beast than a 200k LOC iPhone app. Some important components will come in a later beta, some components might only come next year, the documentation is still very, very sparse, live preview requires the beta of macOS Catalina. 

In general, it seems that much of the flexibility that UIKit offered has been replaced with a more high level and less customizable interface. You can always resort to UIKit though. This is also a very important point to stress. 

Just as Swift changed a lot after its introduction, I also expected SwiftUI to change in the coming years. This guide introduces SwiftUI in a general manner by developing a small app. It also lists various tips and tricks for things that are difficult or non-intuitive to do in SwiftUI. Lets begin!

