[frontMatter]
description = "FIXME FIXME FIXME"
title = "Clojure/Enlive Static Site Generator that keeps your HTML intact"
created = "2014-01-22"
published = true
keywords = ["clojure", "static", "site", "generator", "jekyll", "html", "enlive"]
slug = "2014-01-22-clojure-enlive-static-site-generator-that-keeps-html-intact.html"
tags = ["blog", "clojure"]
---

Static is a Static Site Generator written in Clojure that I just
released. It is a fork of the original static
<http://nakkaya.com/static.html> from Nurullah Akkaya. I chose
Nurullah\'s Static because it had lots of great i/o features, but had to
fork it because it differed in a couple of ways from what I wanted my
blog to be:

-   Have one (or several) html files as templates that I do not need to
    break up into parts and that are not plastered with weird template
    tags. So I\'m using Enlive to define selectors and the generator
    uses theses selectors to fill the content into the html structure.
    That makes it really really easy to edit the html for the blog
    without having to go the html -\> haml/whatever -\> break up -\> ...
    route.
-   Implement a strong seperation between layout and code: The normal
    Static generator mixes design/layout with Clojure code (within the
    project files, and in the generator source itself). This makes it
    difficult to implement a new layout easily and use it for anything
    but the original envisioned layout. What\'s more, I wanted to define
    my layout in HTML and not have to edit multiple Clojure files to
    make it work.
-   Allow different templates for the different possible views that A
    blog contains. I.e. a template for list views, a template for a blog
    post, and a template for multiple blog posts.

## Features:

-   **Template are all html**: Without any templating language or
    breaking it into pieces in between. In fact, the html templates are
    stored in the public/ folder with all your CSS and images and
    Javascript, so just fire up a \'python -m SimpleHTTPServer\' and you
    can edit your templates as if they were an actual site. Once you\'re
    done, simply run the build process and it is finished.
-   **Org Mode Support**: This may not be interesting for most people,
    but I really dig Emacs Org Mode for document editing. Static has
    terrific Org Mode support. For an example of how to set up your
    environment, see the [Github
    Repo](http://github.com/terhechte/static)
-   **Projects**: Every document put into the `site/` folder will be
    added to the list of projects that can be accessed in a template.
    This allows you to create a small document for any page you\'d like
    to host on your blog. It can then be easily included into your
    navigation. Currently, this works only well for HTML, Markdown and
    Org Mode documents.
-   **Tags**: Every document can be tagged, and the tags can be listed
    on the site, and link to tag archives
-   **Archives**: An archive can automatically be generated for all
    content. You have the option of having a seperate archive page for
    each month or having just one huge archive list.
-   **Just two templates**: There\'re just two templates that need to be
    defined, a list template (for archives and tag lists) and a content
    template (for one or multiple posts). And they can even be the same
    if you wish.
-   **Footnotes in Markdown**: There\'s a bit of support for footnotes
    in Markdown, however since I\'m mostly using Org Mode, which
    automatically inserts the markup for them, I never went beyond
    implementing the basics.
-   **Compilable to jar file**: This means that you can compile it once,
    and whether you update your operating system, or switch to a
    different platform, or re-install something or change your
    environment, the generator will work - as long as you have Java
    installed. I find this much better to generators like, say, Jekyll,
    where it (for me) [often failed when I updated Ruby or installed a
    new Gem (or really changed
    anything)](http://appventure.me/2014/01/20/now-running-clojure/).

## Templates:

Templating is done by modifying the DOM of a html template through
Clojure/Enlive scripts. This allows to layout / design in html and just
bind the date by adding a couple of DOM selectors. I find this much
easier than having to split a template into seperate pieces like in
traditional templating languages.

Templating consists out of multiple parts:

-   The html template file, usually ~index~.html in public/. In this
    example we\'ll call it index.html.
-   The base template file, that contains all the definitions, snippets,
    and more that you need in your templates
-   The default and list templates which are lists of html selectors and
    actions which are then performed against the results.

Since all templating is done via
[Enlive](https://github.com/cgrand/enlive) it may be beneficial to have
a look at it first. [Here\'s a fantastic
tutorial](https://github.com/swannodette/enlive-tutorial/) from David
Nolen. However, the example below should be simple enough to understand
it even without having a look at Enlive first.

With that in mind, lets see a simple example:

public/index.html

``` HTML
<html>
<head><title>title</title></head>
<body>
    <div id='content'>
        <article>
            <h1>text</h1>
            <div>content</div>
        </article>
        <div id='list'>
            <h1>title</h1>
            <div>entry</div>
        </div>
    </div>
</body>
</html>
```

This is straightforward html and a simple model to explain templating.
When this is being used to render the **index.html** of our blog, we
want the following to happen.

1.  Replace `<title>title</title>` with the site title from our metadata
2.  Remove the `#list` element as the index is not a list page (unlike
    tag list or archives)
3.  Use the `<article>` entry and clone it for each of our posts
    replacing h1 with the title and `<div>content</div>` with the
    content.

Enlive selectors are a little bit different than CSS selectors, but
still easy to graps, so first lets see which selectors we need:

1.  `[:head :title]`: That\'s it, and in there we just want to replace
    everythign
2.  `[:#list]`: That\'s it, and we just want to remove what we find
3.  This is a bit more tricky, we first want `[:div#content]` to select
    our container div, but then we want to fill it with an instance of
    our `<article>` html structure for each item we have in our post
    contents.

Static always binds two variables to the template scope: **metadata**
and **content**.

Enlive works in a way where you define a selector and then an operation
that has to be performed on the result of that selector, so now we will
create a simple base template to define snippets for the article
entries. A snipped is a piece of html from a template that you can clone
/ use multiple times - just what we need for our article.

templates/base.clj

``` Clojure
; template-path prefixes the name with the correct path
; We bind this to a var so we can access it easily

(def base-template-file (static.core/template-path "_index.html"))

; This is the snipped for our article template. 
; It will grab the releveant [:article] portion for us 
; and apply the contents to the h1 and the div
; the name of our snippet *article-template* is later available as a function

(enlive/defsnippet article-template base-template-file [:article] 
  ; This snippet will be called with a Post instance. 
  ; Posts are Maps. We just need title and url here

  [{:keys [title url]}] 

    ; we tell enlive to replace the 'content' of the :h1 
    ; tag with the contents of the title var

    [:h1] (enlive/content title) 

    ; we tell enive to replace the 'content' of 
    ; the :div tag with the contents of the url var

    [:div] (enlive/content url) 

    )
```

We\'re almost done. We have defined our article snippet, now we just
need to maps this snippet against all the posts that we have. This is
being done in our default template.

### templates/default.clj

``` Clojure
; The define-template is a macro in core.clj 
; that helps us define simple templates
(define-template base-template-file

  ; We replace the title contents with our site title
  ; or, with the post title, if the author define one

  [:head :title] (enlive/content (if-let [t (:title metadata)] t (:site-title metadata)))

  ; We replace the contents of the #content node with the results of 
  ; mapping our earlier-defined article function against our content

  [:#content] (enlive/content (map #(article %) content))

  ; And finally, we remove the list, as we don't need it. 
  ; Returning nil for an element will get rid of it

  [:#list] nil
)
```

That\'s it! Once these selectors are in place, you\'re done and your
content will be written out. Here\'re some helpful tips on how to write
good selectors:

-   Try to be very specific, otherwise future changes in your html
    require you to re-write your selectors afterwards. I.e. rather use
    `[:#content]` instead of
    `[:body :> :div#container :> :div#content]`. In the later case, once
    you decide to remove the div\#container at some point in the future,
    the selector will fail.
-   The format of the selectors is always `[selector] (action)` so you
    can\'t just do a println for debugging. An easy way to do that,
    though, is by including it in a useless selector:
    `[:head] #(when "1" (println content) %)` will just replace `:head`
    with :head and print content as a side effect.

## Caveats

-   This is my first take on a big Clojure project after reading two
    books and dabbling around with the repl the code may not be good, so
    if you find something atrocious, just send a pull request.
-   The way that I implemented the enlive templates with a base template
    and additional templates feels kinda awful. With my limited Clojure
    knowledge I couldn\'t really come up with anything else that would
    allow me to eval a template and allow it to import additional
    functions from another file to minimize repetition.
-   This is only tested for my personal blog, it may be that if you\'re
    trying to do something else, it doesn\'t work for that, in that
    case, you\'re welcome to fork :)
-   This started out as a proof-of-concept and turned out to be working
    so well that I decided to release it so maybe others can use it too.
    This means that the git commit history could certainly be cleaner.
    There\'s one huge commit that brings in a ton of changes.

## Clone it, Fork it, Source:

[The source is available on Github](http://github.com/terhechte/static)
