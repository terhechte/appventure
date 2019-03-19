[frontMatter]
description = "How can we as a community help expanding the reach of Swift"
title = "Expanding Swift's Reach"
created = "2018-05-03"
published = true
keywords = ["swift", "linux", "server", "opensource"]
slug = "2018-05-03-expanding-swifts-reach.html"
tags = []
category = ["Blog", "All"]
[meta]
thumbnail = "/img-content/swifts_reach.png"
---

I guess we can all agree that Swift is a beautiful programming language
that manages to hit the sweet spot in terms of simplicity and
complexity. It could theoretically become one of the major languages of
the future. Currently though, Swift\'s usage is more or less constrained
to the Apple development domain (plus a few extensions such as
server-side Swift or the [recently announced Swift for
Tensorflow](https://www.tensorflow.org/community/swift)).

> My goal for Swift has always been and still is total world domination.
> It's a modest goal
>
> -   Chris Lattner

[With Swift 4.1\'s new generic
features](https://swift.org/blog/swift-4-1-released/) and the upcoming
[ABI stability in Swift 5](https://swift.org/abi-stability/), it feels
like Swift slowly reaches a point that would allow it to move beyond the
Apple domain. In this post I\'d like to discuss what I see as one of the
issues holding it back from a broader adoption. Specifically, the one
issue that can be solved by us as a community while most of the other
issues are already being worked on.

I\'d also like have a brief look at Swift\'s **competition** in this
space. I.e. other languages that also aspire to become a general purpose
language for all the domains that C++ currently encompasses - and maybe
more [^1]. By observing their take on the issue we can see where Swift
stands in comparison, and what we can do.

# System Packages

Swift has a very healthy open source community with a good amount of
fantastic, well-written, and useful packages. However, the nature of
Swift\'s current primary domain constrained these packages almost
exclusively to iOS (and much less, macOS) UI libraries. There\'re a
dozen UI Animation libraries, UI layout libraries, UI element
frameworks, UI helpers and, of course, JSON parsers. Most of those
packages don\'t even run on Linux as there is no UIKit / AppKit. Of
course, there are also several web frameworks like
[Vapor](https://vapor.codes/) or [Kitura](http://kitura.io/), and
they\'re doing a fantastic job of extending Swift\'s into the web
development realm.

However, contrary to popular opinion, companies do a lot more on Linux
than just running webservers. As we will see in a brief moment, other
languages offer a lot of system management, administration, or general
development tools and libraries that make no sense for iOS or macOS app
development but are tremendously important for systems- or
web-development. I.e. databases and their administration, system file
management, process management and administration, log and analytics
collection, container administration, deployment tooling, or even
blockchain tooling - just to name a few.

In line with Swift\'s 4.1 release, [there was a thread on Hacker News
discussing the language](https://news.ycombinator.com/item?id=16710895).
I\'ve read the entire thread multiple times due to the fact that the
answers were really interesting. What stood out to me was [the following
comment](https://news.ycombinator.com/item?id=16710895):

> The set of libraries and supported OSes is a tiny dot comparable with
> the Go and Rust. ... If we start listing the kind of libraries used in
> distributed applications, database backends, Swift has hardly none of
> them.

So lets have a look at the others.

# Competitors

The field of programming language development has seen a lot of new
competitors over the last couple of years. Naturally, we (that is, you
dear reader, and me) will probably not agree on which of these languages
we do or don\'t consider as true competition for Swift. That is,
here\'re - in no particular order - my personal picks based on gut
feelings.

Also, the opinions below are loosely held. So if you\'re a fan of any of
the languages I\'m about to mention and my description feels wrong to
you and you\'re burning with a desire for venegance and about to grab
your pitchfork and head to Twitter.. please don\'t, I\'m just a normal
guy with a loosely held opinion who most certainly is wrong about a lot
of things. Instead, use this energy to pursue the question of how it
came to be that I\'m misinformed on this particular topic and try to
help to improve on that front.

Go
--

Go has been available much longer than Swift, enjoys strong usage in the
realm of system tools, is hardly used for GUI applications, doesn\'t
provide more modern language features such as tagged unions, generics,
or functional programming constructs. It is easy to learn, fast, uses a
Garbage Collector and the resulting binaries are lightweight in terms of
memory. The garbage collector make it somewhat tricky to use Go for
embedded development or even Webassembly.

The good performance, simplicity of the language and low memory
footprint lead to the development of a lot of system tools & libraries,
such as: Grafana, Kubernetes, CoreOS-etcd, Go-Ethereum, CockroachDB,
Hub, Terraform and many, many others. Have a look at this [list just to
observe how many libraries there are for any use case possibly
imaginable](https://github.com/avelino/awesome-go).

In short, if you want to develop anything system-based, almost all
packages you might need as dependencies are readily available.

## Kotlin

Kotlin, basically the Swift for Android is a language that feels and
looks a lot like Swift but is - under the hood - quite different. The
JVM foundation of Kotlin forces it to utilize a much stronger usage of
reference types vs. value types. Like Go, the Garbage Collector makes
embedded & systems development a challenge, however [there is
Kotlin-Native which will make this more feasible in the
future.](https://kotlinlang.org/docs/reference/native-overview.html) It
builds with LLVM, supports embedded platforms, Webassembly, and much
more. Kotlin can also be compiled to Javascript, and Kotlin-Native even
allows buliding Frameworks for iOS apps.

Kotlin could also become a big language in the future but is currently
held back by the same mechanics that are also holding back Swift: Almost
all available open source libraries are primarily for Android
development (i.e. UI, etc). While Kotlin native solves the issues that a
pure JVM language would have, I have no idea how performant and
lightweight Kotlin native could actually become (i.e. Compared to C++ or
Swift, especially for things like embedded development, complex systems
development, or Webassembly).

## Rust

Rust is an interesting language. Actually so interesting that I spend
the last couple of months slowly learning it. In many ways it is very
similar to Swift - but harder (but this is a topic for a future blog
post). it feels like the two languages started out diametrically opposed
from each other: Swift started out as an (mostly) easy to learn language
with a easy-to-grasp feature set which is slowly adding more complex
features. Rust started out as a complex language which is slowly adding
simpler abstractions or better error messages to make it more
approachable for beginners. Given that both languages have a very
similar syntax it wouldn\'t surprise me when, at some point in the
future, both languages converge to a point of high similarity in terms
of features and simplicity / complexity. However, currently, Rust offers
a couple of very attractive features hidden behind a more complex
learning experience:

A much better cross-platform story, a hard but rewarding memory
management story (i.e. lifetimes / ownership) [that is thankfully also
partially coming to Swift in the
future](https://github.com/apple/swift/blob/master/docs/OwnershipManifesto.md),
support for
[Webassembly](https://rust-lang-nursery.github.io/rust-wasm/) (i.e. you
can write frontend apps in Rust), and the beginnings of a really good
foundation of packages to allow users to quickly get started on new
projects. While it does not offer the same amount of high-profile
projects like Go, there\'re already a couple of promising projects
(CoreUtils, RedoxOS, TikV, Vagga, Servo, Parity), but more importantly,
there are many libraries for interaction with third party dependencies.
[Have a look at this
list.](https://github.com/rust-unofficial/awesome-rust)

## Others

There\'re also D, Nim, Chrystal, Elixir, TypeScript, and obviously C++
itself but this post is already long enough as it is.

# What can we see

Swift currently falls short in the area of system packages. This is also
a chicken-egg problem:

> As long as there are not enough system packages, an interested
> developer will try out Swift, but will not find a package for his
> favorite database. Not interested in porting a database package just
> for the sake of writing a simple example app, he will back off and
> never start to enjoy the language enough to start submitting his own
> system packages.

To me it feels like we need to improve our system package / library
game. It would certainly be nice if we had something like Kubernetes
written in Swift, but in order for such a project to emerge, we need a
good set of base libraries that are useful for general systems
development. Libraries for tasks or third party services in the
following domains (also, some of those domains may have packages
already, but that doesn\'t mean we need more):

-   Authentication
-   Caching
-   Concurrency
-   Cloud Providers
-   Command Line Argument Parsing
-   Command Line UI
-   Command Line Editors
-   Compression
-   Computations (i.e. BLAS)
-   Cryptography
-   Databases
-   Data Processing
-   Data Structures
-   Data Visualization
-   Date and Time
-   Distributed Systems
-   Email
-   Encoding & Decoding
-   Filesystems
-   Image Processing
-   Machine Learning
-   Parsing
-   Text Processing
-   Virtualization

In order to become a valid general purpose language on Non-Apple
operating systems, I think, Swift needs to offer a healthy ecosystem of
useful system packages on all platforms.

# So, what can you do

## Write libraries

Before you decide to write the 150th JSON parser, Animation library,
custom switch button, or collection view / table view abstraction,
consider writing a fully working cross platform system library. If you
can\'t come up with an idea head over to Rust or Go and see what they
have to offer.

## Rewrite Existing C libraries

For certain use cases, Swift does offer libraries but only via a small
shism to an underlying C implementation. While that does get the job
done, it introduces a very unsafe language into the mix, something we
should only need to do in use cases where performance is absolutely
critical. So, if you can\'t think of anything you\'d want to write,
maybe write a pure-swift implementation of something you already use.
That\'s also a great opportunity for learning more C and in turn loving
Swift even more ;-)

## Care about Linux

I recently wrote a small application in Vapor and for that I needed a
couple of additional dependencies (i.e. for time calculations) and
almost all existing libraries were iOS / macOS only. If you already work
on something that could be cross platform (due to no UIKit / AppKit
dependencies) try to go the extra step of testing it on Swift Linux.

This might also be easier than it sounds. [There\'s a readily-available
docker image for Swift
4.1](https://hub.docker.com/r/ibmcom/swift-ubuntu/tags/), so you can
just run that in order to test your code.[^2]. Alternatively, you can
run [Virtualbox](https://www.virtualbox.org/) if you\'d rather have a
full running VM.

## Support Swift Package Manager

If you have a library already, try to always support the Swift Package
Manager in addition to CocoaPods and Carthage.

## Work on Foundation

Another thing that is still difficult is that Swift for Linux\'s
[Foundation library](https://github.com/apple/swift-corelibs-foundation)
is a re-implementation of iOS/macOS foundation and therefore still has
unimplemented features and (especially tricky) bugs. This means that
code you write on your Mac in Xcode might run great, but it will crash
on Linux because of a Linux-Only foundation bug. Making Foundation for
Linux better is another great task to work on in order to improve
Swift\'s reach.

The easiest starter for this is to head over to the [Swift
Jira](https://bugs.swift.org/secure/Dashboard.jspa) and search for
Foundation bugs.

## Help out Foundation

If you don\'t have the time or are not interested in working on Swift
Foundation, you can still help out by using it / testing it on Linux and
submitting bug reports. The more people use it, the more stable it will
become.

## Help the Linux editing experience

Linux users won\'t have Xcode, so they\'ll be using Atom or Emacs or Vim
or VSCode. There\'re already multiple projects that offer Swift support
for these editors, but it feels like we can also improve on this front.
If you have some cycles to spare, play around with these projects and
your favorite non-Xcode editor, see if things work as expected,
otherwise create issues or (even better!) try to actively fix them ;)

## Try Swift in San Jose

If you happen to be in San Jose during this years WWDC, there\'s a great
opportunity for you to learn something, meet interesting people, and
help out Swift: [The Try Swift San
Jose](https://www.tryswift.co/events/2018/sanjose/).

> ...your chance to contribute to Swift. Join a panel of Swift Open
> Source contributors for a discussion about the latest news on the
> Swift open source project, then contribute to Swift Evolution yourself
> with the help of community mentors!

[Check it out](https://www.tryswift.co/events/2018/sanjose/).

# I should be doing this

I haven\'t had much time to do any open source work in the past 1.5
years because I was busy working on [my own (closed source)
project](https://photodesk-app.com), but I really want to work on open
source Swift code again. I really like Swift, it is a great language,
and helping it to (hopefully) succeed feels like the best pasttime to
have. If you feel the same, feel free to share this article.

[Also, for any discussion on this article, head to
Twitter.](https://twitter.com/terhechte)

[^1]: I.e. WebAssembly

[^2]: I\'m trying to write another blog post that explains this in much
    more detail
