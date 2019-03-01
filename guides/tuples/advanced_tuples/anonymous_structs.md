[frontMatter]
title = "Anonymous Structs"
tags = []
created = "2019-03-01 17:35:30"
description = ""
published = false

---

# Anonymous Structs

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
