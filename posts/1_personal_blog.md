[frontMatter]
title = "A Personal Blog"
tags = ["various", ]
created = "2019-01-02"
description = "A brief explanation of what this is and why it exists."
published = true
---

# What is this?

Another blog? Even though I'm hardly posting to [my main one](https://appventure.me) anymore. While that is true, I want to change that. For 2019 I want to write more. However I also want to write things that are not directly Swift / iOS / Apple related. That's actually how appventure started. I wrote about Postgres, Clojure, and more.

Now, though, appventure is where I write about Swift. And that's great. I'm very thankful to have this publication and I want to write more there. I have a chock full list of articles that I'd like to publish on appventure. However, I also have a growing list of articles that are not about Swift but I'd still like to publish. Recently, I published an article about my C project [Gitsi](http://appventure.me/2019/01/24/interactive-git-status-written-in-c/) on appventure and it is clearly not the right fit. Appventure, for me, is about iOS development in Swift, not about C, or other technologies. That's why I felt that in order to write more, I actually need a better way to organize my writings into two different entities. 

That's how this new blog was born.

# What can you expect here?

There'll obviously Apple related content that is not directly related to Swift / Development (i.e. hardware, macOS). There might also be a lot of Rust as I'm really excited about Rust right now. Apart from that it will be whatever crosses my mind. Even vacation experiences. A typical blog.

# Techou

I started on this blog last week. The sane thing would have been to just go with one of the pre-existing static blog engines, such as [Hugo](https://gohugo.io/), [Pelican](https://blog.getpelican.com/), [Zola](https://www.getzola.org/), or [Cobalt](https://cobalt-org.github.io/). As you can guess, I didn't do that. Another sane thing would have been to just use one of the thousands of [pre-existing themes](https://themes.gohugo.io/). As you can imagine I didn't do that either.

Instead, last weekend, when I decided to have this new blog, I searched for some layouts but could find nothing that I really liked. Then, I decided to roll my own. While I was doing that, I realized it needed features that are more difficult to configure in pre-existing static site engines.  So I wondered if I could cobble together a very simple static site generator on that weekend. That's how [techou](https://github.com/terhechte/techou)  was born. 

<div align="center">
<br/><img class="invertable-icon" src="/content/techou_logo.svg" alt="Techou Logo" /><br/>
<br/>
</div>


Techou is japanese (てちょう) and means diary / notepad. Given that Techou was hacked over a weekend, it has a surprising amount of features. Custom Markdown syntax extensions, Auto-reload via websockets, project files, auto-generate on file change, tags, toml front matter support, meta tags per article, and templates. _This all thanks to the amazing Rust package ecosystem_. Techou is still very much a hack but I want to extend it into a very-easy-to-hack-on static site engine library. You can learn more about Techou [here](https://github.com/terhechte/techou)

Thanks for reading.

