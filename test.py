from pug4py.pug import Pug

pug = Pug("pug")
rendered_html = pug.render("example.pug")
with open("index.html", "w") as f:
    f.write(rendered_html)