[frontMatter]
title = "Introduction"
tags = []
created = "2019-03-01 17:35:30"
description = ""
published = false

---

# Introduction

Tuples are one of Swift\'s less visible language features. They occupy a
small space between Structs and Arrays. In addition, there\'s no
comparable construct in Objective-C (or many other languages). Finally,
the usage of tuples in the standard library and in Apple\'s example code
is sparse. One could get the impression that their raison d\'être in
Swift is pattern matching, but I disgress.

Most tuple explanations concentrate on three tuple use cases (pattern
matching, return values, destructuring) and leave it at that. The
following guide tries to give a more comprehensive overview of tuples
with best practices of when to use them and when not to use them. I\'ll
also try to list those things that you can\'t do with tuples, to spare
you asking about them on stack overflow. Let\'s dive in.
