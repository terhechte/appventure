[frontMatter]
title = "Settings"
tags = []
created = "2019-03-01 16:31:41"
description = ""
published = false

[meta]
swift_version = "5.1"
---

# Settings

[This is a very, very smart solution that Erica Sadun came up
with](http://ericasadun.com/2015/10/19/sets-vs-dictionaries-smackdown-in-swiftlang/?utm_campaign%3DSwift%252BSandbox&utm_medium%3Demail&utm_source%3DSwift_Sandbox_12).
Basically whenever you\'d use a dictionary of attribute keys as a way to
configure an item, you\'d instead use a `Set` of enums with associated
values. That way, the type checker can confirm that your configuration
values are of the correct type.

[For more details, and proper examples, check out her original blog
post.](http://ericasadun.com/2015/10/19/sets-vs-dictionaries-smackdown-in-swiftlang/?utm_campaign%3DSwift%252BSandbox&utm_medium%3Demail&utm_source%3DSwift_Sandbox_12)
