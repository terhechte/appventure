[frontMatter]
title = "Tuples for Pattern Matching"
tags = ["tuples", "pattern matching"]
created = "2019-03-01 17:35:30"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Tuples for Pattern Matching

Pattern matching oftentimes feels like the strongest use case for
tuples. Swift\'s `switch` statement offers a really powerful yet easy
way to define complex conditionals without cluttering up the source
code. You can then match for the type, existence, and value of multiple
variables in one statement.

We wrote a game where both players have to take a quiz. After each question we evaluate
who won or lost. There're four states: 

- Player 1 is correct
- Player 2 is correct
- Both were correct
- Both were wrong

We can model this logic very nicely with a `switch` statement such as the following:

``` Swift
let player1 = true
let player2 = false
switch (player1, player2) {
case (true, false): print("Player 1 won")
case (false, true): print("Player 2 won")
case (true, true): print("Draw, both won")
case (false, false): print("Draw, both lost")
}
```

Here, we create a tuple `(player1, player2)` and then match each of
the possible cases.

Much more complex matchings are also possible. Below, we will match over
a tuple that has the type `(Int, String?, Any)`.

``` Swift
// Contrived example
// These would be return values from various functions.
let age: Int = 23
let job: String? = "Operator"
let payload: Any = ["cars": 1]
```

In the code above, we want to find the persons younger than 30 with a
job and a Dictionary payload. Imagine the payload as something from the
Objective-C world, it could be a Dictionary or an Array or a Number,
weakly typed code that somebody else wrote years ago, and you have to interact with
it now.

``` Swift
switch (age, job, payload) {
case (let age, _?, _ as Dictionary<AnyHashable, Any>) where age < 30:
    print(age)
default:
    break
}
```

By constructing the switch argument as a tuple `(age, job, payload)` we
can query for specific or nonspecific attributes of all tuple elements
at once. This allows for elaborately constrained conditionals.


