[frontMatter]
title = "Expression Pattern"
tags = ["pattern matching", "switch", "equatable", "~="]
created = "2019-02-15 20:40:47"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Expression Pattern

The expression pattern is very powerful. It matches the `switch` value
against an expression implementing the `~=` operator. There\'re default
implementations for this operator, for example for ranges, so that you
can do:

``` Swift
switch 5 {
 case 0..10: print("In range 0-10")
 default: print("In another range")
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

Now we can match against an entity. In this example, only soldiers that
have a `hp` of `0` would be matched (thus, we print `dead soldier`),
because we're commparing the `value.hp` to the `switch` pattern in our
`~=` implementation above.

``` Swift
let soldier = Soldier(hp: 99, x: 10, y: 10)
switch soldier {
   case 0: print("dead soldier")
   default: ()
}
```

What if you'd like to not just compare the `hp` but also the `x` and the `y`? You
can just implement `pattern` with a [tuple](apv::tuple):

``` Swift
func ~= (pattern: (hp: Int, x: Int, y: Int), value: Soldier) -> Bool {
    let (hp, x, y) = pattern
    return hp == value.hp && x == value.x && y == value.y
}


let soldier = Soldier(hp: 99, x: 10, y: 10)
switch soldier {
  case (50, 10, 10): print("health 50 at pos 10/10")
  default: ()
}
```

You can even match structs against structs. However, this only works if your
structs are `Equatable`. Swift can implement this automatically, as long as
you tell it to by conforming to the protocol. So lets first extend our `Soldier`
struct to conform to `Equatable`:

``` Swift
struct Soldier: Equatable {
    let hp: Int
    let x: Int
    let y: Int
}
```

Now, we can add a new match implementation. Since both soldiers are equatable `value types`, we can actually just directly compare them. If they both have the same values for their three properties (hp, x, y), then they are considered equal:

``` Swift
func ~= (pattern: Soldier, value: Soldier) -> Bool {
    return pattern == value
}

let soldier = Soldier(hp: 50, x: 10, y: 10)
switch soldier {
  case Soldier(hp: 50, x: 10, y: 10): print("The same")
  default: ()
}
```

The left side of the `~=` operator (the `pattern` argument) can be anything. So 
it can even be a `protocol`:

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

This completes list of possible switch patterns. Our next topic is 
flow control in `switch` statements.
