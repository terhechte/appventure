[frontMatter]
title = "For Case"
tags = []
created = "2019-02-15 20:40:47"
description = ""
published = false

---

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
