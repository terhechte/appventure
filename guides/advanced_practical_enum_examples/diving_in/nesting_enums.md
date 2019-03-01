[frontMatter]
title = "Nesting Enums"
tags = []
created = "2019-03-01 16:29:51"
description = ""
published = false

---

# Nesting Enums

If you have specific sub type requirements, you can also logically nest
enums in an enum. This allows you to contain specific information on
your enum case within the actual enum. Imagine a character in an RPG.
Each character can have a weapon, all characters have access to the same
set of weapons. All other instances in the game do not have access to
those weapons (they\'re trolls, they just have clubs).

``` Swift
enum Character {
  enum Weapon {
    case Bow
    case Sword
    case Lance
    case Dagger
  }
  enum Helmet {
    case Wooden
    case Iron
    case Diamond
  }
  case Thief
  case Warrior
  case Knight
}
```

Now you have a hierachical system to describe the various items that
your character has access to.

``` Swift
let character = Character.Thief
let weapon = Character.Weapon.Bow
let helmet = Character.Helmet.Iron
```
