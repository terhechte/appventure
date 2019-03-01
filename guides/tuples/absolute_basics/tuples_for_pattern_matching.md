[frontMatter]
title = "Tuples for Pattern Matching"
tags = []
created = "2019-03-01 17:35:30"
description = ""
published = false

---

# Tuples for Pattern Matching

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
