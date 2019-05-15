[frontMatter]
description = "When thinking about the great language features of Swift, few people think about `typealias` first. However, there're many situations where they can become particularly useful."
title = "The usefulness of typealiases in swift"
created = "2019-05-15"
published = true
keywords = ["typealias", "generics", "struct"]
tags = []

[meta]
feature_image = "/img-content/typealias-code.jpg"
thumbnail = "/img-content/typealias.png"
---
# What is a `typealias`?

When thinking about the great language features of Swift, few people think about the `typealias`. However, there're many situations where a typealias can become useful. This article will give a brief introduction of what a `typealias` is, how you define it, and list multiple examples of how you can use them in your own code. Lets dive in.

A `typealias` is - as the name implies - an alias for a specific type. Types, such as `Int`, `Double`, `UIViewController`, or one of your custom types. A `Int32` and a `Int8` are different types. A type alias, on the other hand, inserts a second name for an existing type into your codebase. For example:

``` swift
typealias Money = Int
```

Creates an alias for the `Int` type. With this, you can use `Money` as if it were `Int` everywhere in your code:

``` swift
struct Bank {
  typealias Money = Int
  private var credit: Money = 0
  mutating func deposit(amount: Money) {
    credit += amount
  }
  mutating func withdraw(amount: Money) {
    credit -= amount
  }
}
```

Above, we have a struct `Bank` that manages money. Instead of using `Int` for our amounts, though, we use our `Money` type. Observe that the `+=` and `-=` operators still work as expected.

You can also mix and match type aliases and the original types. This is possible because, to the Swift compiler, they all resolve to the same thing:

``` swift
struct Bank {
  typealias DepositMoney = Int
  typealias WithdrawMoney = Int
  private var credit: Int = 0
  mutating func deposit(amount: DepositMoney) {
    credit += amount
  }
  mutating func withdraw(amount: WithdrawMoney) {
    credit -= amount
  }
}
```

Here, we're mixing `Int` and our different custom type aliases `DepositMoney` and `WithdrawMoney`.

## Generic Type aliases

In addition to the above, a type aliase can also have generic parameters:

``` swift
typealias MyArray<T> = Array<T>
let newArray: MyArray = MyArray(arrayLiteral: 1, 2, 3)
```

Above, we defined a typealias for `MyArray` that works just like the normal array.
Finally, the generic parameters of your aliased types can even have constraints. Imagine that we want our new `MyArray` to only hold types that conform to `StringProtocol`:

``` swift
typealias MyArray<T> = Array<T> where T: StringProtocol
```

This is already a nice feature as you can quickly define arrays for particular types without having to subclass `Array`. With that said, let us look at some practical applications of these typealias types.

# Practical Applications

## Clearer Code

The first, and obvious, use case is something we already briefly touched on. A type alias can give your code more meaning. In our example `typealias Money = Int` we introduced a clear concept of what the `Money` type is. Using it like `let amount: Money = 0` is much more understandable than `let amount: Int = 0`. In the first example, you know immediately that this is an *amount* of *money*. In the second example, it could be anything: An amount of bikes, an amount of characters, an amount of donuts - who knows!

Obviously, this is not always necessary. If your function signature already clearly explains the type of the parameter (`func orderDonuts(amount: Int)`) then it would be an unnecessary overhead to include another typealias. On the other hand, for variables and constants, it oftentimes improves readability and tremendously improves the documentation. 

## Simpler Optional Closures

Optional closures in Swift are a wee bit unwieldy. The normal definition of a closure accepting one `Int` parameter and returning `Int` looks like this:

``` swift
func handle(action: (Int) -> Int) { ... }
```

Now, if you want to make this closure optional, you can't just add a questionmark:

``` swift
func handle(action: (Int) -> Int?) { ... }
```

After all, this is not an optional closure but instead *a closure that returns optional `Int`*. The right way to do this is by adding parentheses:

``` swift
func handle(action: ((Int) -> Int)?) { ... }
```

This becomes especially ugly if you have multiple of such actions. Below, have have a function that handles a success and failure case, as well as calling an additional closure with the progress of the operation.

``` swift
func handle(success: ((Int) -> Int)?,
            failure: ((Error) -> Void)?,
            progress: ((Double) -> Void)?) {
    
}
```

This small section of code contains *a lot* of parentheses. As we're not aiming to become lispers, we'd like to address this by using typealiases for the different closures:

``` swift
typealias Success = (Int) -> Int
typealias Failure = (Error) -> Void
typealias Progress = (Double) -> Void

func handle2(success: Success?, failure: Failure?, progress: Progress?) { ... }
```

The actual function does look much more readable. While this is good, we did introduce additional syntax through three lines of `typealias`. This, however, might actually help us in the long run, as we will see next.

## Centralizing Defintions

The action handlers in our previous example might not be the only place where this specific type is used. Here's a draft of what a slightly modified class would look like that actually uses the action handler:

``` swift
final class Dispatcher {
  private var successHandler: ((Int) -> Void)?
  private var errorHandler: ((Error) -> Void)?
  
  func handle(success: ((Int) -> Void)?, error: ((Error) -> Void)?) {
    self.successHandler = success
    self.errorHandler = error
    internalHandle()
  }
  
  func handle(success: ((Int) -> Void)?) {
   self.successHandler = success
    internalHandle()
  }
  
  func handle(error: ((Int)-> Void?)) {
    self.errorHandler = error
    internalHandle()
  }
  
  private func internalHandle() {
   ...
  }
}
```

This struct introduces two closures, one for the success and one for the error case. However, we also want to offer convenience functions to call with only the one or the other handler. In the example above, if we want to add another parameter to the success and error handler, say the `HTTPResponse`, we'll need to update a lot of code. `((Int) -> Void)?`  would need to become `((Int, HTTPResponse) -> Void)?` in three places. Similarly for the errorHandler. By using multiple typealiases, we can circumvent this and only have to modify the type in one place:

``` swift
final class Dispatcher {
  typealias Success = (Int, HTTPResponse) -> Void
  typealias Failure = (Error, HTTPResponse) -> Void

  private var successHandler: Success?
  private var errorHandler: Failure?
  
  func handle(success: Success?, error: Failure?) {
    self.successHandler = success
    self.errorHandler = error
    internalHandle()
  }
  
  func handle(success: Success?) {
   self.successHandler = success
    internalHandle()
  }
  
  func handle(error: Failure?) {
    self.errorHandler = error
    internalHandle()
  }
  
  private func internalHandle() {
   ...
  }
}
```

Not only is this much easier to read, it will also continue to be helpful as we introduce the type in more places.

## Generic Aliases

A typealias can also be generic. One simple use case would be to enforce a container with a special meaning. Say we have an app that processes books. A book consists out of chapters, chapters consist out of pages. Fundamentally, those are just arrays though. `typealias` to the resuce:

``` swift
struct Page {}
typealias Chapter = Array<Page>
typealias Book = Array<Chapter>
```

This has two benefits compared to just using a array.
1. The code is more explanatory
2. The array that houses the pages can *only* contain pages. Nothing else. 

Coming back to our earlier example of using *success* and *failure* handlers, we can improve this even more by using a generic handler:

``` swift
typealias Handler<In> = (In, HTTPResponse?, Context) -> Void

func handle(success: Handler<Int>?, 
            failure: Handler<Error>?,
           progress: Handler<Double>?,)
```

This composes really well and allows us to write a simpler function, and have one place where we edit the `Handler`.

This approach is also very useful with your own types. You can create one generic definition and then define detailed typealiases:

``` swift
struct ComputationResult<T> {
  private var result: T
}

typealias DataResult = ComputationResult<Data>
typealias StringResult = ComputationResult<String>
typealias IntResult = ComputationResult<Int>
```

Again, the typealias allows us to write less code and simplifies our definitions.

## Tuples like Functions

Similarly, you can use generics and tuples to define types without having to resort to structs. Below, we envision the datatype for a genetic algorithm that modifies its value `T` over multiple generations.

``` swift
typealias Generation<T: Numeric> = (initial: T, seed: T, count: Int, current: T)
```

If you define a typealias like this, you can actually initialize it like you would initialize a struct:

``` swift
let firstGeneration = Generation(initial: 10, seed: 42, count: 0, current: 10)
```

While this does look like a struct, it is just a type alias for a tuple.

## Combining Protocols

Sometimes you end up in a situation where you have multiple protocols and there is one specific type that should implement them all. Usually this happens when you define a protocol hierachy in order to provide more flexibility.

``` swift
protocol CanRead {}
protocol CanWrite {}
protocol CanAuthorize {}
protocol CanCreateUser {}

typealias Administrator = CanRead & CanWrite & CanAuthorize & CanCreateUser

typealias User = CanRead & CanWrite

typealias Consumer = CanRead

```

Here, we define a permission hierachy. The administrator can do everything, a user can read and write, and a consumer can only read.

## Associated Types

This goes beyond the scope of this article, but the associated types of protocols are also defined via type aliases:

``` swift
protocol Example {
 associatedtype Payload: Numeric
}

struct Implementation: Example {
  typealias Payload = Int
}
```

# Drawbacks

While typealiases are generally a very useful feature, they have one small drawback: If you're new to a codebase, then there's an important difference between these two definitions:

``` swift
func first(action: (Int, Error?) -> Void) {}
func second(action: Success) {}
```

The second one is not immediately obvious. What kind of type is `Success`? How do you construct it? You'll have to option-click it in Xcode in order to understand what it does and how it works. This causes additional overhead. If you use many typealiases, this will take even more time. There's no good solution to this, except that it (as so often) depends on the usecase.

# Final Words

I hope you enjoyed this brief overview of the potential of typealiases. If you have any feedback, [you can find me on twitter.](https://twitter.com/terhechte)
