[frontMatter]
title = "How do I support mouse hovering?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---

![](/img-content/catalyst/hover.png)


Apple supports hovering in Catalyst via a new gesture recognizer, the so-called `UIHoverGestureRecognizer`. It works in a very simple manner.

1. First you initialize a new hover gesture recognizer
2. Then, you add it to your view
3. Finally, you implement the method to be called when the user hovers

Now, for every mouse movement within the containment of the view, your method will be called and you can query the gesture recognizer for the position in order to implement custom logic (as Apple does in the Stocks.app when you hover over a Stock's price history).

Below is a simple implementation:

``` Swift
final class MyHoverViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        // Create the recognizer
        let hover = UIHoverGestureRecognizer(target: self, action: #selector(mouseDidMove(with:)))
        // Add it to the view
        view.addGestureRecognizer(hover)
    }

    @objc func mouseDidMove(with recognizer: UIHoverGestureRecognizer) {
        guard let view = recognizer.view else { return }
        // Calculate the location
        let locationInView = recognizer.location(in: view)
        print("Hovering at location \(locationInView)")
    }
}
```
