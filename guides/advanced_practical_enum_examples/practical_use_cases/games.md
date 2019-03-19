[frontMatter]
title = "Games"
tags = []
created = "2019-03-01 16:31:41"
description = ""
published = true

[meta]
swift_version = "5.0"
---

# Games

Enums are a great use case for games, where many entities on screen
belong to a specific family of items (enemies, obstacles, textures,
...). In comparison to native iOS or Mac apps, games oftentimes are a
tabula rasa. Meaning you invent a new world with new relationships and
new kinds of objects, whereas on iOS or OSX you\'re using a well-defined
world of `UIButtons`, `UITableViews`, `UITableViewCells` or `NSStackView`.

What\'s more, since Enums can conform to protocols, you can utilize
protocol extensions and protocol based programming to add functionality
to the various enums that you defined for your game. Here\'s a short
example that tries to display such a hierarchy:

``` Swift
enum FlyingBeast { case dragon, hippogriff, gargoyle }
enum Horde { case ork, troll }
enum Player { case mage, warrior, barbarian }
enum NPC { case vendor, blacksmith }
enum Element { case tree, fence, stone }

protocol Hurtable {}
protocol Killable {}
protocol Flying {}
protocol Attacking {}
protocol Obstacle {}

extension FlyingBeast: Hurtable, Killable, Flying, Attacking {}
extension Horde: Hurtable, Killable, Attacking {}
extension Player: Hurtable, Obstacle {}
extension NPC: Hurtable {}
extension Element: Obstacle {}
```
