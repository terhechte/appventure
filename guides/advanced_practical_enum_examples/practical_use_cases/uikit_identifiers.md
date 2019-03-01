[frontMatter]
title = "UIKit Identifiers"
tags = []
created = "2019-03-01 16:31:41"
description = ""
published = false

---

# UIKit Identifiers

Enums can be used to map reuse identifiers or storyboard identifiers
from stringly typed information to something the type checker can
understand. Imagine a UITableView with different prototype cells:

``` Swift
enum CellType: String {
    case ButtonValueCell = "ButtonValueCell"
    case UnitEditCell = "UnitEditCell"
    case LabelCell = "LabelCell"
    case ResultLabelCell = "ResultLabelCell"
}
```
