[frontMatter]
title = "Puttting it all together"
tags = ["box", "associated", "generics", "erasure"]
created = "2019-03-01 11:01:50"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Puttting it all together

In the next and final step, we\'re building the actual type that will be
used as the proverbial type eraser. Just as before, lets have a look at
the code first:

``` Swift
final class AnyComputer<Processor: CPU>: Computer {
    private let box: AnyComputerBase<Processor>
    var processor: Processor {
        return box.processor
    }
    var processorCount: Int {
        return box.processorCount
    }
    init<Concrete: Computer>(_ computer: Concrete) 
        where Concrete.ProcessorType == Processor {
      box = AnyComputerBox(computer)
    }
}
```

This `AnyComputer` conforms to the `Computer` protocol and is generic
over the `CPU` type that the protocol requires. Once again, we implement
the protocol requirements (`processor`, and `processorCount`) and
forward to a boxed type. This time we\'re forwarding to
`private let box: AnyComputerBase<Processor>`. This `box` is set in the
initializer where most of the magic happens:

``` Swift
init<Concrete: Computer>(_ computer: Concrete) 
    where Concrete.ProcessorType == Processor {
  box = AnyComputerBox(computer)
}
```

The problem with protocols with `associated types` is that you can\'t
use them as property types. Here, `init` requires any type conforming to
the `Computer` protocol. This is done by having a method-generic type
`Concrete` that requires `Computer` conformance. Even more, we also add
a constraint that makes sure that the generic `Processor` type of the
new `AnyComputer` class is the same type as the `associated type` of the
`Concrete` `Computer` type.

And now comes the kicker: Since we cannot set a property as being of
type `Computer` we, instead, have a property that is of
`AnyComputerBase` with a generic type for the `Processor`. As our
`AnyComputerBox` type is a subclass of `AnyComputerBase` we can
literally put **any** box (that is a subclass of `AnyComputerBase` into
this property. In this case, we\'re creating a new box with the
`Concrete` `Computer`.

Then we return the implementations of the contents of the box (i.e. the
actual `Concrete` `Computer`) in our `Computer` implementations:

``` Swift
var processorCount: Int {
    return box.processorCount
}
```

## Using It

With all this machinery in place, we can finally use this in order to
have different types (which share an associated type) in one container:

``` Swift
let powerComputers: [AnyComputer<PowerPC>] = 
    [AnyComputer(PowerMacG5()), AnyComputer(Xbox360())]
```

