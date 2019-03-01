[frontMatter]
title = "Introduction"
tags = []
created = "2019-03-01 11:47:01"
description = ""
published = false

---

# Introduction

Even though Swift stresses strong types, compile time safety, static
dispatch it still offers a Reflection mechanism as part of the standard
library. You may already have seen it in various blog posts or projects
like [here
(Tuples)](http://design.featherless.software/enumerating-tuple-values-swift/?utm_campaign%3DSwift%252BSandbox&utm_medium%3Demail&utm_source%3DSwift_Sandbox_12),
[here (Midi
Packets)](http://design.featherless.software/enumerate-messages-midipacket-swift-reflection/)
or [here (Core Data).](https://github.com/terhechte/corevalue) Maybe
you\'re interested in using in one of your projects, or you may want to
better understand the problem domains on which reflection can be
applied. This is an overview of the possibilities of the Swift
Reflection API based a talk I held recently at the [Macoun
conference](http://www.macoun.de) in Frankfurt, Germany.

# API Overview

The best understanding of the topic can be achieved by having a look at
the API to see what it offers us.
