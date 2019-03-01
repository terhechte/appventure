[frontMatter]
title = "Containing Enums"
tags = []
created = "2019-03-01 16:29:51"
description = ""
published = false

---

# Containing Enums

In a similar vein, you can also embed enums in `structs` or `classes`.
Continuing with our previous example:

``` Swift
struct Character {
   enum CharacterType {
    case Thief
    case Warrior
    case Knight
  }
  enum Weapon {
    case Bow
    case Sword
    case Lance
    case Dagger
  }
  let type: CharacterType
  let weapon: Weapon
}

let warrior = Character(type: .Warrior, weapon: .Sword)
```

This, again, helps in keeping related information together.
