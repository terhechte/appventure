[frontMatter]
title = "Using try / catch in Swift with asynchronous closures"
created = "2015-06-19"
published = true
keywords = ["swift", "try", "catch", "errortype", "closure", "async", "result", "feature"]
slug = "2015-06-19-swift-try-catch-asynchronous-closures.html"
tags = ["swift", "ios"]
---

With Swift 2.0, Apple introduced a new error handling model with the
`try`, `throw`, and `catch` keywords. Given the sub par state of error
handling in Swift 1.0, this was a welcome addition. It works basically
as follows (simplified example):

``` {.Javascript}
// We define a struct conforming to the new ErrorType
enum Error : ErrorType {
    case DivisionError
}
func divide(a: Int, b: Int) throws -> Int {
    if b == 0 {
        throw Error.DivisionError
    }
    return a / b
}
do {
    let result = try divide(50, 10)
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

``` {.Javascript}

func asynchronousWork(completion: (r: NSDictionary?) -> Void) -> Void {
  // do work
  ...
  completion(aDictionary)
}

```

How do you handle errors in these situations? We can expect, that within
the `asynchronousWork` function most error handling will be via
try/catch. So one possible solution that comes to mind is handling the
errors in there, and only forwarding the result, if there is one:

``` {.Javascript}
func asynchronousWork(completion: (r: NSDictionary?) -> Void) -> Void {
    NSURLConnection.sendAsynchronousRequest(request, queue: queue) { 
      (response, data, error) -> Void in
        guard let data = data else { return }
        do {
            let result = try NSJSONSerialization.JSONObjectWithData(data, options: []) 
                as! NSDictionary
            completion(r: result)
        } catch _ {
            completion(r: nil)
        }
    }
}

// Call
asynchronousWork { (r) -> Void in
    guard let r = r else { return}
    print(r)
}
```

# Result Types

However, this is rather fragile, as it will not gives us any information
about the error in question. In Swift 1.0, when such a structure
presented itself, people usually implemented a Result type which can be
either the result of the computation, or the error [^1]:

``` {.Javascript}
enum ResultType {
    case Success(r: NSDictionary)
    case Error(e: ErrorType)
}
```

Given this enum, we can then change the code as follows:

``` {.Javascript}
func asynchronousWork(completion: (r: ResultType) -> Void) -> Void {
    NSURLConnection.sendAsynchronousRequest(request, queue: queue) { 
       (response, data, error) -> Void in
        guard let data = data else { return }
        do {
            let result = try NSJSONSerialization.JSONObjectWithData(data, options: []) 
                as! NSDictionary
            completion(r: ResultType.Success(r: result))
        } catch let error {
            completion(r: ResultType.Error(e: error))
        }
    }
}

// Call
asynchronousWork { (r: ResultType) -> Void in
    switch r {
    case .Success(let e): print(e)
    case .Error(let e): print("Error", e)
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

``` {.Javascrip}

func asynchronousWork(completion: (r: ResultType) -> Void) throws -> Void {
}
```

This can\'t throw, because the function returns before the computation
has even begun.

# A solution with an inner closure

However, a nice way to solve this is by encapsulating the error into a
throwable closure. See for yourself:

``` {.Javascript}

func asynchronousWork(completion: (inner: () throws -> NSDictionary) -> Void) -> Void {
    NSURLConnection.sendAsynchronousRequest(request, queue: queue) { 
        (response, data, error) -> Void in
        guard let data = data else { return }
        do {
            let result = try NSJSONSerialization.JSONObjectWithData(data, options: []) 
                as! NSDictionary
            completion(inner: {return result})
        } catch let error {
            completion(inner: {throw error})
        }
    }
}

// Call
asynchronousWork { (inner: () throws -> NSDictionary) -> Void in
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
`() throws -> NSDictionary`. This closure will either provide the result
of the computation, or it will throw. The closure itself is being
constructed during the computation by one of two means:

-   In case of an error: `inner: {throw error}`
-   In case of success: `inner: {return result}`

This is a simple and flexible way of throwing errors up a closure chain
without any additional means. Much like `rethrow` but for asynchronous
operations.

# Addendum

The only downside of this setup is that it can\'t be used with any
asynchronous operation which takes a completion block. You will need to
have access to the operation in order to rewrite it to not call the
completion block with the result but instead call a completion block
with an inner closure. So you can\'t use it with specific functionality
from external libraries, but it is a good approach for your own code,
frameworks, and libraries, if you like the idea of using the try/catch
approach natively without having to resort to abstraction containers.

[^1]: And with Swift 2.0, the dreaded multi-value enum error
    disappeared, and we can finally implement such a type without having
    to box it.
