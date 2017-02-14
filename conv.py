import json

inp = ""
with open("out.json") as out:
    inp = out.read()
print(inp)
js = json.loads(inp)

from lxml import etree

# create XML
root = etree.Element('gexf')
graph = etree.Element('graph', attrib={"mode":"static", "defaultedgetype":"directed"})
root.append(graph)
# another child with text
nodes = etree.Element('nodes')
edges = etree.Element('edges')

graph.append(nodes)
graph.append(edges)

idname = "url"
labeln = "title"
linkto = "linksto"

edgeid = 0

for n in js:
    print(n)
    nodes.append(etree.Element('node', attrib={"id":n[idname], "label":n[labeln] if n[labeln] else n[idname]}))
    for e in n[linkto]:
        edges.append(etree.Element("edge", attrib={"id":str(edgeid), "source":n[idname], "target":e}))
        edgeid += 1

# pretty string
s = etree.tostring(root, pretty_print=True)
print s

with open("out.gexf", "w+") as gexf:
    gexf.write(s)
