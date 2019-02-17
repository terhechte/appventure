[frontMatter]
title = "Applying ranges for grading"
tags = []
created = "2019-02-15 20:40:47"
description = ""
published = false

---

# Applying ranges for grading

So you\'re writing the grading iOS app for your local Highschool. The
teachers want to enter a number value from 0 to 100 and receive the
grade character for it (A - F). Pattern Matching to the rescue:

``` Swift
let aGrade = 84

switch aGrade {
case 90...100: print("A")
case 80...90: print("B")
case 70...80: print("C")
case 60...70: print("D")
case 0...60: print("F")
default:
    print("Incorrect Grade")
}
```
