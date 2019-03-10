[frontMatter]
description = "Understand how to model your way around some of the issues that arise when introducing associated typed protocols into your codebase"
title = "Patterns for Working With Associated Types"
created = "2017-12-10"
published = true
keywords = ["swift", "protocol", "protocols", "associated", "associatedtype", "typealias", "pattern", "pat"]
slug = "2017-12-10-patterns-for-working-with-associated-types.html"
tags = ["swift", "cocoa", "ios"]
---

# Useful Patterns for Working Your Way Around Associated Types

This blog post is based [on a talk I
gave](https://www.youtube.com/watch?v=P_ifSjia9mE) at [AppBuilders
2016](https://www.appbuilders.ch/) explaining protocols with associated
types offering tips for using them.

Swift is a powerful language with a very powerful type system. Among the
features that define said type system are `associated types`. They can
be defined on a `protocol` to allow implementors of the `protocol` to
specialize certain types in a generic way:

``` Swift
protocol Example {
  associatedtype Value
  var value: Value { get }
}
```

In the snippet above, any type that implements the `Example` protocol
has to define the `Value` type. Protocols with `associated types` can be
understood as **unfinished types**. Compared to regular protocols, which
can be used within Swift like normal types, those protocols can only be
used as a generic constraint. This means that once your type requires an
`associated type`, using it suddenly becomes much more complicated.

The example below shows an example of ****finishing**** a type. By
explicitly telling the compiler that the `Value` type is `Int` it is now
able to understand `ImplementExample` fully.

``` Swift
struct ImplementExample: Example {
  typealias Value = Int
}
```

Associated types are useful for a certain kind of problems where
subclassing and composition does allow you to [build the right kind of
abstractions](https://www.appbuilders.ch/). However, this is a seperate
topic. The topic of this article, on the other hand, is what to do when
you end up with associated types trouble.

# Associated Types Trouble

The classic example of `associated types` trouble certainly is the
following Swift error message:

``` bash
protocol 'Bookmarkable' can only be used as a generic constraint because it has Self 
or associated type requirements
var bookmarks: [Bookmarkable]
```

This happens once your type conforms to a protocol which conforms to
`Equatable`:

``` Swift
protocol Bookmarkable: Equatable {
}

struct User {
    var bookmarks: [Bookmarkable]
}
```

Here, the problem is that `Equatable` contains a method `==` which has
two paramters of type `Self`. Protocol Methods with `Self` parameters
automatically opt in to `associated types`.

In this article, we will be investigating several patterns that allow
you to work your way around the `associated type` requirement or that
show how such a type can be handled.

# Working Around Associated Types

# Make Your Types Equatable

The first solution for the archetypical problem is also a really simple
one. Instead of enforcing `Equatable` on your custom `protocol`, you can
simply require your full fledged, final, types to conform to the
`Equatable` protocol instead of your custom protocol. Consider the
previously defined `Bookmarkable` protocol:

``` Swift
protocol Bookmarkable {
}

struct Bookmark: Bookmarkable, Equatable {
  var identifier: Int
}

func ==(lhs: Bookmark, rhs: Bookmark) -> Bool {
  return lhs.identifier == rhs.identifier
}

var myBookmarks: [Bookmark] = []
```

In the example above, the `Equatable` requirement actually stems from
the `Bookmark` type conforming to the `Equatable` protocol, not the
`Bookmarkable` protocol itself. The actual `Equatable` information,
however, lies in the new `identifier` property, which has been added to
the `Bookmark` `struct`. As you can easily see, this also requires you
to make the `myBookmarks` array require only elements of type
`Bookmark`. A serious disgression if you\'re used to using protocols
like partially anonymous types. A better solution, if your design allows
for it, goes one step further by enforcing the new `property` which we
introduced in this example.

## Equatable Properties

Here, the idea is that we take one of the types that already implement
`Equatable` in a proper way (i.e. `Int`, `String`, ...) and add a new
`property` requirement to our `Bookmarkable` protocol. Then, we can use
this `property` to add `Equatable` support without actually implementing
`Equatable`:

``` Swift
protocol Bookmarkable {
    var identifier: Int { get }
}

struct Bookmark: Bookmarkable {
    var identifier: Int
}

var myBookmarks: [Bookmarkable] = []
```

The main change, compared to the code above, is that the
`var identifier` moved to the `Bookmarkable` protocol and that we
removed the `func ==`.

While this works better, it still has a major deficit. Since
`Bookmarkable` does not directly comply with `Equatable`, you will not
gain the standard library\'s methods that specifically deal with
`Equatable` types. So instead of being able to call `Array.contains`
like this:

``` Swift
let ourBookmark = Bookmark(identifier: 0)
let result = myBookmarks.contains(ourBookmark)
```

You will have to use the more verbose closure-based version:

``` Swift
let ourBookmark = Bookmark(identifier: 0)

let result = myBookmarks.contains { (bookmark) -> Bool in
    return bookmark.identifier == ourBookmark.identifier
}
```

# Associated Types and Self

Another vector which can introduce `associated types` into your codebase
is the usage of `Self`:

``` Swift
protocol Example {
  /// Indirect Associated Type
  var builder: Self { get }
  /// Indirect Associated Type
  func makeSomething(with example: Self)
}
var myExamples: [Example] = []
```

As you can see in the example above, using `Self` as a method parameter
or using `Self` as a property type automatically introduces an
`associated type` (like we saw with `Equatable`, earlier).

The most helpful note here is that once you use a `method` instead of a
`property` in order to return something of type `Self` you will not opt
in to an `associated type`:

``` Swift
protocol Example {
  /// No Indirect Associated Type
  func builder() -> Self
}
var myExamples: [Example] = []
```

This example works fine. No `indirect associated` type is introduced.

# Method-Only Types

If your `associated type` requirement doesn\'t come from `Equatable`
conformance but instead from your own use, you can double-check if you
actually need these associated types.

Take this example of a validator type:

``` Swift
protocol Validator {
    associatedtype I
    func validate(_ input: I) -> Bool
}
```

As the `associated type` is only used in one method, you can
alternatively just make it a `generic` method and thus save yourself
from introducing unnecessary unfinished types:

``` Swift
protocol Validator {
    func validate<I>(_ input: I) -> Bool
}
```

# Hiding Behind Protocols

This is an especially useful and flexible pattern. It can be used in
many situations where you want to use protocols with `associated types`
like a normal, full fledged type, but still be able to opt in to the
generic part if necessary. The idea here is that you define two
protocols that share common methods. Only one of those protocols
contains `associated types`, the other does not. Your types conform to
both protocols. This means that you can use the **normal** protocol as a
type for all situations. If you, then, need to use the parts of the type
that only affect the `associated type`, you can do so by means of a
runtime cast.

Begin by defining an `associated` Protocol `ExampleAssociatedProtocol`
that is shadowed by a `normal` Protocol `ExampleProtocol`.

``` Swift
/// The `Normal` Protocol
protocol ExampleProtocol {
  var anyValue: Any { get }
}

/// The Protocol with an associated type
protocol ExampleAssociatedProtocol: ExampleProtocol {
  associatedtype Value

  /// Retrieving the actual associated type
  var value: Value { get }
}

/// Conform to the `ExampleProtocol`
extension ExampleAssociatedProtocol {
  var anyValue: Any {
    return value
  }
}
```

Now, you can use the `ExampleProtocol` as a normal type throughout your
app in all situations where a protocol with an `associated type` would
otherwise fail:

``` Swift
struct World {
  var examples: [ExampleProtocol]

  let example: ExampleProtocol

  func generate() -> ExampleProtocol { 
    return example
  }
}
```

However, if you need to access the property that is specific to the
`ExampleAssociatedProtocol` (`value`) then you can do so through at
runtime.

``` Swift
/// Custom type implementing `ExampleAssociatedProtocol`
struct IntExample: ExampleAssociatedProtocol {
  var value: Int
}

/// Custom type implementing `ExampleAssociatedProtocol`
struct StringExample: ExampleAssociatedProtocol {
  var value: String
}

/// Shadowing via `ExampleProtocol`
let myExamples: [ExampleProtocol] = 
    [StringExample(value: "A"), IntExample(value: 10)]

/// Runtime Casting
for aNormalExample in myExamples {
  if let anAssociatedExample = aNormalExample as? IntExample {
    print(anAssociatedExample.value)
  }
  if let anAssociatedExample = aNormalExample as? StringExample {
    print(anAssociatedExample.value)
  }
}
```

This will print \"A10\" as both types (`IntExample` and `StringExample`)
are being identified at runtime via a cast from `ExampleProtocol`.

# Type Erasure

## The Problem

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

## An Abstract Class

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

## A Box Type

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

## Putting it all together

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

# Conclusion

`Associated types` are a powerful concept however they come with a fair
share of difficulties. Most notably, as soon as you introduce an
`associated type` you can\'t use it like you\'d use normal full types.
This article provided several patterns that make it a bit easier to
handle `associated type` problems in your codebase. Each of these
patterns has downsides though. In general, if you intend to use
`associated types` in a `protocol`, one of the best solutions is to try
to only use the types that implement this `protocol` instead of the
`protocol` itself. Because then you don\'t even need those patterns.
