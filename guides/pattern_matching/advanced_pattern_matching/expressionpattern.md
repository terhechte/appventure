[frontMatter]
title = "Expression Pattern"
tags = []
created = "2019-02-15 20:40:47"
description = ""
published = false

---

# Expression Pattern

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
