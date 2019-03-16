[frontMatter]
title = "Hiding Behind Protocols"
tags = ["box", "associated", "protocol"]
created = "2019-03-01 11:01:50"
description = ""
published = true

[meta]
swift_version = "5.1"
---

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
