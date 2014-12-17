#! /usr/bin/env python3 -Wall
import json
import sqlite3
import tornado.ioloop
import tornado.web

conn = sqlite3.connect('example.db')
c = conn.cursor()


def intidb():
    c.execute("CREATE TABLE albums (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, slug text)")
    c.execute("CREATE TABLE photos (id INTEGER PRIMARY KEY AUTOINCREMENT, album_id integer, name text, path text)")
    conn.commit()


class Photo:
    def __init__(self, file):
        self.path = ''

    def save(self):
        c.execute("INSERT INTO photos (name")

class Album:
    def __init__(self, name):
        self.id = None
        self.name = name

    @classmethod
    def get(cls, id):
        c.execute("SELECT * FROM albums WHERE id = ?", (id,))
        row = c.fetchone()
        album = Album(row[1])
        album.id = row[1]
        return album

    def save(self):
        if self.id:
            c.execute("UPDATE albums SET name = ? WHERE id = ?", (self.name, self.id,))
        else:
            c.execute("INSERT INTO albums (name) VALUES (?)", (self.name,))
            self.id = c.lastrowid

    def get_photos(self):
        photos = []
        c.execute("SELECT * FROM photos WHERE album_id = ?", (self.id,))
        for p in c.fetchall():
            photos.append(Photo(p))

        return photos

    def asdict(self):
        return {'id': self.id, 'name': self.name}

    def __str__(self):
        return self.name


class UploadHandler(tornado.web.RequestHandler):
    def post(self, album):
        for f in self.request.files['file']:
            photo = Photo(album_id=album)
            upload_dir = 'uploads/%d' % album
            import os
            try:
                os.mkdir(upload_dir)
                fpath = '%s/%s' % (upload_dir, f.filename,)
                fh = open(fpath, 'wb')
                fh.write(f.body)
                photo.save()
            except Exception, e:
                print e


class MainHandler(tornado.web.RequestHandler):
    def get(self, id=None):
        album = Album('New Album')
        albums = []
        c.execute('SELECT * FROM albums')

        for r in c.fetchall():
            album = Album(r[1])
            album.id = r[0]
            albums.append(album)
        
        self.render("templates/gallery-index.html", albums=albums, album=album)

    def post(self):
        data = self.request.body.decode('utf-8')
        data = json.loads(data)
        album = Album(data['name'])
        album.save()
        self.write(album.asdict())

    def put(self, id):
        data = self.request.body.decode('utf-8')
        data = json.loads(data)
        album = Album.get(id)
        album.name = data['name']
        album.save()


if __name__ == "__main__":
    #intidb()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/albums/", MainHandler),
        (r"/albums/(\d+)/", MainHandler),
        (r"/albums/(\d+)/", MainHandler),
        (r"/albums/(\d+)/upload/", UploadHandler),
    ], static_path="static", debug=True)

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    #db.generate_mapping(create_tables=True)
