[frontMatter]
description = "Swift's `try` / `catch` error handling is great. However, you can't use it in an async context. This article briefly explains which options you have if you intend to use Error Handling asynchronously"
title = "Using try / catch in Swift with asynchronous closures"
created = "2015-06-19"
published = true
keywords = ["swift", "try", "catch", "errortype", "closure", "async", "result", "feature"]
slug = "2015-06-19-swift-try-catch-asynchronous-closures.html"
tags = ["try", "catch"]
category = ["Language", "All"]

[meta]
swift_version = "5.0"
---

With Swift 2.0, Apple introduced a new error handling model with the
`try`, `throw`, and `catch` keywords. Given the sub par state of error
handling in Swift 1.0, this was a welcome addition. It works basically
as follows (simplified example):

``` Swift
// We define a struct conforming to the new ErrorType
enum OurError : ErrorType {
    case divisionError
}
func divide(a: Int, b: Int) throws -> Int {
    if b == 0 {
        throw OurError.divisionError
    }
    return a / b
}
do {
    let result = try divide(a: 50, b: 10)
} catch let error {
    print("Could not divide")
}
```

This is a nice and flexible way of structuring possible errors types and
handling them. **In synchronous code**.

But what about asynchronous operations?

# An asynchronous operation

Imagine the following operation as an example of any kind of
asynchronous operation where there is a delay between the initiation of
a computation and the result of the computation. In Objective-C land,
this is solved with delegates, blocks or (though rarely) NSInvocation,
in Swift the typical solution is a closure.

``` Swift
func asynchronousWork(completion: (r: [String: Any]?) -> Void) -> Void {
  // do work
  ...
  completion(someValue)
}
```

How do you handle errors in these situations? We can expect, that within
the `asynchronousWork` function most error handling will be via
try/catch. So one possible solution that comes to mind is handling the
errors in there, and only forwarding the result, if there is one:

``` Swift
func asynchronousWork(completion: (result: [String: Any]?) -> Void) -> Void {
    URLConnection.sendAsynchronousRequest(request, queue: queue) { 
      (response, data, error) -> Void in
        guard let data = data else { return }
        do {
            let result = try JSONSerialization.JSONObjectWithData(data, options: []) as? [String: Any]
            completion(r: result)
        } catch _ {
            completion(r: nil)
        }
    }
}

// Call
asynchronousWork { (result) -> Void in
    guard let result = result else { return}
    print(result)
}
```

# Result Types

However, this is rather fragile, as it will not gives us any information
about the error in question. In Swift 1.0, when such a structure
presented itself, people usually implemented a Result type which can be
either the result of the computation, or the error:

``` Swift
enum Result {
    case success(r: [String: Any])
    case failure(e: ErrorType)
}
```

# Swift 5 Result

Swift 5 now contains a `Result` type in the standard library. It is similar to the one we used above. This
means the names of the two cases are also `success` and `failure`. The name of the type is `Result`.

Given this enum, we can then change the code as follows:

``` Swift
func asynchronousWork(completion: (result: Result) -> Void) -> Void {
    URLConnection.sendAsynchronousRequest(request, queue: queue) { 
       (response, data, error) -> Void in
        guard let data = data else { return }
        do {
            let result = try JSONSerialization.JSONObjectWithData(data, options: []) 
                as? [String: Any]
            completion(r: Result.success(r: result))
        } catch let error {
            completion(r: Result.failure(e: error))
        }
    }
}

// Call
asynchronousWork { (result: Result) -> Void in
    switch r {
    case .success(let successValue): print(successValue)
    case .failure(let error): print("Error", error)
    }
}
```

Much nicer. When we look closely, though, there is a bit of overhead. We
have to define a ResultType enum and encapsulate our data in it. What\'s
more, if Result enums were the way Apple intends things to be, surely we
would have one in the standard library.

Instead, we do have try / catch, a construct which is incompatible with
the task at hand because you can\'t catch something that happens at some
point in the future. I.e:

``` Swift

func asynchronousWork(completion: (result: Result) -> Void) throws -> Void {
}
```

This can\'t throw, because the function returns before the computation
has even begun.

# A solution with an inner closure

However, a nice way to solve this is by encapsulating the error into a
throwable closure. See for yourself:

``` Swift

func asynchronousWork(completion: (inner: () throws -> [String: Any]) -> Void) -> Void {
    URLConnection.sendAsynchronousRequest(request, queue: queue) { 
        (response, data, error) -> Void in
        guard let data = data else { return }
        do {
            guard let result = try JSONSerialization.JSONObjectWithData(data, options: []) 
                as? [String: Any] else {
                completion(inner: { throw OurError.InvalidJSONType })
            }
            completion(inner: { return result })
        } catch let error {
            completion(inner: { throw error })
        }
    }
}

// Call
asynchronousWork { (inner: () throws -> [String: Any]) -> Void in
    do {
        let result = try inner()
    } catch let error {
        print(error)
    }
}

```

We successfully performed the asynchronous work while maintaining the
possibility to catch the error in our calling function\'s completion
block and being able to match different error types - all without having
to resort to enums or switches. How did we do this?

As you can see, the trick is that the asynchronousWork function takes an
additional closure called \'inner\' of the type
`() throws -> [String: Any]`. This closure will either provide the result
of the computation, or it will throw. The closure itself is being
constructed during the computation by one of two means:

-   In case of an error: `inner: {throw error}`
-   In case of success: `inner: {return result}`

This is a simple and flexible way of throwing errors up a closure chain
without any additional means. Much like `rethrow` but for asynchronous
operations.

We also had to add an additional error for the case where our JSON was
not of the `[String: Any]` type.

# Addendum

The only downside of this setup is that it can\'t be used with any
asynchronous operation which takes a completion block. You will need to
have access to the operation in order to rewrite it to not call the
completion block with the result but instead call a completion block
with an inner closure. So you can\'t use it with specific functionality
from external libraries, but it is a good approach for your own code,
frameworks, and libraries, if you like the idea of using the try/catch
approach natively without having to resort to abstraction containers.

