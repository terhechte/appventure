[frontMatter]
title = "A Box Type"
tags = ["box", "associated", "generics", "erasure"]
created = "2019-03-01 11:01:50"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# A Box Type

The next step is the most difficult to understand part of type erasure,
which means that after this, it\'ll be easy. We will introduce another
`private` type. This will be the actual box that houses our original
type (the XBox360 or the PowerMac G5). Let\'s start by having a look at
the code:

``` Swift
private class AnyComputerBox<ConcreteComputer: Computer>: 
        AnyComputerBase<ConcreteComputer.ProcessorType> 
{
    private let internalComputer: ConcreteComputer
    override var processor: ConcreteComputer.ProcessorType {
        return internalComputer.processor
    }
    override var processorCount: Int {
        return internalComputer.processorCount
    }
    init(_ computer: ConcreteComputer) {
        internalComputer = computer
    }
}
```

The most important concept here can be found in the very first line:

``` Swift
private class AnyComputerBox<ConcreteComputer: Computer>: 
        AnyComputerBase<ConcreteComputer.ProcessorType>
```

Here, we define a new type `AnyComputerBox` which is generic over
**any** computer (`ConcreteComputer`). This new type, then, is a
subclass of our earlier abstract class `AnyComputerBase`. Remember that
`AnyComputerBase` made the original `ProcessorType` of the `Computer`
protocol generic by adding it as a generic parameter `CPU`. Now, our new
box has a **different** generic type (`Computer`) and provides only its
`associated type` **ProcessorType** to the abstract superclass. In a
simpler explanation, this is what happens (in a mock language):

1.  `Computer<CPU>`
2.  `AnyComputerBase<Processor: CPU>: Computer<CPU> where Computer.CPU = Processor`
3.  `AnyComputerBox<ConcreteComputer: Computer>: AnyComputerBase<ConcreteComputer.ProcessorType>`

So the box (`AnyComputerBox`) subclasses the abstract class and forwards
in the `Processor` type via its own generic `Computer` type which also
has a `ProcessorType`.

Why do we do this? It makes the box generic over any computer so that
**any** computer can be boxed into it.

The rest of the `class` is simple. There\'s an `internal` computer
`internalComputer` which is the actual type conforming to the `Computer`
`protocol`. We\'re also overriding the two classes that are required by
the protocol and forwarding the implementations of the
`internalComputer`. Finally we have an initializer with a new
`ConcreteComputer` (i.e. the `Computer` protocol).

