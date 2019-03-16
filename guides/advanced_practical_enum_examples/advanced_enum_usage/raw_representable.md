[frontMatter]
title = "RawRepresentable"
tags = ["enum", "RawRepresentable"]
created = "2019-03-01 16:29:51"
description = ""
published = true

[meta]
swift_version = "5.1"
---

The Swift documentation for the `RawRepresentable` protocol says:

> A type that can be converted to and from an associated raw value.
> With a `RawRepresentable` type, you can switch back and forth between a
> custom type and an associated `RawValue` type without losing the value of
> the original `RawRepresentable` type.

This type allows us to map a certain raw value to a certain `enum` case back and forth. 
jjkk


``` Swift
enum KeyCommand: CaseIterable {
    case newArticle
    case delete
    case reload
}

extension KeyCommand: RawRepresentable {
    typealias RawValue = UIKeyCommand

    private static func flags(for command: KeyCommand) -> (input: String, modifierFlags: UIKeyModifierFlags, Selector) {
        switch command {
        case .newArticle: return ("n", [.command], #selector(ViewController.doCommand(_ :)))
        case .delete: return ("d", [.command], #selector(ViewController.doCommand(_ :)))
        case .reload: return ("r", [.shift, .command], #selector(ViewController.doCommand(_ :)))
        }
    }

    init?(rawValue: UIKeyCommand) {
        guard let commandInput = rawValue.input else { return nil }
        for commandCase in KeyCommand.allCases {
            let (input, flags, _) = KeyCommand.flags(for: commandCase)
            if commandInput == input, rawValue.modifierFlags == flags {
                self = commandCase
                break
            }
        }
        return nil
    }

    var rawValue: UIKeyCommand {
        let (input, flags, action) = KeyCommand.flags(for: self)
        return UIKeyCommand(input: input, modifierFlags: flags, action: action)
    }
}

class ViewController: UIViewController {

    override var keyCommands: [UIKeyCommand]? {
        return [KeyCommand.newArticle.rawValue, KeyCommand.delete.rawValue, KeyCommand.reload.rawValue]
    }

    @objc func doCommand(_ command: UIKeyCommand) {
        switch KeyCommand(rawValue: command) {
        case .newArticle?: newAction()
        case .delete?: deleteAction()
        case .reload?: reloadAction()
        default: ()
        }
    }

    private func newAction() {}
    private func deleteAction() {}
    private func reloadAction() {}

}
```
