# Cocotoca

**Cocotoca is very alpha and probably broken!** Help would be most welcome in making it less broken.

An overzooming microservice.

Overzooming is when a tile is scaled and clipped to make a subsection of it into a tile at a higher zoom. For example, tile 0/0/0 is the whole world at zoom 0. The upper left quadrant of that, mainly containing North America, would be 1/0/0. If we clip the 0/0/0 tile, we will get an "overzoomed" 1/0/0 tile.

## Why?

This is not very useful for low-zoom tiles, since no new detail can be added by the overzooming process. However, it can be useful for making tiles which are beyond the maximum zoom supported by the tile service. Although the Mapzen tile service supports tiles at zoom > 16, there is no extra detail available beyond zoom 16. Therefore, instead of creating tiles, we can just overzoom the zoom 16 ones.

Since creating tiles can involve an expensive trip to the database, it can be more efficient to overzoom tiles which already exist. Also, it's easier to distribute tiles around to the edge of a network, whereas the database is unfortunately centralised. This can mean that overzoomed tiles are quicker to generate at the edge, and result in lower latency for the user.

What would be even lower latency is if the client were to perform the overzooming locally, on data it had already downloaded. [Tangram](https://github.com/tangrams/tangram) and [Tangram-ES](https://github.com/tangrams/tangram-es) already do this, so are awesome and efficient to build upon!

## Why "cocotoca"?

It means "it breaks up; it falls to pieces; cut to pieces", according to [freelang.net's Nahuatl dictionary](http://www.freelang.net/online/nahuatl.php?lg=gb), which seems appropriate for something that breaks up or cuts up tiles to make smaller tiles. It is sibling to [Tapalcatl](https://github.com/tilezen/tapalcatl), which serves metatiles, and [Xonacatl](https://github.com/tilezen/xonacatl), which serves layers. There's a bit of a theme going on now.

## Installing

Check out the code, and then run:

```
python setup.py test
python setup.py install
```

Note that you may want to set up a [virtualenv](https://virtualenv.pypa.io/en/stable/) environment so that you don't need to install as an administrator.
