[frontMatter]
title = "Guard Case"
tags = ["pattern matching", "switch", "guard"]
created = "2019-02-15 20:40:47"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Using **guard case**

Another keyword which supports patterns is the newly introduced `guard`
keyword. You know how it allows you to bind `Optionals` into the local
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
    guard case let Entity.Entry(.player, _, _, hp) = entity 
      where hp < MAX_HP 
        else { return 0 }
    return MAX_HP - hp
}

print("Soldier", healthHP(Entity.Entry(type: .soldier, x: 10, y: 10, hp: 79)))
print("Player", healthHP(Entity.Entry(type: .player, x: 10, y: 10, hp: 57)))

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
