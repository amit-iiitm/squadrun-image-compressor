import urllib2
import Image
import cStringIO

imgdata = urllib2.urlopen("https://media0.giphy.com/media/3oKIPo7VdVtho7deRG/giphy.gif").read()
img = Image.open(cStringIO.StringIO(imgdata))
img.save("goog.gif")
