[frontMatter]
title = "Introduction"
tags = []
created = "2019-03-01 16:29:51"
description = ""
published = true

---

# Introduction

When and how to use enums in Swift? This is a detailed practical
overview of all the possibilities enums can offer you.

Similarly to the [`switch`
statement](lnk::switch),
`enum`\'s in Swift may at first glance look like a slightly improved
variant of the well known **C** `enum` statement. I.e. a type that
allows you to define that something is \"one of something more
general\". However, the particular design
decisions behind Swift\'s enums allow it to be used in a much wider
range of practical scenarios than plain **C** enums. In particular,
they\'re great tools to clearly manifest the intentions of your code.

In this post, we\'ll first look at the syntax and possibilities of using
`enum`, and will then use them in a variety of (hopefully) practical,
real world scenarios to give a better idea of how and when to use them.
We\'ll also look a bit at how enums are being used in the Swift Standard
library.

Before we dive in, here\'s a definition of what `enums` can be. We\'ll
revisit this definition later on:

\"Enums declare types with finite sets of possible states and
accompanying values. With nesting, methods, associated values, and
pattern matching, however, enums can define any hierarchically organized
data.\"

First, though, what are `enums`?
