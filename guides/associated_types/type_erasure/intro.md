[frontMatter]
title = "Type Erasure"
tags = ["box", "associated", "generics", "erasure", "protocol"]
created = "2019-03-01 11:01:50"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Type Erasure

Quite often, when Swift\'s associated types are dicussed, `type erasure`
is mentioned as another solution to the problem of handling the issues
that `associated types` bring along.

Type Erasure in the context of `associated types` solves one particular
problem. We\'ll use computers as an example. Back in the golden age of
desktop operating systems, you could buy a desktop computer with many
non-X86 CPU architectures: PowerPC, Alpha, Sparc, 68000, and so on. One
of the many differences were the `endianness` of the architecture. Lets
model these computers in Swift:

``` Swift
protocol CPU {
    var littleEndian: Bool { get }
}

struct PowerPC: CPU {
    let littleEndian = false
}

struct X86: CPU {
    let littleEndian = true
}
```

Next up, we want to define a protocol for a computer. It could be a
desktop computer or a phone or maybe a game console, so we use a
protocol. In order to model the CPU, we\'re using an `associated type`,
so that the actual type can define the CPU:

``` Swift
protocol Computer {
    associatedtype ProcessorType: CPU
    var processor: ProcessorType { get }
    var processorCount: Int { get }
}
```

Based on this, we can now define a couple of systems:

``` Swift
struct PowerMacG5: Computer {
    let processor = PowerPC()
    let processorCount = 2
}

struct Xbox360: Computer {
    let processor = PowerPC()
    let processorCount = 1
}

struct MacPro: Computer {
    let processor = X86()
    let processorCount = 1
}
```

Now that we have all this, we\'d like to perform a computation on all
**PowerPC** based computers. I.e. something like:

``` Swift
let powerComputers = [PowerMacG5(), Xbox360()]
```

However, what would be the type of this? We can\'t use the `Computer`
protocol, as it contains `associated types`. However, the
`associated types` for the PowerMacG5 **and** the Xbox360 **are** the
same, so in terms of types, Swift ought to understand that those things
are kinda similar. However, there\'s no way to (easily) express this in
the type system; both **PowerMacG5** and **Xbox360** are not the correct
types for the array:

``` Swift
// None of those work
let powerComputers: [PowerMacG5] = [PowerMacG5(), Xbox360]
let powerComputers: [Xbox360] = [PowerMacG5(), Xbox360]
let powerComputers: [Computer] = [PowerMacG5(), Xbox360]
```

Type erasure is a solution for this. The idea is to box the actual type
into a generic wrapper so that Swift can coalesce around wrapper + type.
The solution we\'re aiming for would look like this in the end:

``` Swift
let powerComputers: [AnyComputer<PowerPC>] = [AnyComputer(PowerMacG5()), AnyComputer(Xbox360())]
```

Now we would have our **shared** type, in this case it is
`AnyComputer<CPU>`. Where does this mystic `AnyComputer` come from? We
have to build it ourselves. This is a multi-step process, and requires
quite a bit of boilerplate. We will start simple and expand step by
step. This solution requires multiple types.
