[frontMatter]
title = "support keyboard shortcuts?"
tags = ["catalyst", "macos", "uikitformac"]
created = "2019-07-05"
description = ""
published = true

[meta]
swift_version = "5.1"
---


# How do I support keyboard shortcuts?

Keyboard shortcuts are implemented via the existing `UIKeyCommand` system on `UIResponder`. Here's a simple example of how your currently visible view controller can listen for `Escape` key presses by the user:

``` swift
class MyKeyListeningViewController: UIViewController {
    override var keyCommands: [UIKeyCommand]? {
        return [UIKeyCommand(input: UIKeyCommand.inputEscape,
                             modifierFlags: [],
                             action: #selector(doCancelCommand(sender:)))
        ]
    }
}
```

Keep in mind that on macOS multiple views can easily be visible at the same time and [the rules of the responder chain apply.](how/responder_chain.md)
