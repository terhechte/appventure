[frontMatter]
title = "An Abstract Class"
tags = ["box", "associated", "generics", "erasure"]
created = "2019-03-01 11:01:50"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# An Abstract Class

In essense, what we\'re going to build, is a generic wrapper (or box)
that hosts a type conforming to a `protocol` with an `associated type`.
It does so by implementing the requirements of the `protocol` and
forwarding all invocations to the boxed type.

The first new type we need for that is a base `class` that acts as a
abstract class:

``` Swift
class AnyComputerBase<Processor: CPU>: Computer {
    var processor: Processor {
        fatalError()
    }
    var processorCount: Int {
        fatalError()
    }
}
```

This `class` should never be initialized, as it only provides an
abstract template of what subclasses should implement. While other
languages (like Java) allow explicitly marking classes as abstract,
Swift doesn\'t offer us a way to do so. One solution to this is adding a
`fileprivate init` to this `class`. However as that requires subclasses
to be in the same file as this superclass, we can also just make the
whole `class` `private` with an even better result. Now, other parts of
the code won\'t even know about the existence of `AnyComputerBase` or
even `initialize` it:

``` Swift
private class AnyComputerBase<Processor: CPU>: Computer {
...
}
```

Why do we even need this, and what does it do? As you can see, it just
implements the `Computer` `protocol` by implementing the requirements
and doing nothing in there. The more important part is that it moves the
`associated type` from the protocol into a generic type for the `class`:
`AnyComputerBase<Processor: CPU>`.

Swift automatically figures out that `Processor` is the `typealias` for
`Computer.ProcessorType`. However, when in doubt you can also add an
extra typealias:

``` Swift
class AnyComputerBase<Processor: CPU>: Computer {
  typealias ProcessorType = Processor
  ...
}
```
