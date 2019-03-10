[frontMatter]
description = "With Swift, Apple introduced several new programming languages features to iOS and Mac developers. One of them are Optionals. This is a simple introduction into Optionals that glosses over details to make it more approachable."
title = "Swift optionals made simple"
created = "2014-06-13"
published = true
keywords = ["lisp", "swift", "optional", "scala", "simple", "optionals", "switch", "chaining", "feature"]
slug = "2014-06-13-swift-optionals-made-simple.html"
tags = ["swift", "ios", "cocoa"]
---

**Note**: This blog post has been edited to be compatible with Swift 2.0
b4

With Swift, Apple introduced several new programming languages features
to iOS and Mac developers. One of them are `Optionals`. I\'ve used
Optionals before in Scala and I found them a deeply satisfying concept
that made me feel much better about the code I wrote.

I\'m trying a simple explanation that glosses over details to make it
more approachable.

### Life without Optionals

In Objective-C, each method that returns a NSObject[^1] subclass can
also choose to return `Nil` instead. Quick Example, imagine we want to
split an array in two equally sized partitions.

``` Objective-C
@implementation Example
+ (NSArray*) partitionArray:(NSArray*)p {
    // can't partition for non-power-2 array-sizes
    if (p.count % 2 != 0) return nil;
    // return an array with the two partitions
    return @[[p subarrayWithRange: NSMakeRange(0, p.count/2 - 1)]
             [p subarrayWithRange: NSMakeRange(p.count/2, p.count/2 - 1)]]
}
@end
```

If we can\'t partition the array, what are we to do, we can only return
nil.

Now in Swift, we can\'t do such a thing. If we tell the Swift compiler
that we\'re returning an NSArray from a function, we **have** to return
an NSArray. Everything else is a compile error. So what you do in Swift
instead, if you were to write a function `partitionArray` is to tell the
compiler that the function **may** return an NSArray, but that it
**may** also return nil. That really depends upon the input values. The
return value of your function may be NSArray or nil, it is optional.

``` Swift
// Wrong
func partitionArray(p: NSArray) -> NSArray {
    return nil // Compile error
}

// Right
func partitionArray(p: NSArray) -> NSArray? {
    // Works fine, we return Optional.None
    if p.count % 2 != 0 {
        return nil
    }
    // partition
    return NSArray(array: [p[0..p.count/2-1], p[p.count/2..p.count-1]])
}
```

By extending the `NSArray` type with a `?` we basically told the
compiler that the partitionArray function my either return an NSArray,
or not. The `?` at the end of a type declares it as an Optional type.

### Why is this useful?

Let\'s go back to our initial Objective-C example and see it in use.

``` Objective-C
NSArray *data = someWebServiceMagic();
NSArray *storePartitions = [Example partitionArray: data];
// move user backups to locations
[user moveData:storePartitions[0][0]];
```

This works great, you test it in development, production, all is fine.
Until one day your magic web service returns a non-power-of-two array.
In that case, `storePartitions` will be nil and you will probably move
all your users data to /dev/null or wherever.

The issue, of course, is that you never expected the value of
`partitionsArray` to ever become nil. Now, maybe you\'re the cautious
kind of guy and you always check whether external data is nil or null.
Even then, you just may have had a hectic day and may have forgotten one
of those.

With Optionals in Swift, this can\'t happen to you anymore. Whenever a
function **may** return a nil value, the compiler will force you to
check for it. You can\'t just use the value right away. So how does that
work?

### Checking for Optionals

Swift introduces two ways of unwrapping a value. The first one is the
forced unwrap. You do it by adding a `!` to the end of the variable.
This works great, but it means that the optional has to have a value. If
you try a forced unwrap on an empty optional (i.e. nil) it will cause a
runtime error. (Ignore the `as NSArray`, it simply tells the compiler to
convert the native Array to an NSArray)

``` Swift
partitionArray([1, 2, 3, 4] as NSArray?)![0] // will work fine
partitionArray([1, 2, 3] as NSArray?)![0] // will crash
```

So you should only use this if you\'re really sure that your method,
function, or variable will unwrap into a value.

The other way is to unwrap into a let expression. That way, you define a
block of code that will only be executed if the Optional contains a
value.

``` Swift
if let p = partitionArray([1, 2, 3, 4] as NSArray?) {
    // this code will be called
}

if let p = partitionArray([1, 2, 3] as NSArray?) {
    // this code won't be called
}

```

This works totally fine in all cases. Be it nil or not nil. The inner
scope will only be reached if the if let successfully binds the contents
of value (the actual NSArray) to the constant p.

### Inverse Comparison

Oftentimes, however, you actually just want to do the opposite.

``` Swift
if not let p = partitionArray([1, 2, 3] as NSArray?) {
    // print an error
   return
}
```

This, though, does not work. The let expression can\'t be negated.
Unwrapping it into a variable with ! also doesn\'t work, because if it
is indeed nil, it will crash. So what to do? Thankfully, this case can
be identified with a simple equality comparison:

``` Swift
if p == nil {
    return
}
```

Now you may say, that that looks an awful lot like how you dealt with
nil in Objective-C, and that is the case. Only that this time you\'ll
never forget when to add this check as the compiler will tell you for
sure.

Another advantage is that optionals work for every type in Swift, not
just objects, so you can also use them for Int, Bool, even Closures:

    func opt1() -> Bool? {
       return nil
    }
    func opt2() -> Int? {
       return nil
    }

### Additional Tips and Tricks

1.  Optionals for unknown Methods

    Optionals also work for unknown selectors. Say you want to call a
    method on a Objective-C object, but you didn\'t know whether it
    existed or not, you can do that the following way:

    ``` Swift
    // 1.
    object.secredMethod?(param)
    // 2.
    if let obj = object.secretFunction(param) {
       // do things with obj
    }
    ```

2.  Optionals in Pattern Matching

    The sophisticated Pattern Matching in Swift\'s `switch` construct is
    also a good alternative to unwrap Optionals:

    ``` Swift
    var result: String? = secretFunction()
    switch result {
    case .None:
        print("is nothing")
    case let a:
        print("is a value")
    }
    ```

    With Swift 2.0, this can also be expressed more cleanly:

    ``` Swift
    var result: String? = secretFunction()
    switch result {
    case nil:
        print("is nothing")
    case let a?:
        print("is a value")
    }
    ```

    While this may seem to offer little benefit, the advanced pattern
    matching syntax in Swift allow you to define far more detailed cases
    that test for much more than just nil or not nil.

    ``` Swift
    // A number of very stub methods 
    func secretFunction1() -> Int? {return 0}
    func secretFunction2() -> [String] {return ["a", "b"]}
    func secretFunction3() -> Bool {return true}

    switch (secretFunction1(), secretFunction2(), secretFunction3()) {
    case (nil, let col, true):
        print("case1")
    case (let num?, let col, true) where num > 1:
        print("case2")
    default: ()
        print ("default")
    }
    ```

    Try to figure out what the above will finally print. We\'re matching
    for the return results of three function calls at once. This would
    quickly become a cumbersome list of `if` and `else` blocks if it
    weren\'t for `Optionals` and `switch`.

3.  Objective-C interop

    As already explained above, Objective-C always offers you to use
    `nil` instead of an actual object. This, of course, means that
    **every** Cocoa or UIKit method that returns a NSObject subclass
    will need to be typed as optional in Swift. This means that whenever
    you interact with UIKit or Cocoa libraries, you will need to unwrap
    your values:

    ``` Swift
    if let u = c.componentsSeperatedByString("a") {
    }
    if let u = c.firstItem() {
    }
    ```

4.  NSDictionary Interop

    This is also necessary for NSDictionary access:

    ``` Swift
    let u: NSDictionary = magicMethod()
    // image u as having the following structure
    // Objc Syntax: @{@"a-key": @[@1, @2, @3]}
    // Swift Syntax: ["a-key": [1, 2, 3]]
    u["a-key"].count // u["a-key"] returns an optional, this fails.
    u["a-key"]!.count // this works fine 
    // *Until* a-key does not exist in your NSDictionary, then it will crash.
    // So the better way is
    if let ux = u["a-key"] {
    }
    ```

    However, it is much more important here to use the `let ux = ...`
    syntax, until you\'re really, really sure, that the NSDictionary
    **will** contain the required key. In general, if your code contains
    `!` outside of `IBOutlet` bindings, there may be a better way to do
    this. In this case, Swift\'s combined `let` statements.

    ``` Swift
    let example = ["a": ["b": ["c": 1]]]
    if let a = example["a"],
        b = a["b"],
        c = b["c"] where c > 0 {
            print(c)
    }
    ```

    Since `let` can access previous `let`\'s contents, we can access `b`
    from `a` etc. We can also add a where block for any of the let-bound
    values. This makes it particularly easy to express the desired
    requirements for accessing a value.

5.  Optional Chaining

    The alternative to the list of `let` statements from the previous
    section would be `optional chaining`. Here, Swift will take the
    return value of an optional operation, and if it is non-nil, will
    process the next operation on the value, and return the optional
    result of this again.

    By adding `?` in between each call / access, Swift will
    automatically unwrap if there is a value, or stop the chain as soon
    as any one evaluates to nil. For our previous example, that would
    look like the following:

    ``` Swift
    example["a"]?["b"]?["c"]
    ```

6.  Mapping

    Consider the following code:

    ``` Swift
    func example() -> Int? {return 10}
    if let value = example() {
        storeInDatabase(value * 2)
    }
    ```

    If we break down the logic, what we\'re really trying to achieve,
    were it not for optionals, is the following:

    ``` Swift
    storeInDatabase(example() * 10)
    ```

    Optionals are still very useful here, as they prevent us from the
    danger of multiplying nil with 10 and trying to store that in the
    database. But still, we have to admit that the optionals code looks
    more convoluted. As you can imagine, there\'s a solution to this, of
    course.

    Optionals offer an implementation of the `map` function which will
    call the `.Some` value of an optional with a supplied closure iff
    the optional has a value.

    ``` Swift
    // The following will call print with 5, i.e. will print 5
    let px: Int? = 5
    px.map { print($0) }

    // The following won't call print
    let px: Int? = nil
    px.map { print($0) }

    ```

    This lets us rewrite our example from above in terms of `map` as
    follows:

    ``` Swift
    example().map { storeInDatabase($0 * 2) }
    ```

7.  Unwrapping Multiple Dictionary Keys

    **Note**: I\'ve kept the following in since it still explains a nice
    way to match multiple dictionary entries, however the intended use
    case for matching JSON values is better served by using one of the
    modern JSON Swift libraries like SwityJSON or Argo.

    Say you\'re receiving data from a json frontend. The data converts
    to a NSDictionary, and then you want to process it. However, this
    being json and a mystic webservice, you don\'t know for sure if the
    dictionary contains all the keys. So the be really sure, you\'d like
    to test for all keys in the dictionary. It is not immediately clear
    how to do that, but [@_nickmain on
    Twitter](https://twitter.com/_nickmain) (and subsequently [Wes
    Campaigne](http://twitter.com/westacular/status/478018591280070656))
    came up with a really good solution for this. They\'re utilizing the
    switch statement with a tuple to test for multiple entries.

    ``` Swift
    let j2 = ["a": 1, "b": 2, "c": 3]
    switch (j2["a"], j2["b"], j2["c"]) {
    case (let a?, nil, nil):
        print("got \(a)")
    case (let a?, let b?, .None) where b is String:
        print("got \(a), \(b)")
    case (let a?, let b?, let c?):
        print("got \(a), \(b), \(c)")
    default:
        print("got none")
    }
    ```

    This prints \"got none\" because b is not of type string. If the
    dictionary would be `["b": "45"]` then, it would print
    `[got 5, "45"]`. This is a really nice solution, because it allows
    you to test different cases based on the information available in
    the dictionary. What\'s more, you can also use the `where` operator
    to test for advanced properties of your values. I.e. you can test
    whether they\'re of class String, or whether they\'re above a
    certain value (i.e. \> 5).

    If this looks tempting, have a look at my tutorial on using `switch`
    statements in Swift, particularly for people who\'re mostly
    accustomed to the way it works in C / Objective-C and not the much
    more powerful switch statements like in Swift, Scala, Erlang, or
    Clojure\'s core.match.

[^1]: or NSProxy, but you shouldn\'t really do that
