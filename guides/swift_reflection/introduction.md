[frontMatter]
title = "Introduction"
tags = ["reflection"]
created = "2019-03-01 11:47:01"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Introduction

Even though Swift stresses strong types, compile time safety and static
dispatch, it still offers a Reflection mechanism as part of the standard
library. 

Reflection means that you can ask Swift at runtime questions about types.
I.e. you can tell Swift "what are the methods that this class implements"

This might not sound useful, but in reality is allows to do some really
clever tricks: For example, you could write a function that takes any
`struct`, lists all the properties (`var username, var age`, etc)
and writes this information into Core Data. 

Reflection in Swift is `read-only`, so you can't write any properties.
However, it is still quite powerful. This guide will explain reflection
and also show how it can be used in a practical way (the aforementioned
struct to Core Data example).

The best understanding of the topic can be achieved by having a look at
the API to see what it offers us.
