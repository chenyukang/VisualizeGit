VisualizeGitProj
================

Visualize A Git Project, show developer's contribution and connections with components. Using Ubigraph for rendering.

# Usage
 1. ./gitstat.rb -o log.txt (run at the top directory, get the commits log output to log.txt)

 2. ./bin/ubigraph_server   (start the Ubigraph render server)

 3. ./gitshow.py log.txt    (render commit log)
