[frontMatter]
title = "Legacy API and Value Extractions"
tags = []
created = "2019-02-15 20:40:47"
description = ""
published = false

---

# Legacy API and Value Extractions

Oftentimes, when you get data from an external source, like a library,
or an API, it is not only good practice but usually even required that
you check the data for consistency before interpreting it. You need to
make sure that all keys exists or that the data is of the correct type,
or the arrays have the required length. Not doing so can lead from buggy
behaviour (missing key) to crash of the app (indexing non-existent array
items). The classic way to do this is by nesting `if` statements.

Let\'s imagine an API that returns a user. However, there\'re two types
of users: System users - like the administrator, or the postmaster - and
local users - like \"John B\", \"Bill Gates\", etc. Due to the way the
system was designed and grew, there\'re a couple of nuisances that API
consumers have to deal with:

-   `system` and `local` users come via the same API call.
-   the `department` key may not exist, since early versions of the db
    did not have that field and early employees never had to fill it
    out.
-   the `name` array contains either 4 items (username, middlename,
    lastname, firstname) or 2 items (full name, username) depending on
    when the user was created.
-   the `age` is an Integer with the age of the user

Our system needs to create user accounts for all system users from this
API with only the following information: username, department. We only
need users born before 1980. If no department is given, \"Corp\" is
assumed.

``` Swift
func legacyAPI(id: Int) -> [String: AnyObject] {
    return ["type": "system", "department": "Dark Arts", "age": 57, 
           "name": ["voldemort", "Tom", "Marvolo", "Riddle"]] 
}
```

Given these constraints, let\'s develop a pattern match for it:

``` Swift
let item = legacyAPI(4)
switch (item["type"], item["department"], item["age"], item["name"]) {
   case let (sys as String, dep as String, age as Int, name as [String]) where 
      age < 1980 &&
      sys == "system":
     createSystemUser(name.count == 2 ? name.last! : name.first!, dep: dep ?? "Corp")
  default:()
}

// returns ("voldemort", "Dark Arts")
```

Note that this code makes one dangerous assumption, which is that if the
name array does not have 2 items, it **must** have 4 items. If that case
doesn\'t hold, and we get a zero item name array, this would crash.

Other than that, it is a nice example of how pattern matching even with
just one case can help you write cleaner code and simplify value
extractions.

Also, see how we\'re writing `let` at the beginning right after the
case, and don\'t have to repeat it for each assignment within the case.
