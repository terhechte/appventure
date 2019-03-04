[frontMatter]
description = "Several helpful extensions to the Optional type in order to simplify using it."
title = "Useful Optional Extensions"
created = "2018-01-10"
published = true
keywords = ["swift", "protocol", "optional", "optionals", "extensions"]
slug = "2018-01-10-optional-extensions.html"
tags = ["swift", "cocoa", "ios"]

---

`Optionals` are a staple of Swift. I guess everybody will agree that
they are a huge boon insofar as they force us to properly handle edge
cases. The `Optional` language feature alone removes a whole category of
bugs from the development process.

However, the API surface of Swift\'s optional is rather limited. The
[Swift documentation lists just a
couple](https://developer.apple.com/documentation/swift/optional#topics)
of methods / properties on `Optional` - if we ignore `customMirror` and
`debugDescription`:

``` Swift
var unsafelyUnwrapped: Wrapped { get } 
func map<U>(_ transform: (Wrapped) throws -> U) rethrows -> U? 
func flatMap<U>(_ transform: (Wrapped) throws -> U?) rethrows -> U? 
```

The reason why optionals are still very useful even though they have
such a small amount of methods is that the Swift syntax makes up for it
via features such as [optional
chaining](http://appventure.me/2014/06/13/swift-optionals-made-simple/),
[pattern
matching](http://appventure.me/2015/08/20/swift-pattern-matching-in-detail/),
`if let` or `guard let`. In some situations, though, this manifests
itself in unnecessary line noise. Sometimes, a very succinct method will
let you express a concept in one short line of code instead of multiple
lines of combined `if let` statements.

I\'ve sifted through Swift Projects on Github as well as the optional
implementations of other languages such as Rust, Scala, or C\# in order
to find a couple of useful additions to `Optional`. Below are 14 useful
`Optional` extensions. I\'ll describe them by category and then give a
couple of examples per category. Finally, I\'ll write a more involved
example that uses several extensions at once.

# Emptiness

``` Swift
extension Optional {
    /// Returns true if the optional is empty
    var isNone: Bool {
        return self == .none
    }

    /// Returns true if the optional is not empty
    var isSome: Bool {
        return self != .none
    }
}
```

Those are the most basic additions to the optional type. The
implementation could also use a `switch` pattern match instead, but the
`nil` comparison is much shorter. What I like about these additions is
that they move the concept of an empty optional being nil away from your
code. This might just as well be an implementation detail. Using
`optional.isSome` feels much cleaner and less noisy than
`if optional == nil`:

``` Swift
// Compare
guard leftButton != nil, rightButton != nil else { fatalError("Missing Interface Builder connections") }

// With
guard leftButton.isSome, rightButton.isSome else { fatalError("Missing Interface Builder connections") }
```

Or
==

``` Swift
extension Optional {
    /// Return the value of the Optional or the `default` parameter
    /// - param: The value to return if the optional is empty
    func or(_ default: Wrapped) -> Wrapped {
        return self ?? `default`
    }

    /// Returns the unwrapped value of the optional *or*
    /// the result of an expression `else`
    /// I.e. optional.or(else: print("Arrr"))
    func or(else: @autoclosure () -> Wrapped) -> Wrapped {
        return self ?? `else`()
    }

    /// Returns the unwrapped value of the optional *or*
    /// the result of calling the closure `else`
    /// I.e. optional.or(else: { 
    /// ... do a lot of stuff
    /// })
    func or(else: () -> Wrapped) -> Wrapped {
        return self ?? `else`()
    }

    /// Returns the unwrapped contents of the optional if it is not empty
    /// If it is empty, throws exception `throw`
    func or(throw exception: Error) throws -> Wrapped {
        guard let unwrapped = self else { throw exception }
        return unwrapped
    }
}

extension Optional where Wrapped == Error {
    /// Only perform `else` if the optional has a non-empty error value
    func or(_ else: (Error) -> Void) {
        guard let error = self else { return }
        `else`(error)
    }
}
```

Another abstraction on the `isNone / isSome` concept is being able to
specify instructions to be performed when the invariant doesn\'t hold.
This saves us from having to write out `if` or `guard` branches and
instead codifies the logic into a simple-to-understand method.

This concept is so useful, that it is defined in three distinct
functions.

## Default Value

The first one returns the wrapped value of the optional or a default
value:

``` Swift
let optional: Int? = nil
print(optional.or(10)) // Prints 10
```

## Default Closure

The second one is very similar to the first one, however it allows to
return a default value from a closure instead.

``` Swift
let optional: Int? = nil
optional.or(else: secretValue * 32) 
```

Since this uses the `@autoclosure` parameter we could actually use just
the second `or` implementation. Then, using a just a default value would
automatically be converted into a closure returning the value. However,
I prefer having two separate implementations as that allows users to
also write closures with more complex logic.

``` Swift
let cachedUserCount: Int? = nil
...
return cachedUserCount.or(else: {
   let db = database()
   db.prefetch()
   guard db.failures.isEmpty else { return 0 }
   return db.amountOfUsers
})
```

A really nice use case for `or` is code where you only want to set a
value on an optional if it is empty:

``` Swift
if databaseController == nil {
  databaseController = DatabaseController(config: config)
}
```

This can be replaced with the much nicer:

``` Swift
databaseController = databaseController.or(DatabaseController(config: config)
```

## Throw an error

This is a very useful addition as it allows to merge the chasm between
Optionals and Error Handling in Swift. Depending on the code that
you\'re using, a method or function may express invalid behaviour by
returning an empty optional (imagine accessing a non-existing key in a
`Dictionary`) or by throwing an `Error`. Combining these two oftentimes
leads to a lot of unnecessary line noise:

``` Swift
func buildCar() throws -> Car {
  let tires = try machine1.createTires()
  let windows = try machine2.createWindows()
  guard let motor = externalMachine.deliverMotor() else {
    throw MachineError.motor
  }
  let trunk = try machine3.createTrunk()
  if let car = manufacturer.buildCar(tires, windows,  motor, trunk) {
    return car
  } else {
    throw MachineError.manufacturer
  }
}
```

In this example, we\'re building a car by combining internal and
external code. The external code (`external_machine` and `manufacturer`)
choose to use optionals instead of error handling. This makes the code
unnecessary complicated. Our `or(throw:)` function makes this much more
readable:

``` Swift
func build_car() throws -> Car {
  let tires = try machine1.createTires()
  let windows = try machine2.createWindows()
  let motor = try externalMachine.deliverMotor().or(throw: MachineError.motor)
  let trunk = try machine3.createTrunk()
  return try manufacturer.buildCar(tires, windows,  motor, trunk).or(throw: MachineError.manufacturer)
}
```

## Handling Errors

The code from the **Throw an error** section above becomes even more
useful when you include the following free function that was proposed by
[Stijn Willems on Github](https://github.com/doozMen). Thanks for the
suggestion!

``` Swift
func should(_ do: () throws -> Void) -> Error? {
    do {
        try `do`()
        return nil
    } catch let error {
        return error
    }
}
```

This free function (alternatively, you could make it a class method on
optional) will perform a `do {} catch {}` block and return an error if
and only if the closure \`do\` resulted in an error. Take, the following
Swift code as an example:

``` Swift
do {
  try throwingFunction()
} catch let error {
  print(error)
}
```

This is one of the basic tennets of error handling in Swift, and it
introduces quite a lot of line noise. With the free function above, you
can reduce it to this simple on-liner:

``` Swift
should { try throwingFunction) }.or(print($0))
```

I feel that there\'re many situations where such a one-liner for error
handling would be very beneficient.

## Map

As we saw above, `map` and `flatMap` are the only methods that Swift
offers on Optionals. However, even those can be improved a bit to be
more versatile in many situations. There\'re two additional variations
on `map` that allow defining a default value similar to how the `or`
variants above are implemented:

``` Swift
extension Optional {
    /// Maps the output *or* returns the default value if the optional is nil
    /// - parameter fn: The function to map over the value
    /// - parameter or: The value to use if the optional is empty
    func map<T>(_ fn: (Wrapped) throws -> T, default: T) rethrows -> T {
        return try map(fn) ?? `default`
    }

    /// Maps the output *or* returns the result of calling `else`
    /// - parameter fn: The function to map over the value
    /// - parameter else: The function to call if the optional is empty
    func map<T>(_ fn: (Wrapped) throws -> T, else: () throws -> T) rethrows -> T {
        return try map(fn) ?? `else`()
    }
}
```

The first one will allow you to `map` the contents of an optional to a
new type `T`. If the optional is empty, you can define a `default` value
that should be used instead:

``` Swift
let optional1: String? = "appventure"
let optional2: String? = nil

// Without
print(optional1.map({ $0.count }) ?? 0)
print(optional2.map({ $0.count }) ?? 0)

// With 
print(optional1.map({ $0.count }, default: 0)) // prints 10
print(optional2.map({ $0.count }, default: 0)) // prints 0
```

The changes are minimal, but we\'re moving away from having to use the
`??` operator and can instead express the operation more clearly with
the `default` keyword.

The second variant is very similar. The main difference is that it
accepts (again) a closure returning value `T` instead of value `T`.
Here\'s a brief example:

``` Swift
let optional: String? = nil
print(optional.map({ $0.count }, else: { "default".count })
```

# Combining Optionals

This category contains four functions that allow you to define relations
between multiple optionals.

``` Swift
extension Optional {
    /// Tries to unwrap `self` and if that succeeds continues to unwrap the parameter `optional`
    /// and returns the result of that.
    func and<B>(_ optional: B?) -> B? {
        guard self != nil else { return nil }
        return optional
    }

    /// Executes a closure with the unwrapped result of an optional.
    /// This allows chaining optionals together.
    func and<T>(then: (Wrapped) throws -> T?) rethrows -> T? {
        guard let unwrapped = self else { return nil }
        return try then(unwrapped)
    }

    /// Zips the content of this optional with the content of another
    /// optional `other` only if both optionals are not empty
    func zip2<A>(with other: Optional<A>) -> (Wrapped, A)? {
        guard let first = self, let second = other else { return nil }
        return (first, second)
    }

    /// Zips the content of this optional with the content of another
    /// optional `other` only if both optionals are not empty
    func zip3<A, B>(with other: Optional<A>, another: Optional<B>) -> (Wrapped, A, B)? {
        guard let first = self,
              let second = other,
              let third = another else { return nil }
        return (first, second, third)
    }
}
```

These four functions all share that they take an additional optional as
a parameter and return another optional value. However, they\'re all
quite different in what they achieve.

## Dependencies

`and<B>(_ optional)` is useful if the unpacking of an optional is only
required as a invariant for unpacking another optional:

``` Swift
// Compare
if user != nil, let account = userAccount() ...

// With
if let account = user.and(userAccount()) ...
```

In the example above, we\'re not interested in the unwrapped contents of
the `user` optional. We just need to make sure that there **is** a valid
user before we call the `userAccount` function. While this relationship
is kinda codified in the `user != nil` line, I personally feel that the
`and` makes it more clear.

## Chaining

`and<T>(then:)` is another very useful function. It allows to chain
optionals together so that the output of unpacking optional `A` becomes
the input of producing optional `B`. Lets start with a simple example:

``` Swift
protocol UserDatabase {
  func current() -> User?
  func spouse(of user: User) -> User?
  func father(of user: User) -> User?
  func childrenCount(of user: User) -> Int
}

let database: UserDatabase = ...

// Imagine we want to know the children of the following relationship:
// Man -> Spouse -> Father -> Father -> Spouse -> children

// Without
let childrenCount: Int
if let user = database.current(), 
   let father1 = database.father(user),
   let father2 = database.father(father1),
   let spouse = database.spouse(father2),
   let children = database.childrenCount(father2) {
  childrenCount = children
} else {
  childrenCount = 0
}

// With
let children = database.current().and(then: { database.spouse($0) })
     .and(then: { database.father($0) })
     .and(then: { database.spouse($0) })
     .and(then: { database.childrenCount($0) })
     .or(0)
```

There\'re a lot of improvements when using the version with `and(then)`.
First of all, you don\'t have to come up with superfluous temporary
variable names (user, father1, father2, spouse, children). Second, we
clearly have less code. Also, using the `or(0)` instead of a complicated
`let childrenCount` is so much easier to read.

Finally, the original Swift example can easily lead to logic errors. You
may not have noticed, but there\'s a bug in the example. When writing
lines like that, copy paste errors can easily be introduced. Do you see
the error?

Yeah, the `children` property should be created by calling
`database.childrenCount(spouse)` but I wrote
`database.childrenCount(father2)` instead. It is difficult to spot
errors like that. The `and(then:)` example makes it much easier because
it always relies on the same variable name `$0`.

## Zipping

This is another variation on an existing Swift concept. The `zip` method
on optional will allow us to combine multiple optionals and unwrap them
together or not at all. I\'ve just provided implementations for `zip2`
and `zip3` but nothing prevents you from going up to `zip22` (Well,
maybe sanity and compiler speed).

``` Swift
// Lets start again with a normal Swift example
func buildProduct() -> Product? {
  if let var1 = machine1.makeSomething(),
    let var2 = machine2.makeAnotherThing(),
    let var3 = machine3.createThing() {
    return finalMachine.produce(var1, var2, var3)
  } else {
    return nil
  }
}

// The alternative using our extensions
func buildProduct() -> Product? {
  return machine1.makeSomething()
     .zip3(machine2.makeAnotherThing(), machine3.createThing())
     .map { finalMachine.produce($0.1, $0.2, $0.3) }
}
```

Less code, clearer code, more beautiful code. However, as a downside,
this code is also more involved. The reader has to know and understand
`zip` in order to easily grasp it.

On
--

``` Swift
extension Optional {
    /// Executes the closure `some` if and only if the optional has a value
    func on(some: () throws -> Void) rethrows {
        if self != nil { try some() }
    }

    /// Executes the closure `none` if and only if the optional has no value
    func on(none: () throws -> Void) rethrows {
        if self == nil { try none() }
    }
}
```

These two short methods will allow you to perform side effects if an
optional is empty or not. In contrast to the already discussed methods,
these ignore the contents of the optional. So `on(some:)` will only
execute the closure `some` if the optional is not empty but the closure
`some` will not get the unwrapped contents of the optional.

``` Swift
/// Logout if there is no user anymore
self.user.on(none: { AppCoordinator.shared.logout() })

/// self.user is not empty when we are connected to the network
self.user.on(some: { AppCoordinator.shared.unlock() })
```

## Various

``` Swift
extension Optional {
    /// Returns the unwrapped value of the optional only if
    /// - The optional has a value
    /// - The value satisfies the predicate `predicate`
    func filter(_ predicate: (Wrapped) -> Bool) -> Wrapped? {
        guard let unwrapped = self,
            predicate(unwrapped) else { return nil }
        return self
    }

    /// Returns the wrapped value or crashes with `fatalError(message)`
    func expect(_ message: String) -> Wrapped {
        guard let value = self else { fatalError(message) }
        return value
    }
}
```

### Filter

This is a simple method which works like an additional guard to only
unwrap the optional if it satisfies a predictate. Here\'s an example.
Imagine we want to upgrade all our old users to a premium account for
sticking with us for a long time:

``` Swift
// Only affect old users with id < 1000
// Normal Swift
if let aUser = user, user.id < 1000 { aUser.upgradeToPremium() }

// Using `filter`
user.filter({ $0.id < 1000 })?.upgradeToPremium()
```

Here, `user.filter` feels like a much more natural implementation. Also,
it only implements what already exists for Swift\'s collections.

### Expect

This is one of my favorites. Also, I shamelessly stole it from Rust.
I\'m trying very hard to never force unwrap anything in my codebase.
Similar for implicitly unwrapped optionals.

However, this is tricky when working with interface builder outlets. A
common pattern that I observed can be seen in the following function:

``` Swift
func updateLabel() {
  guard let label = valueLabel else {
    fatalError("valueLabel not connected in IB")
  }
  label.text = state.title
}
```

The alternative solution, obviously, would be to just to force unwrap
the label, as that leads to a crash just like `fatalError`. Then, I\'d
have to insert `!` though, also it wouldn\'t give me a nice succinct
description of what actually is wrong. The better alternative here is to
use `expect` as implemented above:

``` Swift
func updateLabel() {
  valueLabel.expect("valueLabel not connected in IB").text = state.title
}
```

# Example

So now that we\'ve seen a couple of (hopefully) useful `Optional`
extensions, I\'ll set up an example to better see how some of these
extensions can be combined to simplify optional handling. First, we need
a bit of context. Forgive me for the rather unconventional and
impossible example:

You\'re working in the 80s at a shareware distributor. A lot of student
programmers are working for you and writing new shareware apps and games
every month. You need to keep track of how many were sold. For that, you
recieve an XML file from accounting and you need to parse it and insert
it into the database (isn\'t it awesome how in this version of the 80s
there\'s Swift to love but also XML to hate?). Your software system has
an XML parser and a database (both written in 6502 ASM of course) that
implement the following protocols:

``` Swift
protocol XMLImportNode {
    func firstChild(with tag: String) -> XMLImportNode?
    func children(with tag: String) -> [XMLImportNode]
    func attribute(with name: String) -> String?
}

typealias DatabaseUser = String
typealias DatabaseSoftware = String
protocol Database {
    func user(for id: String) throws -> DatabaseUser
    func software(for id: String) throws -> DatabaseSoftware
    func insertSoftware(user: DatabaseUser, name: String, id: String, type: String, amount: Int) throws
    func updateSoftware(software: DatabaseSoftware, amount: Int) throws
}
```

A typical file looks like this (behold the almighty XML):

``` XML
<users>
 <user name="" id="158">
  <software>
   <package type="game" name="Maniac Mansion" id="4332" amount="30" />
   <package type="game" name="Doom" id="1337" amount="50" />
   <package type="game" name="Warcraft 2" id="1000" amount="10" />
  </software>
 </user>
</users>
```

Our original Swift code to parse the XML looks like this:

``` Swift
enum ParseError: Error {
    case msg(String)
}

func parseGamesFromXML(from root: XMLImportNode, into database: Database) throws {
    guard let users = root.firstChild(with: "users")?.children(with: "user") else {
        throw ParseError.msg("No Users")
    }
    for user in users {
        guard let software = user.firstChild(with: "software")?
                .children(with: "package"),
            let userId = user.attribute(with: "id"),
            let dbUser = try? database.user(for: userId)
            else { throw ParseError.msg("Invalid User") }
        for package in software {
            guard let type = package.attribute(with: "type"),
            type == "game",
            let name = package.attribute(with: "name"),
            let softwareId = package.attribute(with: "id"),
            let amountString = package.attribute(with: "amount")
            else { throw ParseError.msg("Invalid Package") }
            if let existing = try? database.software(for: softwareId) {
                try database.updateSoftware(software: existing, 
                                              amount: Int(amountString) ?? 0)
            } else {
                try database.insertSoftware(user: dbUser, name: name, 
                                              id: softwareId, 
                                            type: type, 
                                          amount: Int(amountString) ?? 0)
            }
        }
    }
}
```

Lets apply what we learned above:

``` Swift
func parseGamesFromXML(from root: XMLImportNode, into database: Database) throws {
    for user in try root.firstChild(with: "users")
                    .or(throw: ParseError.msg("No Users")).children(with: "user") {
        let dbUser = try user.attribute(with: "id")
                    .and(then: { try? database.user(for: $0) })
                    .or(throw: ParseError.msg("Invalid User"))
        for package in (user.firstChild(with: "software")?
                    .children(with: "package")).or([]) {
            guard (package.attribute(with: "type")).filter({ $0 == "game" }).isSome
                else { continue }
            try package.attribute(with: "name")
                .zip3(with: package.attribute(with: "id"), 
                   another: package.attribute(with: "amount"))
                .map({ (tuple) -> Void in
                    switch try? database.software(for: tuple.1) {
                    case let e?: try database.updateSoftware(software: e, 
                                                               amount: Int(tuple.2).or(0))
                    default: try database.insertSoftware(user: dbUser, name: tuple.0, 
                                                           id: tuple.1, type: "game", 
                                                       amount: Int(tuple.2).or(0))
                    }
                }, or: { throw ParseError.msg("Invalid Package") })
        }
    }
}
```

If we look at this, then there\'re two things that immediately come to
mind:

1.  Less Code
2.  More Complicated Looking Code

I deliberately went into overdrive when utilizing the various `Optional`
extensions. Some of them fit better while others seem to be a bit
misplaced. However, the key is not to solely rely on these extensions
(like I did above) when using optionals but instead to mix and match
where it makes most sense. Compare the two implementations and consider
which from the second example you\'d rather implement with Swift\'s
native features and which feel better when using the `Optional`
extensions.
