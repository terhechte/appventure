[frontMatter]
description = "Tuples are one of Swift's less visible language features. They occupy a small space between Structs and Arrays. In addition, there's no comparable construct in Objective-C (or many other languages). Finally, the use of tuples in the standard library and in Apple's example code is sparse. The following guide tries to give a more comprehensive overview of tuples with best practices of when to use them, and when not to use them. I'll also try to list those things that you can't do with tuples, to spare you asking about them on stack overflow."
title = "Tuples in Swift, Advanced Usage and Best Practices"
created = "2015-07-19"
published = true
keywords = ["swift", "tuples", "generics", "feature"]
slug = "2015-07-19-tuples-swift-advanced-usage-best-practices.html"
tags = ["swift"]
---

<h6><a href="http://swift.gg/2015/10/10/tuples-swift-advanced-usage-best-practices/">An older version of this post is also available in <b>🇨🇳Chinese</b></a><span> Thanks to </span><a href="http://swift.gg/tags/APPVENTURE/">SwiftGG</a></h6>

Tuples are one of Swift\'s less visible language features. They occupy a
small space between Structs and Arrays. In addition, there\'s no
comparable construct in Objective-C (or many other languages). Finally,
the usage of tuples in the standard library and in Apple\'s example code
is sparse. One could get the impression that their raison d\'être in
Swift is pattern matching, but I disgress.

Most tuple explanations concentrate on three tuple use cases (pattern
matching, return values, destructuring) and leave it at that. The
following guide tries to give a more comprehensive overview of tuples
with best practices of when to use them and when not to use them. I\'ll
also try to list those things that you can\'t do with tuples, to spare
you asking about them on stack overflow. Let\'s dive in.

# The absolute basics

You probably already know most of this, so I\'ll keep it concise.

A tuple can combine different types into one. Tuples are value types and
even though they look like sequences they aren\'t sequences, as there\'s
no direct way of looping over the contents. We\'ll start with a quick
primer on how to create and use tuples.

## Creating and Accessing Tuples

``` Swift
// Constructing a simple tuple
let tp1 = (2, 3)
let tp2 = (2, 3, 4)

// Constructing a named tuple
let tp3 = (x: 5, y: 3)

// Different types
let tp4 = (name: "Carl", age: 78, pets: ["Bonny", "Houdon", "Miki"])

// Accessing tuple elements
let tp5 = (13, 21)
tp5.0 // 13
tp5.1 // 21

let tp6 = (x: 21, y: 33)
tp6.x // 21
tp6.y // 33

```

## Tuples for pattern matching

As already mentioned above, this feels like the strongest use case for
tuples. Swift\'s `switch` statement offers a really powerful yet easy
way to define complex conditionals without cluttering up the source
code. You can then match for the type, existence, and value of multiple
variables in one statement:

``` Swift

// Contrived example
// These would be return values from various functions.
let age = 23
let job: String? = "Operator"
let payload: Any = ["cars": 1]

```

In the code above, we want to find the persons younger than 30 with a
job and a Dictionary payload. Imagine the payload as something from the
Objective-C world, it could be a Dictionary or an Array or a Number,
awful code somebody else wrote years ago, and you have to interact with
it now.

``` Swift

typealias AnyDictionary = Dictionary<AnyHashable, Any>

switch (age, job, payload) {
case (let age, _?, _ as AnyDictionary) where age < 30:
    print(age)
default:
    break
}

```

By constructing the switch argument as a tuple `(age, job, payload)` we
can query for specific or nonspecific attributes of all tuple elements
at once. This allows for elaborately constrained conditionals.

## Tuples as return types

Probably the next-best tuple use case. Since tuples can be constructed
on the fly, they\'re a great way to easily return multiple values from a
function.

``` Swift
func abc() -> (Int, Int, String) {
    return (3, 5, "Carl")
}
```

## Tuple Destructuring

Swift took a lot of inspiration from different programming languages,
and this is something that Python has been doing for years. While the
previous examples mostly showed how to easily get something into a
tuple, destructuring is a swifty way of getting something out of a
tuple, and in line with the `abc` example above, it looks like this:

``` Swift
let (a, b, c) = abc()
print(a)
```

Another example is getting several function calls into one line:

``` Swift
let (a, b, c) = (a(), b(), c())
```

Or, an easy way to swap two values:

``` Swift
var v1: Int
var v2: Int
(v1, v2) = (5, 4)
(a: v1, b: v2) = (a: v2, b: v1) // swapped: v1 == 4, v2 == 5
(v1, v2) = (5, 4)
(a: v1, b: v2) = (b: v1, a: v2) // swapped: v1 == 4, v2 == 5

```

# Beyond the basics

## Tuples as anonymous structs

Tuples as well as structs allow you to combine different types into one
type:

``` Swift
let user1 = (name: "Carl", age: 40)
// vs.
struct User {
    let name: String
    let age: Int
}
let user2 = User(name: "Steve", age: 39)
```

As you can see, these two types are similar, but whereas the tuple
exists simply as an instance, the struct requires both a struct
declaration and a struct initializer. This similarity can be leveraged
whenever you have the need to define a temporary struct inside a
function or method. As the Swift docs say:

> Tuples are useful for temporary groups of related values. (...) If
> your data structure is likely to persist beyond a temporary scope,
> model it as a class or structure (...)

As an example of this, consider the following situation where the return
values from several functions first need to be uniquely collected and
then inserted:

``` Swift
func zipForUser(userid: String) -> String { return "12124" }
func streetForUser(userid: String) -> String { return "Charles Street" }
let users = [user1]

// Find all unique streets in our userbase
var streets: [String: (zip: String, street: String, count: Int)] = [:]
for user in users {
    let zip = zipForUser(userid: user.name)
    let street = streetForUser(userid: user.name)
    let key = "\(zip)-\(street)"
    if let (_, _, count) = streets[key] {
        streets[key] = (zip, street, count + 1)
    } else {
        streets[key] = (zip, street, 1)
    }
}

// drawStreetsOnMap(streets.values)
for street in streets.values { print(street) }
```

Here, the tuple is being used as a simple structure for a short-duration
use case. Defining a struct would also be possible but not strictly
necessary.

Another example would be a class that handles algorithmic data, and
you\'re moving a temporary result from one method to the next one.
Defining an extra struct for something only used once (in between two or
three methods) may not be required.

``` Swift
// Made up algorithm
func calculateInterim(values: [Int]) -> (r: Int, alpha: CGFloat, chi: (CGFloat, CGFloat)) {
    return (values[0], 2, (4, 8))
}
func expandInterim(interim: (r: Int, alpha: CGFloat, chi: (CGFloat, CGFloat))) -> CGFloat {
    return CGFloat(interim.r) + interim.alpha + interim.chi.0 + interim.chi.1
}

print(expandInterim(interim: calculateInterim(values: [1])))
```

There is, of course, a fine line here. Defining a struct for one
instance is overly complex; defining a tuple 4 times instead of one
struct is overly complex too. Finding the sweet spot depends on various
factors.

## Private State

In addition to the previous example, there are also use cases where
using tuples beyond a temporary scope is useful. Following Rich
Hickey\'s \"If a tree falls in the woods, does it make a sound?\", as
long as the scope is private and the tuple\'s type isn\'t littered all
over the implementation, using tuples to store internal state can be
fine.

A simple and contrived example would be storing a static UITableView
structure that displays various information from a user profile and
contains the key path to the actual value as well as a flag noting
whether the value can be edited when tapping on the cell.

``` Swift
let tableViewValues = [
    (title: "Age", value: "user.age", editable: true),
    ("Name",           "user.name.combinedName",  true),
    ("Username",       "user.name.username",      false),
    ("ProfilePicture", "user.pictures.thumbnail", false)]
```

The alternative would be to define a struct, but if the data is a purely
private implementation detail, a tuple works just as well.

A better example is when you define an object and want to add the
ability to add multiple change listeners to your object. Each listener
consists of a name and the closure to be called upon any change:

``` Swift
typealias Action = (_ change: Any?) -> Void
func addListener(name: String, action: @escaping Action) { }
func removeListener(name: String) { }
```

How will you store these listeners in your object? The obvious solution
would be to define a struct, but this is a very limited scope, and the
struct will only be internal, and it will be used in only three cases.
Here, using a tuple may even be the better solution, as the
destructuring makes things simpler:

``` Swift

class ListenerStuff {

    typealias Action = (_ change: Any?) -> Void

    var listeners: [(String, Action)] = []

    func addListener(name: String, action: @escaping Action) {
        listeners.append((name, action))
    }

    func removeListener(name: String) {
        if let idx = listeners.index(where: { $0.0 == name }) {
            listeners.remove(at: idx)
        }
    }

    func execute(change: Int) {
        for (_, listener) in listeners {
            listener(change as Any?)
        }
    }
}

var stuff = ListenerStuff()
let ourAction: ListenerStuff.Action = { x in print("Change is \(x ?? "NONE").") }
stuff.addListener(name: "xx", action: ourAction)
stuff.execute(change: 17)
```

As you can see in the `execute` function, the destructuring abilities
make tuples especially useful in this case, as the contents are directly
destructured into the local scope.

## Tuples as Fixed-Size Sequences

Another area where tuples can be used is when you intend to constrain a
type to a fixed number of items. Imagine an object that calculates
various statistics for each month in a year. You need to store a certain
Integer value for each month separately. The solution that comes to mind
first would of course be:

``` Swift
var monthValuesArray: [Int]
```

However, in this case we don\'t know whether the property indeed
contains 12 elements. A user of our object could accidentally insert 13
values, or 11. We can\'t tell the type checker that this is a fixed size
array of 12 items[^1]. With a tuple, this specific constraint can easily
be put into place:

``` Swift
var monthValues: (Int, Int, Int, Int, Int, Int, Int, Int, Int, Int, Int, Int)
```

The alternative would be to have the constraining logic in the object\'s
functionality (say via a `guard` statement); however, this would be a
run time check. The tuple check happens at compile time; your code
won\'t even compile if you try to give 11 months to your object.

## Tuples for Varargs Types

Varargs i.e. variable function arguments are a very useful technique for
situations where the number of function parameters is unknown.

``` Swift
// classic example
func sum(of numbers: Int...) -> Int {
    // add up all numbers with the + operator
    return numbers.reduce(0, +)
}

let theSum = sum(of: 1, 2, 5, 7, 9) // 24
```

A tuple can be useful here if your requirement goes beyond simple
integers. Take this function, which does a batch update of `n` entities
in a database:

``` Swift
func batchUpdate(updates: (String, Int)...) {
    self.db.begin()
    for (key, value) in updates {
        self.db.set(key, value)
    }
    self.db.end()
}

// We're imagining a weird database
batchUpdate(updates: ("tk1", 5), ("tk7", 9), ("tk21", 44), ("tk88", 12))
```

# Advanced Tuples

## Tuple Iteration

In the above descriptions, I\'ve tried to steer clear of calling tuples
sequences or collections because they aren\'t. Since every element of a
tuple can have a different type, there\'s no type-safe way of looping or
mapping over the contents of a tuple. Well, no beautiful one, that is.

Swift does offer limited reflection capabilities, and these allow us to
inspect the elements of a tuple and loop over them. The downside is that
the type checker has no way to figure out what the type of each element
is, and thus everything is typed as `Any`. It is your job then to cast
and match this against your possible types to figure out what to do.

``` Swift
let t = (a: 5, b: "String", c: Date())

let mirror = Mirror(reflecting: t)
for (label, value) in mirror.children {
    switch value {
    case is Int:
        print("int")
    case is String:
        print("string")
    case is NSDate:
        print("nsdate")
    default: ()
    }
}
```

This is not as simple as array iteration, but it does work if you really
need it.

## Tuples and Generics

There\'s no `Tuple` type available in Swift. If you wonder why that is,
think about it: every tuple is a totally different type, depending on
the types within it. So instead of defining a generic tuple requirement,
you define the specific but generic incarnation of the tuple you intend
to use:

``` Swift
func wantsTuple<T1, T2>(_ tuple: (T1, T2)) -> T1 {
    return tuple.0
}

wantsTuple(("a", "b")) // "a"
wantsTuple((1, 2)) // 1
```

You can also use tuples in `typealiases`, thus allowing subclasses to
fill out your types with details. This looks fairly useless and
complicated, but I\'ve already had a use case where I need to do exactly
this.

``` Swift
class BaseClass<A,B> {
    typealias Element = (A, B)
    func add(_ elm: Element) {
        print(elm)
    }
}
class IntegerClass<B> : BaseClass<Int, B> {
}
let example = IntegerClass<String>()
example.add((5, ""))
// Prints (5, "")
```

## Define a Specific Tuple Type

In many of the earlier examples, we rewrote a certain tuple type like
`(Int, Int, String)` multiple times. This, of course, is not necessary,
as we could define a `typealias` for it:

``` Swift
typealias Example = (Int, Int, String)
func add(elm: Example) { }
```

However, if you\'re using a certain tuple construction so often that you
think about adding a typealias for it, you might really be better off
defining a struct.

## Tuples as function parameters

[Swift 3 removed the tuple splat
feature](https://github.com/apple/swift-evolution/blob/master/proposals/0029-remove-implicit-tuple-splat.md),
which used to be described in this section.

If you pass a tuple as a parameter to a function, it always works as you
would expect: the tuple is available as an immutable variable in the
function.

## Tuples to reorder function parameters

[Swift 3 removed the tuple splat
feature](https://github.com/apple/swift-evolution/blob/master/proposals/0029-remove-implicit-tuple-splat.md),
which was the basis for tricks discussed in this section.

# Tuple impossibilities

Finally, we reach the list of some of the things that are impossible to
achieve with tuples.

## Tuples as Dictionary Keys

If you\'d like to do the following:

``` Swift
let p: [(Int, Int): String]
```

Then this is not possible, because tuples don\'t conform to the Hashable
protocol. Which is really a bummer, as the example above has a multitude
of use cases. There may be a crazy type checker hack to extend tuples of
varying arities to the Hashable protocol, but I haven\'t really looked
into that. If you happen to know if this works, feel free to contact me
via [twitter](http://twitter.com/terhechte).

## Tuple Protocol Compliance

Given the following protocol:

``` Swift
protocol PointProtocol {
    var x: Int { get }
    var y: Int { get }
}
```

You can\'t get the type checker to accept the tuple `(x: 10, y: 20)` as
implementing that protocol.

``` Swift
func addPoint(point: PointProtocol)
addPoint(point: (x: 10, y: 20) as PointProtocol) // doesn't work.
```

The compiler complains, \"\'(x: Int, y: Int)\' is not convertible to
\'PointProtocol\'; did you mean to use \'as!\' to force downcast?
(Answer: no.)

# Addendum

That\'s it. I probably forgot one or another thing. Things may also be
wrong. If you find a factual error, or if there\'s something else I
forgot, feel free to [contact me](http://twitter.com/terhechte).

# The code, suitable for use in a playground

``` Swift
import AppKit

// * Creating and Accessing Tuples

// Constructing a simple tuple
let tp1 = (2, 3)
let tp2 = (2, 3, 4)

// Constructing a named tuple
let tp3 = (x: 5, y: 3)

// Different types
let tp4 = (name: "Carl", age: 78, pets: ["Bonny", "Houdon", "Miki"])

// Accessing tuple elements
let tp5 = (13, 21)
tp5.0 // 13
tp5.1 // 21

let tp6 = (x: 21, y: 33)
tp6.x // 21
tp6.y // 33


// * Tuples for pattern matching

// Contrived example
// These would be return values from various functions.
let age = 23
let job: String? = "Operator"
let payload: Any = ["cars": 1]

typealias AnyDictionary = Dictionary<AnyHashable, Any>

switch (age, job, payload) {
case (let age, _?, _ as AnyDictionary) where age < 30:
    print(age)
default: ()
}


// * Tuples as return types

func abc() -> (Int, Int, String) {
    return (3, 5, "Carl")
}


// * Tuple Destructuring

let (a, b, c) = abc()
print(a)

func f1() -> Int { return 1 }
func f2() -> Int { return 2 }
func f3() -> Int { return 3 }

let (r1, r2, r3) = (f1(), f2(), f3())

var v1: Int
var v2: Int
(v1, v2) = (5, 4)
(a: v1, b: v2) = (a: v2, b: v1) // swapped: v1 == 4, v2 == 5
(v1, v2) = (5, 4)
(a: v1, b: v2) = (b: v1, a: v2) // swapped: v1 == 4, v2 == 5


// * Tuples as anonymous structs

let user1 = (name: "Carl", age: 40)
// vs.
struct User {
    let name: String
    let age: Int
}
let user2 = User(name: "Steve", age: 39)

func zipForUser(userid: String) -> String { return "12124" }
func streetForUser(userid: String) -> String { return "Charles Street" }
let users = [user1]

// Find all unique streets in our userbase
var streets: [String: (zip: String, street: String, count: Int)] = [:]
for user in users {
    let zip = zipForUser(userid: user.name)
    let street = streetForUser(userid: user.name)
    let key = "\(zip)-\(street)"
    if let (_, _, count) = streets[key] {
        streets[key] = (zip, street, count + 1)
    } else {
        streets[key] = (zip, street, 1)
    }
}

// drawStreetsOnMap(streets.values)
for street in streets.values {
    print(street)
}


// Made up algorithm
func calculateInterim(values: [Int]) -> (r: Int, alpha: CGFloat, chi: (CGFloat, CGFloat)) {
    return (values[0], 2, (4, 8))
}
func expandInterim(interim: (r: Int, alpha: CGFloat, chi: (CGFloat, CGFloat))) -> CGFloat {
    return CGFloat(interim.r) + interim.alpha + interim.chi.0 + interim.chi.1
}

print(expandInterim(interim: calculateInterim(values: [1])))


// * Private State

let tableViewValues = [
    (title: "Age", value: "user.age", editable: true),
    ("Name",           "user.name.combinedName",  true),
    ("Username",       "user.name.username",      false),
    ("ProfilePicture", "user.pictures.thumbnail", false)]


class ListenerStuff {

    typealias Action = (_ change: Any?) -> Void

    var listeners: [(String, Action)] = []

    func addListener(name: String, action: @escaping Action) {
        listeners.append((name, action))
    }

    func removeListener(name: String) {
        if let idx = listeners.index(where: { $0.0 == name }) {
            listeners.remove(at: idx)
        }
    }

    func execute(change: Int) {
        for (_, listener) in listeners {
            listener(change as Any?)
        }
    }
}

var stuff = ListenerStuff()
let ourAction: ListenerStuff.Action = { x in print("Change is \(x ?? "NONE").") }
stuff.addListener(name: "xx", action: ourAction)
stuff.execute(change: 17)


// * Tuples as Fixed-Size Sequences

var monthValuesArray: [Int]


var monthValues: (Int, Int, Int, Int, Int, Int, Int, Int, Int, Int, Int, Int)


// * Tuples for Varargs Types

// classic example
func sum(of numbers: Int...) -> Int {
    // add up all numbers with the + operator
    return numbers.reduce(0, +)
}

let theSum = sum(of: 1, 2, 5, 7, 9) // 24
print(theSum)

func batchUpdate(updates: (String, Int)...) {
    //self.db.begin()
    for (key, value) in updates {
        print("self.db.set(\"\(key)\", \(value))")
        //self.db.set(key, value)
    }
    //self.db.end()
}

// We're imagining a weird database
batchUpdate(updates: ("tk1", 5), ("tk7", 9), ("tk21", 44), ("tk88", 12))


// * Advanced Tuples

// ** Tuple Iteration

let t = (a: 5, b: "String", c: Date())

let mirror = Mirror(reflecting: t)
for (label, value) in mirror.children {
    switch value {
    case is Int:
        print("int")
    case is String:
        print("string")
    case is NSDate:
        print("nsdate")
    default: ()
    }
}

// ** Tuples and Generics

func wantsTuple<T1, T2>(_ tuple: (T1, T2)) -> T1 {
    return tuple.0
}

let tr1 = wantsTuple(("a", "b")) // "a"
let tr2 = wantsTuple((1, 2)) // 1


class BaseClass<A,B> {
    typealias Element = (A, B)
    func add(_ elm: Element) {
        print(elm)
    }
}
class IntegerClass<B> : BaseClass<Int, B> {
}
let example = IntegerClass<String>()
example.add((5, ""))
// Prints (5, "")


// ** Define a Specific Tuple Type

typealias Example = (Int, Int, String)
func add(elm: Example) { }


// ** Tuples as Dictionary Keys


// let p: [(Int, Int): String]  // doesn't compile


// ** Tuple Protocol Compliance

protocol PointProtocol {
    var x: Int { get }
    var y: Int { get }
}

func addPoint(point: PointProtocol) {
    print(point)
}

// addPoint(point: (x: 10, y: 20) as PointProtocol) // doesn't work.
// The compiler complains,
//    "'(x: Int, y: Int)' is not convertible to 'PointProtocol'; did you mean to use 'as!' to force downcast?
```

# Changes

****07/23/2015**** Added section on tuples as function parameters

****08/06/2015**** Updated the Reflection example to the latest Swift
beta 4. (It removes the `reflect` call)

****08/12/2015**** Updated the **Tuples as function parameters** with a
couple more examples and more information.

****08/13/2015**** Fixed a couple of bugs..

****10/28/2015**** Fixed bugs and added a new section on parameter
reordering.

[^1]: Interestingly, something that C can do just fine
