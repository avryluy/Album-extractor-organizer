source = r"C:\Users\avryl\Desktop\Music_Zips"
dest = "C:\\Users"


# OBJECTS
class albumExtractor:
    def __init__(self, source_dir, dest_dir):
        self.source_dir = source_dir
        self.dest_dir = dest_dir

    def __str__(self):
        print(f"Source: {self.source_dir}\nDestination: {self.dest_dir}")


class Album:
    def __init__(self, album_path, artist_name, album_name):
        self.album_path = album_path
        self.album_name = album_name
        self.artist_name = artist_name
        self.tracks = []

    def add_tracks(self, *tracks):
        for track in tracks:
            track.album = self
            self.tracks.append(track)

    # def __str__(self):
    #     print(f"Album Data: {self.album_name}, {self.artist_name}, {self.artist_name}")

    def __repr__(self):
        return f"Album({self.album_name}, {self.artist_name})"


class Track:
    def __init__(self, track_name):
        self.track_name = track_name

    def __str__(self):
        print(f"Parent Album Info: {self.album_name}")
        print(f"Track Info: {self.track_name}")

    def __repr__(self):
        return f"Track({self.track_name})"


# MAIN()
# a = albumExtractor(source, dest)

album1 = Album(source, "Avry Luy", "My Album")
track1 = Track("My Track")

album1.add_tracks(track1)

print(album1)
print(album1.tracks)
