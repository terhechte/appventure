import os
import re

# this is a terrible hack that converts `static` style org mode 
# documents with header to `techou` style markdown documents
# it requires pandoc

# later on, collect via fn
#entries = ["2016-02-02-hirundo-mac-app-swift-mailing-lists.org"]
#entries = ["2016-03-29-three-tips-for-clean-swift-code.org"]

entries = []
for l in os.listdir("."):
    if l[-4:] == ".org":
        entries.append(l)

def parse_lines(filename):
    parsed = {}
    output = ""
    done_head = False
    fp = open(filename, "r")
    for line in fp.readlines():
        if done_head:
            output = output + line
            continue
        if line[0:2] == "# ": continue
        if line[0:2] != "#+": 
            done_head = True
            continue
        (name, content) = line[2:].split(":", 1)
        parsed[name.strip()] = content.strip()
    return (output, parsed)

def make_front_matter(output, meta):
    def section_with_name(name, dct):
        fm = ["[%s]" % (name,)]
        for key in dct.keys():
            val = dct[key]
            if val == "true" or val == "false":
                fm.append("%s = %s" % (key, val))
            elif type(val) == type([]):
                fm.append("%s = [%s]" % (key, ", ".join(['"%s"' % s for s in val])))
            else:
                fm.append("%s = \"%s\"" % (key, val))
        return fm
    op = []
    op.extend(section_with_name("frontMatter", output))
    if len(meta) > 0:
        op.extend(section_with_name("meta", meta))
    return "\n".join(op)


for entry in entries:
    (content, head) = parse_lines(entry)
    output = {}
    meta = {}
    for key in head.keys():
        if key == "keywords": output[key] = head[key].split(" ")
        elif key == "tags": output[key] = head[key].split(" ")
        elif key == "summary": output[key] = head[key]
        elif key == "description": output[key] = head[key]
        elif key == "inactive": 
            if head[key] == "true":
                output["published"] = "false"
            else:
                output["published"] = "true"
        elif key == "title": output[key] = head[key]
        elif key == "OPTIONS": continue
        else: meta[key] = head[key]
    hs = output.has_key("summary")
    hd = output.has_key("description")
    if hs and hd:
        if len(output["summary"]) > len(output["description"]):
                output["description"] = output["summary"]
    elif hs:
        output["description"] = output["summary"]
    if output.has_key("summary"):
        del output["summary"]
    if not output.has_key("published"):
        output["published"] = "true"

    # try to figure out when this was created based on the file name
    (year, month, day, rest) = entry.split("-", 3)
    output["created"] = "%s-%s-%s" % (year, month, day)
    output["slug"] = entry.replace(".org", ".html")


    # next, strip the head and run through pandoc, write the output with the new front matter to a new file
    front_matter = make_front_matter(output, meta)
    front_matter += "\n---\n\n"

    fp = open("/tmp/grah.org", "w")
    fp.write(content)
    fp.close()
    os.system("/usr/local/bin/pandoc -s -o /tmp/mdgrah.md -i /tmp/grah.org")
    # pandoc makes h1 -> '---' and h2 -> '==='. I don't particularly like that, so lets write it back
    lines = []
    fp = open("/tmp/mdgrah.md", "r")
    last = ""
    for line in fp.readlines():
        if len(lines) > 0 and len(line) > 3 and re.match("^[\=]*\n$", line):
            lines[len(lines) - 1] = "# " + last
            continue
        if len(lines) > 0 and len(line) > 3 and re.match("^[\-]*\n$", line):
            lines[len(lines) - 1] = "## " + last
            continue
        lines.append(line)
        last = line
    mdcontent = "".join(lines)
    final = front_matter + mdcontent
    newname = entry.replace(".org", ".md")
    fp = open(newname, "w")
    fp.write(final)
    fp.close()

