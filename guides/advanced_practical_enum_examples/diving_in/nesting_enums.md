[frontMatter]
title = "Nesting Enums"
tags = ["enum"]
created = "2019-03-01 16:29:51"
description = ""
published = false

[meta]
swift_version = "5.1"
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
    case bow
    case sword
    case lance
    case dagger
  }
  enum Helmet {
    case wooden
    case iron
    case diamond
  }
  case thief
  case warrior
  case knight
}
```

Now you have a hierachical system to describe the various items that
your character has access to.

``` Swift
let character = Character.thief
let weapon = Character.Weapon.bow
let helmet = Character.Helmet.iron
```

If you add initializers for the nested `enum` types, you can still benefit from not having
to type out the the long description. Imagine a function that calculates how strong a 
character is, based on the character, the weapon, and the helmet:

``` Swift
func strength(of character: Character, 
     with weapon: Character.weapon, 
     and armor: Character.Helmet) {
     return 0
}

// You can still call it like this:
strength(of: .thief, with: .bow, and: .wooden)
```

This is still really clear and easy to understand.

# Containing Enums

In a similar vein, you can also embed enums in `structs` or `classes`.
Continuing with our previous example:

``` Swift
struct Character {
   enum CharacterType {
    case thief
    case warrior
    case knight
  }
  enum Weapon {
    case bow
    case sword
    case lance
    case dagger
  }
  let type: CharacterType
  let weapon: Weapon
}

let warrior = Character(type: .warrior, weapon: .sword)
```

This really helps in keeping related information together.
