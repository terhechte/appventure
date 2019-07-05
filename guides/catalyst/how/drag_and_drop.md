[frontMatter]
title = "How do I implement drag and drop?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---



Drag and drop is implemented via the same mechanisms that also support drag and drop on iOS. Below, you can see an example of a simple `UIViewContoller` that allows droping JSON files onto the application in order to import them.

``` swift
/// This is the identifier of a JSON File
private let JSONTypeIdentifier = "public.json"

extension MyDragAndDropSupportingViewController: UIDropInteractionDelegate {
    func dropInteraction(_ interaction: UIDropInteraction,
                         canHandle session: UIDropSession) -> Bool {
	// We tell the drag and drop system that we support JSON
        return session.hasItemsConforming(toTypeIdentifiers: [JSONTypeIdentifier])
    }

    func dropInteraction(_ interaction: UIDropInteraction, sessionDidUpdate session: UIDropSession) -> UIDropProposal {
        // If a drag comes in, we copy the file. We don't want to consume it.
        return UIDropProposal(operation: .copy)
    }

    func dropInteraction(_ interaction: UIDropInteraction, performDrop session: UIDropSession) {
        // This is called with an array of NSURL
	session.loadObjects(ofClass: URL.self) { urls in
            for url in urls {
                importJSONData(from: url)
            }
        }
    }
}
```

As with other Catalyst technologies, [there is a lot of good Apple documentation for this as this is the same as on iOS.](https://developer.apple.com/documentation/uikit/drag_and_drop/making_a_view_into_a_drop_destination)
