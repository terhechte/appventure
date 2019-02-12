[frontMatter]
published = true
title = "Now Running Clojure"
created = "2014-01-20"
slug = "2014-01-20-now-running-clojure.html"
tags = ["clojure", "blog"]
---

This blog has been lingering for far too long now. The reasons for that
are manifold, but there are three primary ones which I would like to
elaborate further.

## Flick a Fruit, for iPad

Shortly after finishing this blog, in early January 2012, a good friend
came over to visit me and we started hacking on an indie project which
we were both very excited about: A fun game for the iPad. We estimated
it to be around 3-4 months of work and spend the whole January devotedly
hacking along. Sadly, we grossly miscalculated the required time, we
kept adding features to it, and we both could only work part time on the
project as we were also busy with other things. All in all, it took us
almost 1.5 years to finish the project. I\'m really proud about it and I
learned a ton of stuff along the way, but working on this huge game in
addition to managing my other projects (most notably InstaDesk nee
PhotoDesk[^1]) consumed so much time that I stopped even thinking about
writing new entries for the Appventure blog. The game is currently in a
market test in Canada, if you\'re interested, [give it a
try!](https://itunes.apple.com/ca/app/flick-a-fruit/id771895296?mt%3D8)

## Lack of Focus

Also, 2012 and especially 2013 were transformative years for me. While
honing my Objective-C knowledge, I felt the accumulated wisdom of 10
years of web applications (Javascript/PHP and later Javascript/Python)
slowly fade away. Objective-C is ill suited for web apps[^2], and I\'d
grown weary of Python and wanted to try something new. So I spend most
of 2012 and 2013 trying out various languages and playing around with
different frameworks. All this resulted in a certain lack of focus of
what to write about.

## Jekyll Static Site Generator

The previous version of this blog ran on [Jekyll](http://jekyllrb.com/),
a static site Generator for Ruby. It sounded like a great idea back
then. I could write my posts comfortably in Vim with Markdown and would
not have to mess around with online editors or weird UI. Also, just
having a static set of html would ease the burden on the server and
conveniently expose no security issues[^3].

I quickly had everything running in Jekyll and all was good. However,
after a some time, I constantly ran into issues with this setup. Whenver
I wanted to write a new post, Jekyll would crash. I\'m not very familiar
with Ruby and I hardly use it for anything, but from time to time
there\'re tools that I want to use that are written in Ruby, and then
they need different Ruby versions, and different Gems, and then you need
rvm or rbenv in order to manage all that, and somehow the entangled mess
that I\'ve created here lead to a point where whenever I wanted to use
Jekyll, it would crash because something crucial was missing. I usually
would spend one hour debugging this, until Jekyll ran again, and then,
the next time I was about to write something, there would be a new
error.

A couple of days ago I wanted to write a post again, only to be greeted
by a new error, \'require cannot load such file, inflection error\'.
This was especially demotivating as I had spend a considerable amount of
time updating Jekyll to the latested and greatest and getting everything
running again a couple of weeks ago. At this point, I decided I needed a
better solution. Something compiled which would always work no matter
what happened to my system, something which was not dependent upon a
myriad of gems and files in weird locations [^4].

## Everything new everything better

With the above in mind, I decided to address the problems outlined above
and re-think and re-do this blog. Along the way, I also created a new
layout that works better on mobile devices, offers more information and
in general looks more streamlined.

-   **Clojure**: I wanted to have a static blog solution that can be
    compiled and just works, even if I update my operating system.
    Clojure looked like a great solution for this. I forked
    [Static](http://nakkaya.com/static.html), a static site generator
    for Clojure [^5] and modified it to better fit my needs. I\'m really
    happy with the result.
-   **Focus**: I\'m doing lots of research for the various projects that
    I\'m working on, and I\'ve installed and used several documentation
    systems over the years to store it. The solution that worked best so
    far was to write it as self-contained
    [Org-Mode](http://orgmode.org/) documents in Emacs. My main focus
    for the Appventure blog will be to share some of this research here.
    What\'s really great about the Static generator that I used, is that
    it allows to use org mode documents as input (versus, say Markdown).
    So I can just take my research docs, which already are Org mode
    documents, and publish them here on my blog.
-   **Time**: I\'ve also finished a lot of projects over the last year
    so that I can invest more time into other things - including this
    blog - in 2014. Most notably, I am back on schedule, which really
    wasn\'t the case for the past 6-8 months.

So all in all things look good and I\'m looking forward to writing more.
In addition to that, I really enjoyed working on the Static extensions
in Clojure and I\'m confident that a continous usage of this blog will
help me extend it even more.

[^1]: A change in Instagram\'s marketing guidelines forced me to rename
    the app in late 2013

[^2]: Even though I tried by using it for frontend work via
    [Cappuccino](http://www.cappuccino-project.org/)

[^3]: I\'ve been burned by WordPress more than once simply because I
    forgot to update to the latest version quickly enough.

[^4]: I am not implying that this is a Ruby or Jekyll error. I think
    that the issue was that I know too little Ruby and that my
    environment was all messed up. In hindsight I should have gone with
    a Python static site generator, since I know Python.

[^5]: I\'m still in the process of finishing the final tidbits before
    I\'ll push my modifications to Github. The main difference is that I
    encapsulated the layout using Enlive templates compared to the
    original Static, where the layout was mixed between a Clojure file
    and the compiled sourcecode
