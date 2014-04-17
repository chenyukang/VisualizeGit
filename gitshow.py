#!/usr/bin/env python
import xmlrpclib
import sys
import time

# Create an object to represent our server.
server_url = 'http://127.0.0.1:20738/RPC2'
server = xmlrpclib.Server(server_url)
G = server.ubigraph

user_color   = "#50ff50"
comp_color   = "#FFDB25"
NodeList = {}
EdgeList = set()


#G.set_edge_attribute(e1, "arrow", "true")

tinyred = G.new_vertex_style(0)
greenedge = G.new_edge_style(0)

def getNode(name, type):
    if NodeList.has_key(name):
        return NodeList[name]
    else:
        new_node = G.new_vertex()
        if type == "user":
            node_color = user_color
            font_color = "#ffff00"
        else:
            node_color = comp_color
            font_color = "#ff0000"

        G.set_vertex_attribute(new_node, "color", node_color)
        G.set_vertex_attribute(new_node, "label", name)
        G.set_vertex_attribute(new_node, "fontsize", "20")
        G.set_vertex_attribute(new_node, "fontcolor", font_color)
        NodeList.update({name : new_node})
        return new_node


def ShowLog(logName):
    CompSize = {}
    CompAllSize = {}
    UserSize = {}
    UserAllSize = {}
    Allchange = 0
    Allcompchange = 0

    G.clear()
    G.set_edge_style_attribute(0, "strength", "20.0")
    G.set_edge_style_attribute(0, "spline", "true")
    G.set_edge_style_attribute(0, "stroke", "dotted");

    with open(logName, "r") as fp:
        lines = fp.readlines()
        for line in lines:
            line = line.replace("\n", "")
            elems = line.split("\t")
            comp = elems[4]
            user = elems[0]
            add, sub = int(elems[2]), int(elems[3])
            if CompAllSize.has_key(comp):
                CompAllSize[comp] = CompAllSize[comp] + add + sub
            else:
                CompAllSize[comp] = add + sub
            if UserAllSize.has_key(user):
                UserAllSize[user] = UserAllSize[user] + add + sub
            else:
                UserAllSize[user] = add + sub

            Allchange = Allchange + add + sub
            Allcompchange = Allcompchange + add + sub

    with open(logName, "r") as fp:
        lines = fp.readlines()
        print len(lines)
        length = len(lines)
        num = 0
        for line in lines:
            line = line.replace("\n", "")
            elems = line.split("\t")
            user, comp = elems[0], elems[4]
            add, sub = int(elems[2]), int(elems[3])
            if CompSize.has_key(comp):
                CompSize[comp] = CompSize[comp] + add + sub
            else:
                CompSize[comp] = add + sub

            if UserSize.has_key(user):
                UserSize[user] = UserSize[user] + add + sub
            else:
                UserSize[user] = add + sub

            node1 = getNode(user, "user")
            node2 = getNode(comp, "comp")
            edge = (node1, node2)

            size = CompSize[comp]
            usersize = UserSize[user]
            e = G.new_edge(node1, node2)
            #G.set_edge_attribute(e, "arrow", "true")
            #G.set_edge_attribute(e, "showtrain", "true")
            G.set_vertex_attribute(node2, "size", str(2+ 10.0*float(size) / float(Allcompchange)))
            G.set_vertex_attribute(node1, "size", str(1+ 6.0*float(usersize) / float(Allchange)))
            G.set_vertex_attribute(node2, "shape", "dodecahedron")
            G.set_vertex_attribute(node1, "shape", "sphere")

            EdgeList.add(edge)
            G.set_vertex_attribute(node1, "color", "#ff0000")
            time.sleep(0.2)
            G.set_vertex_attribute(node1, "color", user_color)
            num = num + 1
            if num % 100 == 0:
                print num, length
                print "%.2f"%(float(num) / float(length))


def usage():
    print """gitshow.py: render git commit log
./gitshow.py <logfile> """
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    elif sys.argv[1] == "-h" or sys.argv[1] == "-help":
        usage()
    else:
        logfile = sys.argv[1]
        ShowLog(logfile)
