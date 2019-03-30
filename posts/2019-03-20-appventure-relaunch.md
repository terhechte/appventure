[frontMatter]
description = "Appventure has been relaunched to focus more on Swift"
title = "Relaunching Appventure"
created = "2019-03-20"
published = true
keywords = ["appventure", "relaunch"]
tags = []

[meta]
feature_image = "https://appventure.me/img-content/appventure-relaunch.png"
thumbnail = "/img-content/appventure_relaunch.png"
---

# TLDR

I'm terribly excited to finally relaunch `appventure.me` with new structure, new looks and new purpose:

- Posts are separated into articles and guides now. 
- Guides are long-form explanations on a specific subject, such as `pattern matching`. Guides can have multiple chapters, they're a bit like small books. 
- Guides try to take a specific subject and explain it in very much detail.
- Articles are more or less short Swift tips and tricks or opinion pieces
- The old non-Swift content [moved to a completely different website, terhech.de](https://terhech.de)
- Appventure.me is all about Swift now
- Almost all content & examples have been updated to the current Swift version (minus some old articles that were specific to Swift 1.0 or Swift 2.0). Each chapter and article clearly states the Swift version it was written for.
- There's side-wide search now (top right)
- The site moved to a completely new static site generator
- I'm planning much more regular content updates

# The long form explanation

I'm really excited about this update. I started working on more than a year ago but, due to time constraints and private issues, work stalled. I finally got around to working on it again earlier this year and finally made it. One of the reasons (I tell myself) of why there were few updates to this site in the past year was that the technical underpinnings were tricky. 

## The old stack

The old appventure stack ran on a custom static site generator that I wrote in Clojure in 2013. I really wanted to write the content in Emacs Org-Mode instead of Markdown so what I did was that for rendering the content, I'd fire up Emacs from the static site generator, parse the Org-Mode file, spit out the HTML, and render that into the filesystem. This worked well, but as appventure grew, this became terribly slow. On my old computer, rendering appventure after adding an article too around 4 minutes. Even worse, once I'd fixed a typo in the article, it took another 4 minutes. Now, I could have fixed all that, but I didn't want to. I'm not doing Clojure anymore and I can hardly still read the code. So when I set out to update appventure, I needed to fix the following tasks:

- Find or write a new static site engine that has many features and is *fast*
- Update the looks of appventure
- Update all the content to the most recent Swift version

Static site generators kind of are the new todo apps so I set out to write a new one. I really enjoyed working on it, and it is rendering all of appventure as well as [terhech.de](https://terhech.de) now. It is still closed source as I had to add a lot of hacks in the end in order to support enough features so that appventure could launch. I might open source it once I feel that it has enough abstractions for it to be useful for more people than just me.

This new static site generator renders appventure in a much shorter amount of time, it also detects changes in source files and reloads the browser, which makes it a joy to use. I hope this will make it easier for me to create content.

## Non-Swift Content

I mentioned [terhech.de](https://terhech.de) above. Over the years I had many articles that I would have liked to write but that I felt would not fit well on appventure as they were not about Swift (or development, [example, my music](https://sarbatka.com)). While I was working on the new appventure I felt that I needed a new host for the non-Swift content that was previously hosted on appventure. That's what [terhech.de](https://terhech.de) is about. That's where I will write about tech and non-tech topics. Some of the previous appventure articles (example, my recent project [Gitsi](https://twitter.com/terhechte/gitsi)) moved over.

## New features

As listed above, the new static site generator has a lot of nice features which improve the structure of appventure:
- There's now a project-wide search
- Posts are separated into articles and guides now. 
- Guides are long-form explanations on a specific subject, such as `pattern matching`. Guides can have multiple chapters, they're a bit like small books. 
- Guides try to take a specific subject and explain it in very much detail.
- Articles are more or less short Swift tips and tricks or opinion pieces

## Guides

As explained above, I decided to split up many of the current articles into guides. 

When you visit a guide, (such as the [guide to pattern matching](lnk::switch)), you will see that there is a content menu in the top left corner. This will show the full contents of the guide, making it easy to pick just the specific part you'd like to read about.

Guides are not static. I'll continue to update guides by adding new chapters. New chapters can easily be detected as they'll have a small `NEW` icon next to their name. I'll also announce new chapters on [twitter](https://twitter.com/terhechte) and they'll pop up in the RSS feed.

## Updated Content

Most of the content has been updated to the current Swift version. Obviously, I might have missed the one or other issue. If you find a bug, feel free to point it out to me by [creating an issue on the Github repo](https://github.com/terhechte/appventure). Some articles have not been updated to the current Swift release yet. The guides, however, all have.

## Feedback

I'm looking forward to feedback on the new website! Whether it is positive or negative feedback, [feel free to point it out to me!](https://twitter.com/terhechte) I hope you like it, cheers, Benedikt
