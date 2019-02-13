[frontMatter]
description = "FIXME FIXME FIXME"
title = "An Emacs Lisp tooling tutorial, writing a bulk mailer"
created = "2014-01-29"
published = true
keywords = ["emacs", "lisp", "bulk", "mailer", "tutorial", "email", "vim", "vimscript", "evil"]
tags = ["emacs"]
---

---
attr_html: ':align center :class screenshot'
## caption: Emacs Bulk Mailer Screenshot

There were serveral reasons why I decided to switch from Vim to
Emacs+Evil[^1] almost a year ago. I\'d been using Vim full time since
somewhere between 2009 and 2010, and I\'d solely used it on servers and
in terminals at least since 1999. Before 2009, I was an avid TextMate
user and it was only when I understood the power of Vim macros and
plugins that I made the full switch. Then, around one year ago, I
decided to switch again and try Emacs. I don\'t want to go into the
various reasons for this, that\'s for another post, but I\'d like to
present one in particular: Emacs Lisp.

One of the reasons why I am attracted to editors like Vim and Emacs is
because I am lazy. I don\'t want to spent my time doing things which can
probably be automated. And as a programmer, I see automation
opportunities everywhere. Vim and Emacs offer complex macro abilities
that make it easy to take boring, redundant tasks, encapsulate them in a
dedicated action, and perform them over a range of tasks. Examples are
[wrapping Python
code](http://vimgolf.com/challenges/4d1aa1d9b8cb34093200039f), [turning
csv into
queries](http://vimgolf.com/challenges/4d1b78e281502541ad000009),
[changing paths in CSS
files](http://vimgolf.com/challenges/4fe3d2c2f73248000100004b) or
[working with tabular
data](http://vimgolf.com/challenges/50a2bdd4f0ea8a0002000055). All this
can also be done with other editors, but Vim (in this example) makes it
very easy to accomplish this with only a few keystrokes.

However, once the complexity of the to-be-automated task gets too high,
the macro approach does not work so well anymore. Vim offers Vimscript
for this, a scripting language for editor extensions[^2]. Emacs offers
Emacs Lisp which belongs to the Lisp family of languages, like Common
Lisp, Scheme or nowadays Clojure. Since I wanted to dive deeper into
Lisp anyway, and since I never liked Vimscript much (There\'s also no
use for Vimscript outside of Vim, contrary to Lisp), being able to code
Emacs in Lisp was one of the reasons why I switched[^3].

### Easily Extending Emacs with Lisp

Shortly after feeling at home in Emacs, I started hacking in Emacs Lisp
to get a feeling for it. Compared to other editors, it felt very natural
and easy to extend it. The process is rather simple:

1.  Create a new EmacsLisp Buffer / File
2.  Write some EmacsLisp Code
3.  Select the code and evaluate it
4.  Now you can use the feature

You don\'t even have to save the code in order to use it.

The following line of code binds the shortcut `ctrl-x + 8` to a function
that inserts the string \"test\" at the current cursor position

``` Lisp
(global-set-key (kbd "C-x 8") (lambda () (interactive) (insert "test")))
```

In order to use it, you don\'t have to save or start anything, simply
type it, and at the end hit `ctrl-x ctrl-e`. After that, the command has
been registered and you can use it anywhere.

Lets say you\'re editing a DNA code file, and in there you have to
repeat a certain set of characters n times, i.e.
`gatacagatacagataca...`. So you\'d like a function that you can hand the
characters as well as how often you want them repeated[^4]. The required
code for that is quite simple:

``` Lisp
(defun repeat-the-chars (chars repeat)
  (interactive "MEnter Characters: \nnEnter Repetitions: ")
  (mapcar (lambda (x) (insert chars)) (number-sequence 0 repeat)))

(global-set-key (kbd "C-x 8") 'repeat-the-chars)
```

-   The line `(interactive "MEnter ...)` is an interactive format
    string. It tells Emacs to read user input when calling the function.
    First, it will ask for a String (`M` is the input format code for a
    string), then it will ask for a Number (`n` is the input format code
    for a number). These two values will then be added as function
    arguments (`chars` and `repeat`).
-   The line `(mapcar ...)` runs a anonymous function / lambda over the
    number range from 0 until `repeat`. Each function invocation uses
    the `insert` call to insert text.
-   Finally, the `global-set-key` line tells Emacs to run the function
    `repeat-the-chars` when using the `ctrl-x + 8` shortcut. The quote
    (**\'**) in front of the function name keep Emacs from executing it
    right away. It is a bit like a function pointer. It quotes the
    symbol instead of evaluating it right away.

I find this impressively easy. This allows me to quickly write short
functions for complex tasks whenever I deem it necessary. I recently had
to write [Scala](http://www.scala-lang.org) code to define models for
the [Slick framework](http://slick.typesafe.com). The models had a lot
of fields, but the definitions all looked rather similar. The syntax was
as follows:

``` Swift
def name = column[String] ("bo_name")
def location = column[String] ("bo_location")
def opens = column[Int] ("bo_opens")
def closes = column[Int] ("bo_closes")
```

Since I had to write a lot of fields in this a syntax, I sought a way to
automate it. I wrote the following Emacs Lisp Snippet:

``` Lisp
(defun create-column (name type)
  (interactive "Mname: \nMtype: ")
  (setq tp (split-string name "_"))
  (insert (format "  def %s = column[%s] (\"%s\")\n"
                  (last tp) type name)))
(global-set-key (kbd "C-x 1") 'repeat-the-chars)
```

-   `setq` defines a local variable \'tp\' that contains a list split by
    \"\_\". So when I enter \"bo~test~\" it would contain (\"bo\",
    \"test\")
-   `(last tp)` gets the last element from the list tp. The rest should
    be self explanatory

After this, I could just hit `ctrl-x + 1`, Enter the type and name of
the field, and it would output a field definition as above[^5].

After these simple explorations of why Emacs Lisp is nice, lets have a
look at something more elaborate. But first, a sidenote about calling
functions.

### Simple Function Calling

As you have seen above, whenever I wrote a new function, I bound it to a
keyboard shortcut, like `ctrl-x + 8`. This has several disadvantages
though:

-   You never now which keyboard shortcuts are really free, as different
    major and minor Emacs modes (i.e. modes for different languages or
    editing extensions) may also set a shortcut for the key that you
    chose.
-   If you have too many functions, there\'re no keys left or it will be
    confusing to remember which key did what.

Fortunately the default setup of Emacs has a fantastic alternative to
setting keyboard shortcuts, [the `M-x`
shortcut](https://www.gnu.org/software/emacs/manual/html_node/emacs/M_002dx.html)
to run commands by name. After typing the shortcut, you can simply enter
the name of the function that you\'re searching for and the function
will be executed. Even better, Emacs has integrated auto completion for
this, so if you happen to not remember the detailed name of the function
anymore - no problem. Even better, there\'re [Emacs plugins that offer
fuzzy searching](https://github.com/emacs-helm/helm) for this, so
instead of entering `repeat-the-chars` you simply enter `repeat char`
and the correct function will be highlighted.

This is a great way to call any function that you defined previously, or
any function that was delivered with Emacs or with one of the plugins
that you installed. I can\'t stress how awesome this is. Imagine you\'re
searching for a function to truncate lines in Emacs. Just hit `M-x` type
\"truncate\" and `toggle-truncate-lines` will appear in the search
results. It is like QuickSilver, Butler, Spotlight or Alfred for all the
functions in your editor.

### Writing a simple bulk mailer in Emacs Lisp

Now that we\'ve seen the basics of Emacs Lisp functions, let\'s try our
hands on something more difficult. One of the advantages[^6] of Emacs is
that it offers so much functionality in various disciplines that it can
almost be seen as an operating system. There\'s a newsgroup reader, a
webbrowser, a terminal, a mail reader, a calendar, a todo framework, a
flowchart and UML mode, a RSS reader, a couple of games, and much more.
As explained above, all these modes offer functions that you can call
from your Emacs Lisp code. This makes it terribly easy to hack together
a complex mode to achieve several things at once[^7].

Now we need a problem to solve. Consider you\'re working at the hottest
new startup and you\'re about to launch. Your boss comes over to explain
a problem that just rose up. You need to send out the press release to a
ton of tech websites, but there\'s no money left to buy a bulk mailing
software, and there\'s also no time left to cobble something together in
PHP and MySQL (or Python or Ruby), and now the whole startup is damned
just because they can\'t get the press release out.

You look at him with with a soft expression of understanding, unfold
your fingers and answer \"I\'ll have that running in Emacs in 15
minutes\", enjoying the puzzled look in his eyes as he remembers how he
and the other Textmate users always made fun of you and your very weird
editor and how you\'re still living in the 80ties[^8]. So now there\'s
our problem, and we need to solve it **quickly** lest the others will
start ridiculing Emacs again.

First, we\'ll need to set up Emacs to send mail. Thankfully, that\'s
[easy and already documented
elsewhere](http://www.emacswiki.org/emacs/SendingMail).

The first 3 minutes are over, but now your Emacs can send mails just
fine using the `compose-mail` function.

1.  Getting the mail data

    Next, we need to get our list of addresses from somewhere. We could
    read it from a database, or from a CSV file, or - probably the
    simplest solution - we just open it as a file in Emacs and advance
    over it line for line.

    Our file will have the format:

    ``` CSV
    "Carl" "Hogan" "VentureBeat" "hogan@venturebeat.com"
    "Claus" "Cafka" "StartupStartup" "claus@startupstartup.com"
    ```

    We want to define a function `get-mail-data` that should return a
    map/hash/dictionary with the keys \"name\", \"surname\", \"site\"
    and \"email\".

        (defun get-mail-data (from-buffer-name)
          "Return a dictionary/hash/map from the data buffer with the keys
           name, surname, site and email set."
          (pairlis '("name" "surname" "site" "email")
                   (split-string-and-unquote
                    (with-current-buffer (get-buffer from-buffer-name)
                      (buffer-substring-no-properties (line-beginning-position)
                                                      (line-end-position))))))

    -   `pairlis` Creates a paired list with its arguments. Thus
        (pairlis \'(\"a\" \"b\") (1 2)) becomes \'((\"a\" 1)(\"b\" 2))
    -   The `with-current-buffer get-buffer buffer-substring...`
        function is simple, it gets the current line without formatting
        properties (i.e. bold etc) from the buffer in the argument
        `from-buffer-name`.

    Another 3 minutes are over.

2.  Getting the mail template

    Now, we also need to get the text from the template that should be
    send. Our template will have template tags enclosed in brackets,
    like this `[email]`.

        Hey [name] [surname]

        I'd like to show you our new startup, Example Startup. We think that [site] is the best startup reporting site!

        Cheers,
        Me

    Instead of saving this as a file somewhere and loading it, we\'ll
    just read this template from an open file in Emacs (buffer). Just as
    with the list of addresses.

    ``` Lisp
    (defun get-template-data (from-template-buffer)
      "Return the mail template from the template buffer as a string"
      (with-current-buffer (get-buffer from-template-buffer) (buffer-string)))
    ```

    Nothing new in this function, we get the contents of the buffer
    `from-template-buffer` and return it as a string.

    Another 2 minutes are over, now we have 7 minutes left.

3.  The main function

    Finally, we need a function that reads one line after the other, and
    composes and sends a mail.

    ``` Lisp
    (defvar subject "Awesome startup started!")

    (defun personalize ()
      (interactive "M\nEnter Mail Subject: ")

      (let ((text (get-template-data "template"))
             (dict (get-mail-data "data.el")))

        (loop for (key . value) in dict do
              (setq text (replace-regexp-in-string (format "\\[%s\\]" key) value text)))

        (kill-new text)

        (with-current-buffer (get-buffer "data.el") (forward-line))
        (compose-mail (cdr (assoc "email" dict)) subject)))
    ```

    -   `(defvar ...)` defines a global scope variable. We do this since
        we only want to set the contents of the subject once,
        specifically at the beginning.
    -   `let` defines variables, in this case `text` which contains our
        template, and `dict` which contains our address contents for the
        current line in the data. [^9]
    -   `(loop for (key . value) in dict do ...)` This is actually a
        function defined in an [Emacs extension called
        \'CL-Macs\',](http://www.gnu.org/software/emacs/manual/html_mono/cl.html)
        which is a set of definitions that extend Emacs with Common Lisp
        functionalities. It is a really good Emacs addition. It loops
        over the \'keys\' in our dictionary[^10] and lets us do
        something with them
    -   `(setq text (replace-regexp-in-string ...))` This line replaces
        the contents of the `text` variable during each iteration of the
        loop with an updated version where the key `[key]` is replaced
        with the actual value (i.e. `[email]` with
        `hogan@venturebeat.com`).[^11]
    -   `(kill-new text)` This particular expression adds the contents
        of the variable `text` to our clipboard. The clipboard in Emacs
        is called the \"kill ring\" and \"kill=new\" therefore creates a
        new entry on the \"kill ring\". As you may have guessed, the
        kill ring can have multiple entries, which makes it easy to
        store more than one value.
    -   `(with-current-buffer (get-buffer "data.el") (forward-line))`
        Simply forwards the current line in our data buffer by one since
        we\'ve now finished processing this line.
    -   `(compose-mail ....)` This is an Emacs function that sends opens
        a mail composition buffer for a specific email address and a
        subject.

    When we call the `personalize` function it will open a new buffer
    for us, that looks like this.

    ``` Text
    To: hogan@venturebeat.com
    Subject: Awesome startup started!
    From: Joe the Coder <coder1@awesome-startup.com>
    --text follows this line--
    ```

    But, where\'s the text? Well, we only added it to the clipboard, we
    do have to paste (yank, in Emacs parlance) it from there in order to
    insert it into this mail. This is done with the shortcut `ctrl-y`.

    Now we can send this mail with the shortcut `ctrl-c ctrl-c`

4.  Wait, that\'s it?

    This was a fun excercise, though in reality it would have been even
    faster to code this with the PHP mail function and read the data
    from two text files. However, the beauty of this solution is that it
    is deliberately interactive. Each mail is semi-automated meaning you
    can add custom personalizations before sending it. Also, the mail
    library in Emacs offers more functions like attaching files, signing
    messages[^12], sending messages at a later time and more.

    Now, some may wonder whether it is possible to do all this without
    any interactivity, i.e. sending the mail right away without even
    opening a buffer. Since almost everything in Emacs is written in
    Emacs Lisp (save for a base runtime in C), you can just look up the
    sourcecode of the required function and implement full bulk sending.
    In this case the functions in question are `compose-mail` and
    `message-send-and-exit`. When I say look up the sourcecode, I also
    wasn\'t talking about Google or Github, no simply hit `M-x`, type
    `find-function`, hit enter, and then the name of the function (i.e.
    `compose-mail`). Emacs will then open the required file at the
    correct position. However, this probably goes beyond our initial
    limit of 15minutes so our boss will have to repeatedly hit
    `ctrl-c ctrl-c` until all mails are through.

    So what does it look like in Emacs, when youre doing this, you may
    ask, here\'s a screenshot from my Emacs with the code loaded and
    running:

    [![](http://appventure.me/cimg/screenshot-bulk-mail-thumb.png)](http://appventure.me/cimg/screenshot-bulk-mail.png)

5.  Final Words

    This was more or less an excercise for the sake of excercise. Except
    for some rare situations I doubt there\'s much use in this. However,
    it worked well as an issue that had a confined problem space,
    operated with functionality outside of the realm of other editors
    (sending mail), and was short enough to use it as a simple example.

    Already in the first weeks of using Emacs, I wrote more code in
    Emacs Lisp than I ever wrote in Vimscript. I attribute this to three
    key factors.

    1.  **Ease of Evaluation** The ease with which one can evaluate code
        in any buffer (or in a special Emacs Lisp Repl)
    2.  **Text editing APIs** The functions for working with buffers,
        files, and texts have been honed over 30 years.
    3.  **Library and Search** A huge functionality library with great
        search. It is really easy to use fuzzy search terms to find a
        particular function, and then one can just have a look at the
        source, all from within the editor.

[^1]: [Evil is an Emacs
    extension](https://gitorious.org/evil/pages/Home) that adds Vim
    Keybindings to Emacs so that it can be controlled with the same
    shortcuts as Vim.

[^2]: The smart will point out that Vim also offers bindings to Python
    and Ruby, if it is compiled in such a way, so that one is not
    **required** to use Vimscript, however I always found the actual api
    for this very weird and hackish.

[^3]: Actually, I had already tried Emacs before, in late 2001 but back
    then it lacked good HTML/PHP support compared to my default editor
    at the time,
    [HomeSite](http://en.wikipedia.org/wiki/Macromedia_HomeSite)

[^4]: Of course, both Vim and Emacs offer such a function already, but I
    thought this would be simple as a demonstration

[^5]: I actually simplified it a little for this post, the original
    function made it even easier to create new fields but was more
    elaborate

[^6]: There\'re some who\'d rather call this disadvantages.

[^7]: Like executing a shell script and writing something into your
    calendar whenever a you receive a certain mail

[^8]: I\'ve actually had situations kinda like that

[^9]: data.el is the name of the buffer that contains the addresses.

[^10]: Actually it is not a dictionary but for the sake of simplicity I
    will ignore this here.

[^11]: This code example uses a lot of side effects, something which is
    usually frowned upon in functional programming and Lisp, however I
    decided to write the examples this way so they\'re easier to
    understand for novices.

[^12]: Something quickly gaining importance nowadays
