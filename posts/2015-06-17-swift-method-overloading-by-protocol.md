[frontMatter]
description = "See how you can even overload methods in a generic manner by using protocols"
title = "Generic method overloading by protocol in Swift"
created = "2015-06-17"
published = true
keywords = ["swift", "optional", "simple", "overloading", "method", "protocol", "extensions", "generics", "feature"]
slug = "2015-06-17-swift-method-overloading-by-protocol.html"
tags = ["generics", "protocols", "overload"]
category = ["Language", "All"]

[meta]
swift_version = "5.0"
---

In this article I wanted to delve into a nice generic abstraction in Swift. It resolves around method overloading, so
we will start with a small introduction into general method overloading in Swift.

# Method Overloading in Swift

There\'re multiple ways to overload or override methods in Swift. I
don\'t want to go into the details here. If you\'re interested, [this
blog post has a pretty good
overview](http://sketchytech.blogspot.de/2014/09/swift-overriding-vs-overloading-xcode-6.html).
One of the possible overloading mechanisms is by type:

``` Swift
class Example {
    func method(a : String) -> NSString {
        return a;
    }
    func method(a : UInt) -> NSString {
        return "{\(a)}"
    }
}

Example().method(a: "Foo") // "Foo"
Example().method(a: 123) // "{123}"
```

As you can see, you can call the same method name with different types,
and during compile time the correct code path will be determined and
optimized. So, unlike `Objective-C`, there\'s no runtime dynamic
dispatch to figure out whether the argument to `method` is a String or a
Int.

This is certainly nice, but what if your setup is more complex, and you
don\'t know which kind of type you\'re getting in a generic function:

``` Swift
class DBStore<T> {
    func store(a : T) {
        store T
    }
}
```

Now imagine that T can have different invariants. Let\'s say you have a
protocol \'Storeable\' for objects which can be stored in your database,
and another protocol \'Interim for objects which should only exist
temporarily in memory.

# Generic Method Overloading by Protocol

You want to call \'store\' on all your objects, without having to
dynamically check the type to see if the object is Storeable or Interim.
You can simply do that by adding the protocol:

``` Swift
class DBStore<T> {
    func store<T: Storeable>(a : T) {
        store T
    }

    func store<T: Interim>(a : T) {
        compress T
    }
}
```
Now, you can call the same method in your code, and the correct code
path will be determined at compile time without any overhead.

# Advanced Protocols

With this basic mechanism, you can do much more. as the Swift
documentation points out, we can apply any kind of generic constraints
in order to better structure our types.

> You can overload a generic function or initializer by providing
> different constraints, requirements, or both on the type parameters in
> the generic parameter clause. When you call an overloaded generic
> function or initializer, the compiler uses these constraints to
> resolve which overloaded function or initializer to invoke. ([Apple
> Documentation](https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/Swift_Programming_Language/GenericParametersAndArguments.html#//apple_ref/doc/uid/TP40014097-CH37-ID406))

Here\'re some examples:

``` Swift

/// Call for all Storeable types which are also equatable
func store<T: Storeable where T:Equatable>(a : T) {
    store T
}

/// Call only for collections, whose objects conform to Storeable
func store<T: Storeable>(a: [T]) {
}

/// Alternatively:
func store<T where T.Generator.Element: Storeable>(a: T) {
}

```

You can also extend your Structs and Classes from a different file, to
add additional functionality based on a value or object which is local
to that class

``` Swift
// Objects which are stored in the cloud
protocol CloudStorable {
}

extension DBStore {
    func store<T: CloudStorable> {
      // write your custom cloud store code
    }
}
```

All in all this gives you great flexibility without the overhead of
dynamic dispatch.
