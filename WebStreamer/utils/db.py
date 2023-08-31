from sqlitedict import SqliteDict

class Video():
    def __init__(self, name, url, tags) -> None:
        self.name = name
        self.url = url
        self.tags = tags

    def to_dict(self):
        return {"name": self.name, "url": self.url, "tags": self.tags}


class VideoDB():
    def __init__(self) -> None:
        self.db = SqliteDict(filename="db.sqlite", autocommit=True, outer_stack=False)

    def add_video(self, id, name, url, tags=None):
        self.db[id] = Video(str(name), str(url), tags)

    def get_video_by_tag(self, tag):
        return filter(lambda video: tag in video[1].tags, self.db.itervalues())

    def get_videos(self):
        return [video.to_dict() for video in self.db.values()]
