[frontMatter]
title = "A DebugPrinter"
tags = ["keypath"]
created = "2019-03-29 12:26:11"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# DebugPrinter Intermezzo

Now that we have our writable `KeyPath` types, we'd like to introduce a type that allows us to define the logging behaviour of an object. We'd like to define which properties should be printed when our debug print function is called. It will be a very simple example.

We will actually start by looking at how we would invoke the code before we write it. This will make it easier to understand what is going on here. The class we will define is called `DebugPrinter` and it is used to dynamically change how to debug print and object at runtime.

Say, if you will, that you're working on a Presentation app (aka something like Keynote). You have one structure that represents the current state of a presentation.

``` Swift
class Presentation {
  class Slide {
    var name: String
    var number: Int
    var template: Template
    var backgroundColor: UIColor
    var content: String
    var leftImage: UIImage?
    var rightImage: UIImage?
  }
  var currentSlide: Slide
  var currentSlideIndex: Int
  var slides: [Slide]
  var title: String
  var startedPresenting: Date?
  var isAnimating: Bool
}
```

Now, you'd like to define at runtime which of the properties of this type to print. For example depending on whether a user is currently presenting or editing slides. This is, how we would do that:

``` Swift
let state = Presentation(...) // we need a presentation instance
let printer = DebugPrinter("State", for: state)
printer.addLog(\Presentation.currentSlideIndex, prefix = "Current")
printer.addLog(\Presentation.isAnimating)
printer.addLog(\Presentation.currentSlide.name)
printer.addLog(\Presentation.currentSlide.leftImage)

printer.log()
```

So here, we first create a `printer` that holds a reference to our `state` (an instance of our `Presentation`). Next, we define which parts of the `animation` we want to print (including an optional prefix). Here, we want to print, for example, the current slide, whether we're currently animating, the name of the current slide and, finally, the optional image of the current slide.

So, how would we implement this `DebugPrinter`? here is the code.

``` Swift
/// Dynamically define a debug description for an object
class DebugPrinter<T> where T: AnyObject {
    /// 1
    var keyPaths: [(String?, KeyPath<T, String>)] = []
    let reference: T
    let prefix: String

    /// 2
    init(_ prefixString: String, for instance: T) {
        reference = instance
        start = prefixString
    }

    /// 3
    func addLog(_ path: KeyPath<T, String>, prefix: String? = nil) {
        keyPaths.append((prefix, path))
    }

    /// 4
    func log() {
        print(prefix, terminator: ": ")
        for entry in keyPaths {
          if let prefix = entry.0 { print(prefix, terminator: "") }
          print(reference[keyPath: entry.1], terminator: ", ")
        }
    }
}
```

So lets go through step by step. First, we're creating a new `class` that is generic over the type `T` so that we can store keypaths of type `KeyPath<T, String>` in our `keyPaths` array [1]. Each keypath is stored in a [tuple](lnk::tuple) with an optional prefix.

Then, we can initialize a `DebugPrinter` with a `prefix` `String` - which will be printed at the beginning of each future print invocation - and a reference to the actual instance we want to debug `T` [2].

The `addLog` function, then, inserts a new `KeyPath` into our `keyPaths` array (again, including the optional `prefix`) [3].

Finally, the `log` function, when called, iterates over all the keypaths and, for each of them, prints the contents of the `KeyPath` in our `reference` (including the prefix).

Before you move on, have a brief look at the implementation of the `DebugPrinter` and at the usage example. Would this actually work? 

---

No, it actually doesn't. The problem is that our `Presentation` state has properties of various types: `currentSlideIndex: Int`, `title: String`, `leftImage: UIImage?`. However, our `DebugPrinter` only stores keypaths of the type `KeyPath<T, String>`. We could try to make the second parameter generic as well, but that still doesn't help, because it would be generic for the full instance of `DebugPrinter`, for example:

``` Swift
class DebugPrinter<Root, Value> {
  var keyPaths: [KeyPath<Root, Value>]
}
```

Here, our `KeyPath` still have to be of the same type. All `Int`, all `String`, etc. What we actually want is a keypath that doesn't care about the `Value` type! A KeyPath that just cares about the `Root` type (our `reference`). This is, what the `PartialKeyPath` is for. Lets have a look at it.
