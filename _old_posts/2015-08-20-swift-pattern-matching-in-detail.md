[frontMatter]
description = "In this post, we'll have a look at Pattern Matching in Swift in terms of the 'switch', 'for', 'if', and 'guard' keywords. We'll have a look at the basic syntax and at best practices and helpful examples."
title = "Match Me if you can: Swift Pattern Matching in Detail."
created = "2015-08-20"
published = true
keywords = ["feature", "lisp", "swift", "optional", "scala", "simple", "optionals", "switch", "chaining", "for", "pattern", "matching", "clojure", "haskell"]
slug = "2015-08-20-swift-pattern-matching-in-detail.html"
tags = ["swift", "ios", "cocoa"]
---

<h6><a href="http://swift.gg/2015/10/27/swift-pattern-matching-in-detail/">This post is also available in <b>🇨🇳Chinese</b></a><span> Thanks to </span><a href="http://swift.gg/tags/APPVENTURE/">SwiftGG</a></h6>
<h6><a href="http://qiita.com/mono0926/items/f2875a9eacef53e88122">This post is also available in <b>🇯🇵Japanese</b></a><span> Thanks to </span><a href="https://twitter.com/_mono">M Ono</a></h6>

Among the new features that Swift offers to Objective-C programmers is
one that disguises itself like a boring old man while it offers huge
potential for forming elegant solutions to otherwise unwieldy sets of
nested branches. I\'m, of course talking about the `switch` statement
that many Objective-C programmers probably consider as a clunky syntax
device which is most entertaining when used as [Duff\'s
Device](http://en.wikipedia.org/wiki/Duff's_device), yet usually offers
little to no advantages over multiple if statements.

The `Switch` statement in Swift can do much more though. In the
following tutorial, I will try to explain the various usages for these
new features in more detail. I\'ll mostly ignore those solutions where
there\'s no benefit over how `switch` works in Objective-C or C. The
basics of this post were actually written in July 2014, but so many of
my patterns crashed the compiler back then that I postponed writing it
until there\'s better support.

This Blog Post is also available in the following languages:

# Diving In

The main feature of `switch` is of course pattern matching, the ability
to destructure values and match different switch cases based on correct
match of the values to the cases.

``` Swift
// Example of the worst binary -> decimal converter in history
let bool1 = 1
let bool2 = 0
switch (bool1, bool2) {
   case (0, 0): print("0")
   case (0, 1): print("1")
   case (1, 0): print("2")
   case (1, 1): print("3")
}
```

Pattern matching has long existed in other languages like Haskell,
Erlang, Scala, or Prolog. This is a boon, because it allows us to have a
look at how those languages utilize pattern matching in order to solve
their problems. We can even have a look at their examples to find the
most practical ones that offer real world adaptability.

# A Trading Engine

So Wall Street contacted you, they need a new trading platform running
on iOS devices. As it is a trading platform, you define an `enum` for
trades.

## First Draft

``` Swift
enum Trades {
    case Buy(stock: String, amount: Int, stockPrice: Float)
    case Sell(stock: String, amount: Int, stockPrice: Float)
}
```

You were also handed the following API to handle trades. **Notice how
sell orders are just negative amounts**. And you\'re told the stock
price is not important, their engine will take an internal one anyway.

``` Swift
/**
 - parameter stock: The stock name
 - parameter amount: The amount, negative number = sell, positive = buy
*/
func process(stock: String, _ amount: Int) {
    print ("\(amount) of \(stock)")
}
```

The next step is to process those trades. You see the potential for
using pattern matching and write this:

``` Swift
let aTrade = Trades.Buy(stock: "APPL", amount: 200, stockPrice: 115.5)

switch aTrade {
case .Buy(let stock, let amount, _):
    process(stock, amount)
case .Sell(let stock, let amount, _):
    process(stock, amount * -1)
}
// Prints "buy 200 of APPL"
```

Swift lets us conveniently only destructure / extract the information
from the `enum` that we really want. In this case only the stock and the
amount.

Awesome, you visit Wall Street to show of your fantastic trading
platform. However, as always, the reality is much more cumbersome than
the beautiful theory. Trades aren\'t trades you learn.

-   You have to calculate in a fee which is different based on the
    trader type.
-   The smaller the institution the higher the fee.
-   Also, bigger institutions get a higher priority.

They also realized that you\'ll need a new API for this, so you were
handed this:

``` Swift
func processSlow(stock: String, _ amount: Int, _ fee: Float) { print("slow") }
func processFast(stock: String, _ amount: Int, _ fee: Float) { print("fast") }
```

## Trader Types

So you go back to the drawing board and add another `enum`. The trader
type is part of every trade, too.

``` Swift
enum TraderType {
case SingleGuy
case Company
} 

enum Trades {
    case Buy(stock: String, amount: Int, stockPrice: Float, type: TraderType)
    case Sell(stock: String, amount: Int, stockPrice: Float, type: TraderType)
}

```

So, how do you best implement this new restriction? You could just have
an `if` / `else` switch for buy and for sell, but that would lead to
nested code which quickly lacks clarity - and who knows maybe these Wall
Street guys come up with further complications. So you define it instead
as additional requirements on the pattern matches:

``` Swift

let aTrade = Trades.Sell(stock: "GOOG", amount: 100, stockPrice: 666.0, type: TraderType.Company)

switch aTrade {
case let .Buy(stock, amount, _, TraderType.SingleGuy):
    processSlow(stock, amount, 5.0)
case let .Sell(stock, amount, _, TraderType.SingleGuy):
    processSlow(stock, -1 * amount, 5.0)
case let .Buy(stock, amount, _, TraderType.Company):
    processFast(stock, amount, 2.0)
case let .Sell(stock, amount, _, TraderType.Company):
    processFast(stock, -1 * amount, 2.0)
}
```

The beauty of this is that there\'s a very succinct flow describing the
different possible combinations. Also, note how we changed
`.Buy(let stock, let amount)` into `let .Buy(stock, amount)` in order to
keep things simpler. This will destructure the `enum` just as before,
only with less syntax.

## Guards! Guards!

Once again you present your development to your Wall Street customer,
and once again a new issue pops up (you really should have asked for a
more detailed project description).

-   Sell orders exceeding a total value of \$1.000.000 do always get
    fast handling, even if it\'s just a single guy.
-   Buy orders under a total value of \$1.000 do always get slow
    handling.

With traditional nested `if` syntax, this would already become a bit
messy. Not so with `switch`. Swift includes guards for `switch cases`
which allow you to further restrict the possible matching of those
cases.

You only need to modify your `switch` a little bit to accommodate for
those new changes

``` Swift

let aTrade = Trades.Buy(stock: "GOOG", amount: 1000, stockPrice: 666.0, type: TraderType.SingleGuy)

switch aTrade {
case let .Buy(stock, amount, _, TraderType.SingleGuy):
    processSlow(stock, amount, 5.0)
case let .Sell(stock, amount, price, TraderType.SingleGuy)
    where price*Float(amount) > 1000000:
    processFast(stock, -1 * amount, 5.0)
case let .Sell(stock, amount, _, TraderType.SingleGuy):
    processSlow(stock, -1 * amount, 5.0)
case let .Buy(stock, amount, price, TraderType.Company)
    where price*Float(amount) < 1000:
    processSlow(stock, amount, 2.0)
case let .Buy(stock, amount, _, TraderType.Company):
    processFast(stock, amount, 2.0)
case let .Sell(stock, amount, _, TraderType.Company):
    processFast(stock, -1 * amount, 2.0)
}
```

This code is quite structured, still rather easy to read, and wraps up
the complex cases quite well.

That\'s it, we\'ve successfully implemented our trading engine. However,
this solution still has a bit of repetition; we wonder if there\'re
pattern matching ways to improve upon that. So, let\'s look into pattern
matching a bit more.

# Advanced Pattern Matching

So now we\'ve seen several patterns in action. But what\'s the syntax
here? Which other things can we match for? Swift distinguishes **7**
different patterns. We\'re going to have a quick look at each of them.

All of those patterns can not only be used with the `switch` keyword,
but also with the `if`, `guard`, and `for` keywords. For details on
this, see below.

## 1. Wildcard Pattern

The wildcard pattern ignores the value to be matched against. In this
case any value is possible. This is the same pattern as `let _ = fn()`
where the `_` indicates that you don\'t wish to further use this value.
The interesting part is that this matches all values including `nil`
[^1]. You can even match optionals by appending a `?`:

``` Swift
let p: String? = nil
switch p {
case _?: print ("Has String")
case nil: print ("No String")
}
```

As you\'ve seen in the trading example, it also allows you to omit the
data you don\'t need from matching `enums` or `tuples`:

``` Swift
switch (15, "example", 3.14) {
    case (_, _, let pi): print ("pi: \(pi)")
}
```

## 2. Identifier Pattern

Matches a concrete value. This is how things work in Objective-C\'s
`switch` implementation:

``` Swift
switch 5 {
  case 5: print("5")
}
```

## 3. Value-Binding Pattern

This is the very same as binding values to variables via `let` or `var`.
Only in a switch statement. You\'ve already seen this before, so I\'ll
provide a very short example:

``` Swift
switch (4, 5) {
  case let (x, y): print("\(x) \(y)")
}
```

## 4. Tuple Pattern

[I\'ve written a whole blog post about
tuples,](http://appventure.me/2015/07/19/tuples-swift-advanced-usage-best-practices/)
which offer much more information than this, but here\'s a quick
example:

``` Swift
let age = 23
let job: String? = "Operator"
let payload: AnyObject = NSDictionary()

switch (age, job, payload) {
  case (let age, _?, _ as NSDictionary):
  print(age)
  default: ()
}
```

Here, we\'re combining three values into a tuple (imagine they\'re
coming from different API calls) and matching them in one go. Note that
the pattern achieves three things:

1.  It extracts the age
2.  It makes sure there is a job, even though we don\'t need it
3.  It makes sure that the payload is of kind `NSDictionary` even though
    we don\'t need the actual value either.

## 5. Enumeration Case Pattern

As you saw in our trading example, pattern matching works **really
great** with Swift\'s `enums`. That\'s because `enum cases` are like
sealed, immutable, destructable structs. Much like with `tuples`, you
can unwrap the contents of an individual case right in the match and
only extract the information you need [^2].

Imagine you\'re writing a game in a functional style and you have a
couple of entities that you need to define. You could use `structs` but
as your entities will have very little state, you feel that that\'s a
bit of an overkill.

``` Swift
enum Entities {
    case Soldier(x: Int, y: Int)
    case Tank(x: Int, y: Int)
    case Player(x: Int, y: Int)
}
```

Now you need to implement the drawing loop. Here, we only need the X and
Y position:

``` Swift
for e in entities() {
    switch e {
    case let .Soldier(x, y):
      drawImage("soldier.png", x, y)
    case let .Tank(x, y):
      drawImage("tank.png", x, y)
    case let .Player(x, y):
      drawImage("player.png", x, y)
    }
}
```

## 6. Type-Casting Patterns

As the name already implies, this pattern casts or matches types. It has
two different keywords:

-   `is` **type**: Matches the runtime type (or a subclass of it)
    against the right hand side. This performs a type cast but
    disregards the returned type. So your `case` block won\'t know about
    the matched type.
-   pattern `as` **type**: Performs the same match as the `is` pattern
    but for a successful match casts the type into the pattern specified
    on the left hand side.

Here is an example of the two.

``` Swift
let a: Any = 5 
switch a {
  // this fails because a is still anyobject
  // error: binary operator '+' cannot be applied to operands of type 'Any' and 'Int'
  case is Int: print (a + 1)
  // This works and returns '6'
  case let n as Int: print (n + 1)
  default: ()
}
```

Note that there is no `pattern` before the `is`. It matches directly
against `a`.

## 7. Expression Pattern

The expression pattern is very powerful. It matches the `switch` value
against an expression implementing the `~=` operator. There\'re default
implementations for this operator, for example for ranges, so that you
can do:

``` Swift
switch 5 {
 case 0..10: print("In range 0-10")
}
```

However, the much more interesting possibility is overloading the
operator yourself in order to add matchability to your custom types.
Let\'s say that you decided to rewrite the soldier game we wrote earlier
and you want to use structs after all.

``` Swift
struct Soldier {
  let hp: Int
  let x: Int
  let y: Int
}
```

Now you\'d like to easily match against all entities with a health of
**0**. We can simply implement the `~=` operators as follows.

``` Swift
func ~= (pattern: Int, value: Soldier) -> Bool {
    return pattern == value.hp
}
```

Now we can match against an entity:

``` Swift
let soldier = Soldier(hp: 99, x: 10, y: 10)
switch soldier {
   case 0: print("dead soldier")
   default: ()
}
```

Sadly, full matching with tuples does not seem to work. If you implement
the code below, there\'ll be a type checker error.

``` Swift
func ~= (pattern: (hp: Int, x: Int, y: Int), value: Soldier) -> Bool {
   let (hp, x, y) = pattern
   return hp == value.hp && x == value.x && y == value.y
}
```

One possible way of implementing something akin to the above is by
adding a `unapply` method to your `struct` and then matching against
that:

``` Swift

extension Soldier {
   func unapply() -> (Int, Int, Int) {
      return (self.hp, self.x, self.y)
   }
}

func ~= (p: (Int, Int, Int), t: (Int, Int, Int)) -> Bool {
   return p.0 == t.0 && p.1 == t.1 && p.2 == t.2 
}

let soldier = Soldier(hp: 99, x: 10, y: 10)
print(soldier.unapply() ~= (99, 10, 10))

```

But this is rather cumbersome and defeats the purpose of a lot of the
magic behind pattern matching.

In an earlier version of this post, I wrote that `~=` doesn\'t work with
protocols, but I was wrong. I remember that I tried it in a Playground,
and it didn\'t work. However, this example ([as kindly provided by
latrodectus on
reddit](https://www.reddit.com/r/swift/comments/3hq6id/match_me_if_you_can_swift_pattern_matching_in/cub187r))
does work fine:

``` Swift
protocol Entity {
    var value: Int {get}
}

struct Tank: Entity {
    var value: Int
    init(_ value: Int) { self.value = value }
}

struct Peasant: Entity {
    var value: Int
    init(_ value: Int) { self.value = value }
}

func ~=(pattern: Entity, x: Entity) -> Bool {
    return pattern.value == x.value
}

switch Tank(42) {
    case Peasant(42): print("Matched") // Does match
    default: ()
}
```

There\'s a lot of things you can do with `Expression Patterns`. For a
much more detailed explanation of Expression Patterns, [have a look at
this terrific blog post by Austin
Zheng](http://austinzheng.com/2014/12/17/custom-pattern-matching/).

This completes list of possible switch patterns. Before we move on,
there\'s one final thing to discuss.

## Fallthrough, Break, and Labels

The following is not directly related to pattern matching but only
affects the `switch` keyword, so I\'ll keep it brief. By default, and
unlike C/C++/Objective-C, `switch` `cases` do not fall through into the
next case which is why in Swift, you don\'t need to write `break` for
every case. You can opt into traditional fallthrough behaviour with the
`fallthrough` keyword.

``` Swift
switch 5 {
   case 5:
    print("Is 5")
    fallthrough
   default:
    print("Is a number")
}
// Will print: "Is 5" "Is a number"
```

Alternatively, you can use `break` to break out of a switch statement
early. Why would you do that if there\'s no default fallthrough? For
example if you can only realize within the `case` that a certain
requirement is not met and you can\'t execute the `case` any further:

``` Swift
let userType = "system"
let userID = 10
switch (userType, userID)  {
   case ("system", _):
     guard let userData = getSystemUser(userID) else { break }
     print("user info: \(userData)")
     insertIntoRemoteDB(userData)
   default: ()
}
... more code that needs to be executed
```

Here, we don\'t want to call `insertIntoRemoteData` when the result from
`getSystemUser` is `nil`. Of course, you could just use an `if let`
here, but if multiple of those cases come together, you quickly end up
with a bunch of horrifyingly ugly nested `if lets`.

But what if you execute your switch in a `while` loop and you want to
break out of the loop, not the `switch`? For those cases, Swift allows
you to define `labels` to `break` or `continue` to:

``` Swift
gameLoop: while true {
  switch state() {
     case .Waiting: continue gameLoop
     case .Done: calculateNextState()
     case .GameOver: break gameLoop
  }
}
```

We\'ve discussed the syntax and implementation details of `switch` and
pattern matching. Now, let us have a look at some interesting (more or
less) real world examples.

# Real World Examples

## Optionals

[There\'re many ways to unwrap
optionals,](http://appventure.me/2014/06/13/swift-optionals-made-simple/)
and pattern matching is one of them. You\'ve probably used that quite
frequently by now, nevertheless, here\'s a short example:

``` Swift
var result: String? = secretMethod()
switch result {
case .None:
    println("is nothing")
case let a:
    println("\(a) is a value")
}
```

With Swift 2.0, this becomes even easier:

``` Swift
var result: String? = secretMethod()
switch result {
case nil:
    print("is nothing")
case let a?:
    print("\(a) is a value")
}
```

As you can see, `result` could be a string, but it could also be `nil`.
It\'s an `optional`. By switching on result, we can figure out whether
it is `.None` or whether it is an actual value. Even more, if it is a
value, we can also bind this value to variable right away. In this case
`a`. What\'s beautiful here, is the clearly visible distinction between
the two states, that the variable `result` can be in.

## Type Matches

Given Swift\'s strong type system, there\'s usually no need for runtime
type checks like it more often happens in Objective-C. However, when you
interact with legacy Objective-C code [(which hasn\'t been updated to
reflect simple generics
yet)](https://netguru.co/blog/objective-c-generics), then you often end
up with code that needs to check for types. Imagine getting an array of
NSStrings and NSNumbers:

``` Swift
let u = NSArray(array: [NSString(string: "String1"), NSNumber(int: 20), NSNumber(int: 40)])
```

When you go through this NSArray, you never know what kind of type you
get. However, `switch` statements allow you to easily test for types
here:

``` Swift
for x in u {
    switch x {
    case _ as NSString:
        print("string")
    case _ as NSNumber:
        print("number")
    default:
        print("Unknown types")
    }
}
```

## Applying ranges for grading

So you\'re writing the grading iOS app for your local Highschool. The
teachers want to enter a number value from 0 to 100 and receive the
grade character for it (A - F). Pattern Matching to the rescue:

``` Swift
let aGrade = 84

switch aGrade {
case 90...100: print("A")
case 80...90: print("B")
case 70...80: print("C")
case 60...70: print("D")
case 0...60: print("F")
default:
    print("Incorrect Grade")
}
```

## Word Frequencies

We have a sequence of pairs, each representing a word and its frequency
in some text. Our goal is to filter out those pairs whose frequency is
below or above a certain threshold, and then only return the remaining
words, without their respective frequencies.

Here\'re our words:

``` Swift
let wordFreqs = [("k", 5), ("a", 7), ("b", 3)]
```

A simple solution would be to model this with `map` and `filter`:

``` Swift
let res = wordFreqs.filter({ (e) -> Bool in
    if e.1 > 3 {
        return true
    } else {
        return false
    }
}).map { $0.0 }
print(res)
```

However, with `flatmap` a map that only returns the non-nil elements, we
can improve a lot upon this solution. First and foremost, we can get rid
of the `e.1` and instead have proper destructuring by utilizing (you
guessed it) tuples. And then, we only need one call `flatmap` instead of
`filter` and then `map` which adds unnecessary performance overhead.

``` Swift
let res = wordFreqs.flatMap { (e) -> String? in
    switch e {
    case let (s, t) where t > 3: return s
    default: return nil
    }
}
print(res)
```

## Directory Traversion

Imagine you want to traverse a file hierachy and find:

-   all \"psd\" files from customer1 and customer2
-   all \"blend\" files from customer2
-   all \"jpeg\" files from all customers.

``` Swift
guard let enumerator = NSFileManager.defaultManager().enumeratorAtPath("/customers/2014/")
else { return }

for url in enumerator {
    switch (url.pathComponents, url.pathExtension) {

    // psd files from customer1, customer2
    case (let f, "psd") 
            where f.contains("customer1") 
            || f.contains("customer2"): print(url)

    // blend files from customer2
    case (let f, "blend") where f.contains("customer2"): print(url)

    // all jpg files
    case (_, "jpg"): print(url)

    default: ()
    }
}
```

Note that `contains` stops at the first match and doesn\'t traverse the
complete path. Again, pattern matching lead to very succinct and
readable code.

## Fibonacci

Also, see how beautiful an implementation of the fibonacci algorithm
looks with pattern matching [^3]

``` Swift
func fibonacci(i: Int) -> Int {
    switch(i) {
    case let n where n <= 0: return 0
    case 0, 1: return 1
    case let n: return fibonacci(n - 1) + fibonacci(n - 2)
    }
}

print(fibonacci(8))
```

Of course, this will kill your stack with big numbers.

## Legacy API and Value Extractions

Oftentimes, when you get data from an external source, like a library,
or an API, it is not only good practice but usually even required that
you check the data for consistency before interpreting it. You need to
make sure that all keys exists or that the data is of the correct type,
or the arrays have the required length. Not doing so can lead from buggy
behaviour (missing key) to crash of the app (indexing non-existent array
items). The classic way to do this is by nesting `if` statements.

Let\'s imagine an API that returns a user. However, there\'re two types
of users: System users - like the administrator, or the postmaster - and
local users - like \"John B\", \"Bill Gates\", etc. Due to the way the
system was designed and grew, there\'re a couple of nuisances that API
consumers have to deal with:

-   `system` and `local` users come via the same API call.
-   the `department` key may not exist, since early versions of the db
    did not have that field and early employees never had to fill it
    out.
-   the `name` array contains either 4 items (username, middlename,
    lastname, firstname) or 2 items (full name, username) depending on
    when the user was created.
-   the `age` is an Integer with the age of the user

Our system needs to create user accounts for all system users from this
API with only the following information: username, department. We only
need users born before 1980. If no department is given, \"Corp\" is
assumed.

``` Swift
func legacyAPI(id: Int) -> [String: AnyObject] {
    return ["type": "system", "department": "Dark Arts", "age": 57, 
           "name": ["voldemort", "Tom", "Marvolo", "Riddle"]] 
}
```

Given these constraints, let\'s develop a pattern match for it:

``` Swift
let item = legacyAPI(4)
switch (item["type"], item["department"], item["age"], item["name"]) {
   case let (sys as String, dep as String, age as Int, name as [String]) where 
      age < 1980 &&
      sys == "system":
     createSystemUser(name.count == 2 ? name.last! : name.first!, dep: dep ?? "Corp")
  default:()
}

// returns ("voldemort", "Dark Arts")
```

Note that this code makes one dangerous assumption, which is that if the
name array does not have 2 items, it **must** have 4 items. If that case
doesn\'t hold, and we get a zero item name array, this would crash.

Other than that, it is a nice example of how pattern matching even with
just one case can help you write cleaner code and simplify value
extractions.

Also, see how we\'re writing `let` at the beginning right after the
case, and don\'t have to repeat it for each assignment within the case.

# Patterns with other Keywords

The Swift documentation points out, that not all patterns can be used
with the `if`, `for` or the `guard` statement. However, the docs seem to
be outdated. All 7 patterns work for all three keywords.

For those interested, I compiled an example Gist that has an example for
each pattern for each keyword.

[You can see the example patterns
here.](https://gist.github.com/terhechte/6eaeb90276bbfcd1ea41)

As a shorter example, see the **Value Binding**, **Tuple**, and **Type
Casting** pattern used for all three keywords in one example:

``` Swift
// This is just a collection of keywords that compiles. This code makes no sense
func valueTupleType(a: (Int, Any)) -> Bool {
    // guard case Example
    guard case let (x, _ as String) = a else { return false}
    print(x)

    // for case example
    for case let (a, _ as String) in [a] {
        print(a)
    }

    // if case example
    if case let (x, _ as String) = a {
       print("if", x)
    }

    // switch case example
    switch a {
    case let (a, _ as String):
        print(a)
        return true
    default: return false
    }
}
let u: Any = "a"
let b: Any = 5
print(valueTupleType((5, u)))
print(valueTupleType((5, b)))
// 5, 5, "if 5", 5, true, false
```

With this in mind, we will have a short look at each of those keywords
in detail.

# Using **for case**

With Swift 2.0, pattern matching has become even more important in the
language as the `switch` capabilities have been extended to other
keywords as well. For example, let\'s write a simple array function
which only returns the non-nil elements

``` Swift
func nonnil<T>(array: [T?]) -> [T] {
   var result: [T] = []
   for case let x? in array {
      result.append(x)
   }
   return result
}

print(nonnil(["a", nil, "b", "c", nil]))
```

The `case` keyword can be used in for loops just like in `switch` cases.
Here\'s another example. Remember the game we talked about earlier?
Well, after the first refactoring, our entity system now looks like
this:

``` Swift
enum Entity {
    enum EntityType {
        case Soldier
        case Player
    }
    case Entry(type: EntityType, x: Int, y: Int, hp: Int)
}
```

Fancy, this allows us to draw all items with even less code:

``` Swift
for case let Entity.Entry(t, x, y, _) in gameEntities()
where x > 0 && y > 0 {
    drawEntity(t, x, y)
}
```

Our one line unwraps all the necessary properties, makes sure we\'re not
drawing beyond 0, and finally calls the render call (`drawEntity`).

In order to see if the player won the game, we want to know if there is
at least one Soldier with health \> 0

``` Swift
func gameOver() -> Bool {
    for case Entity.Entry(.Soldier, _, _, let hp) in gameEntities() 
    where hp > 0 {return false}
    return true
}
print(gameOver())
```

What\'s nice is that the `Soldier` match is part of the for query. This
feels a bit like `SQL` and less like imperative loop programming. Also,
this makes our intent clearer to the compiler, opening up the
possibilities for dispatch enhancements down the road. Another nice
touch is that we don\'t have to spell out `Entity.EntityType.Soldier`.
Swift understands our intent even if we only write `.Soldier` as above.

# Using **guard case**

Another keyword which supports patterns is the newly introduced `guard`
keyword. You know how it allows you to bind `optionals` into the local
scope much like `if let` only without nesting things:

``` Swift
func example(a: String?) {
    guard let a = a else { return }
    print(a)
}
example("yes")
```

`guard let case` allows you to do something similar with the power that
pattern matching introduces. Let\'s have a look at our soldiers again.
We want to calculate the required HP until our player has full health
again. Soldiers can\'t regain HP, so we should always return 0 for a
soldier entity.

``` Swift
let MAX_HP = 100

func healthHP(entity: Entity) -> Int {
    guard case let Entity.Entry(.Player, _, _, hp) = entity 
    where hp < MAX_HP 
    else { return 0 }
    return MAX_HP - hp
}

print("Soldier", healthHP(Entity.Entry(type: .Soldier, x: 10, y: 10, hp: 79)))
print("Player", healthHP(Entity.Entry(type: .Player, x: 10, y: 10, hp: 57)))

// Prints:
"Soldier 0"
"Player 43"

```

This is a beautiful example of the culmination of the various mechanisms
we\'ve discussed so far.

-   It is very clear, there is no nesting involved
-   Logic and initialization of state are handled at the top of the
    `func` which improves readability
-   Very terse.

This can also be very successfully combined with `switch` and `for` to
wrap complex logical constructs into an easy to read format. Of course,
that won\'t make the logic any easier to understand, but at least it
will be provided in a much saner package. Especially if you use `enums`.

# Using **if case**

`if case` can be used as the opposite of `guard case`. It is a great way
to unwrap and match data within a branch. In line with our previous
`guard` example. Obviously, we need an move function. Something that
allows us to say that an entity moved in a direction. Since our entities
are `enums`, we need to return an updated entity.

``` Swift
func move(entity: Entity, xd: Int, yd: Int) -> Entity {
    if case Entity.Entry(let t, let x, let y, let hp) = entity
    where (x + xd) < 1000 &&
        (y + yd) < 1000 {
    return Entity.Entry(type: t, x: (x + xd), y: (y + yd), hp: hp)
    }
    return entity
}
print(move(Entity.Entry(type: .Soldier, x: 10, y: 10, hp: 79), xd: 30, yd: 500))
// prints: Entry(main.Entity.EntityType.Soldier, 40, 510, 79)
```

# Limitations

Some limitations were already mentioned in the text, such as the issues
regarding `Expression Patterns`, which seem to not match against
`tuples` (as would be really convenient). In Scala or Clojure, pattern
matching can also work against collections, so you could match head,
tail, parts, etc. [^4] {\
case \[\_, 2, \_, 3\]:\
}\] This doesn\'t work in Swift ([although Austin Zheng kinda
implemented this in the blog post I linked
above](http://austinzheng.com/2014/12/17/custom-pattern-matching/)).

Another thing which doesn\'t work (wich, again, Scala does just fine) is
destructuring against classes or structs. Scala allows us to define an
`unapply` method which does basically the opposite of `init`.
Implementing this method, then, allows the type checker to match against
classes. In Swift, this could look as follows:

``` Swift
struct Imaginary {
   let x: Int
   let y: Int
   func unapply() -> (Int, Int) {
     // implementing this method would then in theory provide all the details needed to destructure the vars
     return (self.x, self.y)
   }
}
// this, then, would unapply automatically and then match
guard case let Imaginary(x, y) = anImaginaryObject else { break }
```

# Changes

****08/21/2015**** Incorporated [helpful feedback from foBrowsing on
Reddit](https://www.reddit.com/r/swift/comments/3hq6id/match_me_if_you_can_swift_pattern_matching_in/)

-   Added `guard case let`
-   Added simplified syntax for let (i.e. `let (x, y)` instead of
    `(let x, let y)`

****08/22/2015**** [Apparently I didn\'t test some things properly
enough.](https://www.reddit.com/r/swift/comments/3hq6id/match_me_if_you_can_swift_pattern_matching_in/)
Some of the limitations I listed do actually work, as another helpful
Reddit commenter (latrodectus) pointed out.

-   All patterns work for all three keywords. Changed that, and added a
    Gist with examples
-   The limitations regarding protocols and the expression pattern were
    invalid. This works fine, too.
-   Added \"Pattern Availability\" section

****08/24/2015****

-   Added `if case` examples, renamed some sections.
-   Fixed typos in the text. In particular, I accidentally wrote that
    `_` does not match `nil`. That\'s of course not true, `_` matches
    everything. (thanks to [obecker](https://github.com/obecker))

****09/18/2015****

-   Added link to Japanese Translation

[^1]: Think of it like the `*` wildcard you use in the shell

[^2]: I\'m not sure whether the compiler optimizes for this, but
    theoretically, it should be able to calculate the correct position
    of the requested data and inline the address ignoring the other
    parts of the enum case

[^3]: of course, no match for a Haskell implementation:\
    fib 0 = 0\
    fib 1 = 1\
    fib n = fib (n-1) + fib (n-2)

[^4]: I.e. switch \[1, 2, 4, 3
