[frontMatter]
description = "Once you add associated types to an enum the task of creating instances quickly becomes very repetitive. See how a simple trick can greatly simplify this"
title = "Raw value initializers for enums with associated types"
created = "2016-04-23"
published = true
keywords = ["swift", "optional", "enum", "raw", "value", "initializers", "associated", "type"]
slug = "2016-04-23-associated-types-enum-raw-value-initializers.html"
tags = ["enum", "init", "associated"]
category = ["Swift Tricks", "All"]

[meta]
swift_version = "5.0"
---

[Enums](https://appventure.me/2015/10/17/advanced-practical-enum-examples/)
are a beautiful way of structuring information in Swift. Sometimes you
find yourself initializing enums from raw values, maybe because the
values were intermittendly stored somewhere else, say in the
`NSUserDefaults`:

``` Swift
enum Device: String {
  case phone, tablet, watch
}
let aDevice = Device(rawValue: "phone")
print(aDevice)
```

``` {.example}
Prints Optional(main.Device.phone)
```

## The Problem

As soon as you\'re using associated values in your enums, this doesn\'t
work anymore:

``` Swift
enum Example {
   case Factory(workers: Int)
   case House(street: String)
}
```

Swift can\'t create an instance of `Example` because the two cases,
*Factory* and *House* have different associated types (the `workers`
integer and the `street` string. Each invocation of `Example` requires
different parameters, so this can\'t be generalized.

However, that\'s not the case when your associated types all match up:

``` Swift
enum Device {
    case phone(name: String, screenSize: CGSize)
    case watch(name: String, screenSize: CGSize)
    case tablet(name: String, screenSize: CGSize)
}
```

In thise case, all the `associated types` are the same. There\'re a
myriad of other ways to model this, but I found the device `enum` to be
a concise example for what I\'m about to explain. Even though every
`Device` invocation is the same now, you still can\'t just call it with
some sort of raw value and expect the correct type. Instead, what you
have to do is perform a
[match](https://appventure.me/2015/08/20/swift-pattern-matching-in-detail/)
in order to create the correct instance:

``` Swift
import Foundation

enum Device {
    case phone(name: String, screenSize: CGSize)
    case watch(name: String, screenSize: CGSize)
    case tablet(name: String, screenSize: CGSize)

    static func fromDefaults(rawValue: String, name: String, screenSize: CGSize) -> Device? {
        switch rawValue {
        case "phone": return Device.phone(name: name, screenSize: screenSize)
        case "watch": return Device.watch(name: name, screenSize: screenSize)
        case "tablet": return Device.tablet(name: name, screenSize: screenSize)
        default: return nil
        }
    }
}
let b = Device.fromDefaults(rawValue: "phone", name: "iPhone SE", screenSize: CGSize(width: 640, height: 1136))
print(b)
```

``` Swift
prints Optional(main.Device.phone("iPhone SE", (640.0, 1136.0)))
```

This looks ok, but it **is** already a bit of repetitive code. Once you
develop more than just three enum cases / two associated types, this
will quickly get out of hand.

``` Swift
enum Vehicle {
  case .car(wheels: Int, capacity: Int, weight: Int, length: Int, height: Int, width: Int, color: Int, name: Int, producer: Int, creation: NSDate, amountOfProducedUnits: Int)
  case .ship(wheels: Int, capacity: Int, weight: Int, length: Int, height: Int, width: Int, color: Int, name: Int, producer: Int, creation: NSDate, amountOfProducedUnits: Int)
  case .yacht(wheels: Int, capacity: Int, weight: Int, length: Int, height: Int, width: Int, color: Int, name: Int, producer: Int, creation: NSDate, amountOfProducedUnits: Int)
  case .truck(wheels: Int, capacity: Int, weight: Int, length: Int, height: Int, width: Int, color: Int, name: Int, producer: Int, creation: NSDate, amountOfProducedUnits: Int)
  case .motorbike(wheels: Int, capacity: Int, weight: Int, length: Int, height: Int, width: Int, color: Int, name: Int, producer: Int, creation: NSDate, amountOfProducedUnits: Int)
  case .helicopter(wheels: Int, capacity: Int, weight: Int, length: Int, height: Int, width: Int, color: Int, name: Int, producer: Int, creation: NSDate, amountOfProducedUnits: Int)
  case .train(wheels: Int, capacity: Int, weight: Int, length: Int, height: Int, width: Int, color: Int, name: Int, producer: Int, creation: NSDate, amountOfProducedUnits: Int)
  ...
}
```

I think you get my point.

## The Solution

So.. how do we solve this? Interestingly, there\'s a quirky similarity
between the initializer of an associated type and a closure. Take this
code:

``` Swift
enum Example {
  case test(x: Int)
}
let exampleClosure = Example.test
```

What is the type of `exampleClosure` here? The type is
`(Int) -> Example`. That\'s right, calling an associated value `enum`
case without any parameters will yield a closure that, when called with
the correct types, will return an instance of said type.

This means that, the following is valid, working Swift:

``` Swift
enum Fruit {
  case apple(amount: Int)
  case orange(amount: Int)
}
let appleMaker = Fruit.apple
let firstApple = appleMaker(amount: 10)
let secondApple = appleMaker(amount: 12)

print(firstApple, secondApple)
```

So, how would that help us simplify the gross code duplication problem
above? Have a look:

``` Swift
import Foundation

enum Device {
    case phone(name: String, screenSize: CGSize)
    case watch(name: String, screenSize: CGSize)
    case tablet(name: String, screenSize: CGSize)

    private static var initializers: [String: (name: String, screenSize: CGSize) -> Device] = {
        return ["phone": Device.phone, "watch": Device.watch, "tablet": Device.tablet]
    }()

    static func fromDefaults(rawValue: String, name: String, screenSize: CGSize) -> Device? {
        return Device.initializers[rawValue]?(name: name, screenSize: screenSize)
    }
}

let iPhone = Device.fromDefaults(rawValue: "phone", name: "iPhone SE", screenSize: CGSize(width: 640, height: 1134))
print(iPhone)
```

``` Swift
Optional(main.Device.phone("iPhone SE", (640.0, 1134.0)))
```

So, let\'s try to figure out what happened here. We have a new property
`initializers` on our `Device`. It\'s a `Dictionary` of type
`[String: (name: String, screenSize: CGSize) -> Device]`. I.e. something
that maps from a `String` key to a closure with the same type as our
`Device` cases. The dictionary contains the initializers of each of our
distinct cases, simply by using the same trick as above, just handing in
the closure: `phone:Device.phone`

The `fromDefaults` function, then, only has to know the key of the
device we\'d like to create, and it can call the appropriate closure.
This leads to a much shorter implementation, especially for bigger enums
(like our **Vehicle** example above). As you can see, creating a
`Device` instance is then as simple as:

``` Swift
Device.initializers["phone"]?(name: "iPhone 5", screenSize: CGSize(width: 640, height: 1134)))
```

Just as with raw values, in case there is no `enum` case **phone** we\'d
just get an empty optional back.

This solution isn\'t perfect of course. You still have to have the
`initializers` dictionary, however it will be much less repetitve than
having to `match` over all cases manually.

Finally, I suppose it goes without saying that the code above ignores an
important best practice to be concise and to be able to concentrate on
the task at hand; Nevertheless: having stringified code like
`Device.initializers["phone"]` is not the best way to write this.
Instead, those keys should be properly defined somewhere else.
