[frontMatter]
title = "Simple Problem Redux"
tags = ["reduce"]
created = "2019-02-20 19:49:10"
description = ""
published = true

[meta]
swift_version = "5.0"
---

We can now go back to our initial count & average problem and try to
solve it with `reduce`.

# InfoFromState, take two

``` Swift

  func infoFromState(state: String, persons: [[String: Any]]) 
      -> (count: Int, age: Float) {

      // The type alias in the function will keep the code cleaner
      typealias Acc = (count: Int, age: Float)

      // reduce into a temporary variable
      let u = persons.reduce((count: 0, age: 0.0)) {
          (ac: Acc, p) -> Acc in

          // Retrive the state and the age
          guard let personState = (p["city"] as? String)?.componentsSeparatedByString(", ").last,
                personAge = p["age"] as? Int

            // make sure the person is from the correct state
            where personState == state

            // if age or state are missing, or personState!=state, leave
            else { return ac }

          // Finally, accumulate the acount and the age
          return (count: ac.count + 1, age: ac.age + Float(personAge))
      }

  // our result is the count and the age divided by count
  return (age: u.age / Float(u.count), count: u.count)
}
print(infoFromState(state: "CA", persons: persons))
// prints: (count: 3, age: 34.3333)
```

As in earlier examples above, we\'re once again using a `tuple` to share
state in the accumulator. Apart from that, the code is easy to
understand.

We also defined a `typealias` **Acc** within the `func` in order to
simplify the type annotations a bit.
