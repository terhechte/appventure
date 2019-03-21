import subprocess

# Terrible hack for migrating code
# Will extract fenced code (```) and try to compile it. 
# Will print the output if compilation fails

def run_swift(code):
    filename = "/tmp/tmpswift.swift"
    tempfile = open(filename, "w")
    tempfile.write(code)
    tempfile.close()
    try:
        output = subprocess.check_output("swiftc %s" % (filename,), shell=True, stderr=subprocess.STDOUT)
        return None
    except subprocess.CalledProcessError as e:
        return e.output

def parse_markdown(filename):
    blocks = []
    buffer = []
    begin = False
    for line in open(filename, "r").readlines():
        l = line.strip()
        if len(l) > 3 and l[0:3] == "```" and l.split(" ")[1].lower() == "swift":
            buffer = []
            begin = True
            continue
        if l == "```":
            begin = False
            blocks.append("\n".join(buffer))
            continue
        if begin == True:
            buffer.append(l)
    return blocks

collector = ""
for block in parse_markdown("posts/2016-07-15-swift3-nsdata-data.md"):
    op = run_swift(block)
    if op != None:
        collector += "#ERROR########################################\n"
        collector += block + "\n"
        collector += "---------------------------------------------\n"
        collector += op + "\n"
        collector += "\n"
print collector
