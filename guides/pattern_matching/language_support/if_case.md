[frontMatter]
title = "If Case"
tags = ["pattern matching", "switch", "if case"]
created = "2019-02-15 20:40:47"
description = ""
published = true

[meta]
swift_version = "5.1"
---

# Using **if case**

`if case` can be used as the opposite of `guard case`. It is a great way
to unwrap and match data within a branch. In line with our previous
`guard` example. Obviously, we need an move function. Something that
allows us to say that an entity moved in a direction. Since our entities
are `enums`, we need to return an updated entity.

``` Swift
func move(entity: Entity, xd: Int, yd: Int) -> Entity {
    if case Entity.Entry(let t, let x, let y, let hp) = entity
    where (x + xd) < 1000 &&
        (y + yd) < 1000 {
    return Entity.Entry(type: t, x: (x + xd), y: (y + yd), hp: hp)
    }
    return entity
}
print(move(Entity.Entry(type: .soldier, x: 10, y: 10, hp: 79), xd: 30, yd: 500))
// prints: Entry(main.Entity.EntityType.soldier, 40, 510, 79)
```
