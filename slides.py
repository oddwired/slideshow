import sys


class Photo:
    def __init__(self, id, orientation, tags):
        self.orientation = orientation
        self.id = id
        self.tags = tags


class Slide:
    def __init__(self, photos, previous=None, next=None):
        self.photos = photos
        self.previous = previous
        self.next = next

    def insert_left(self, slide):
        if self.previous is not None:
            self.previous.next = slide

        slide.previous = self.previous
        slide.next = self
        self.previous = slide

    def insert_right(self, slide):
        if self.next is not None:
            self.next.previous = slide

        slide.next = self.next
        slide.previous = self
        self.next = slide

    def get_tags(self):
        tags = []
        for i in self.photos:
            tags = list(set(tags + i.tags))

        return tags

    def add_slide(self, slide):
        if self.next is None:
            self.next = slide

        else:
            if len(list(set(self.get_tags() + slide.get_tags()))) > 0:
                if len(list(set(self.next.get_tags() + slide.get_tags()))) > 0:
                    self.insert_right(slide)
            else:
                self.next.add_slide(slide)


def create_slide(photo):
    return Slide(photo)


def read_file(file_name):
    with open(file_name) as f:
        N = f.readline().strip()
        root_slide = None

        ext_photo = None
        for i in range(int(N)):
            line = f.readline()
            id = i
            orientation = line.split()[0]
            tags = line.split()[1:]
            photo = Photo(id, orientation, tags)

            if root_slide is None:
                if orientation == 'V' and ext_photo is None:
                    ext_photo = photo
                elif orientation == 'V':
                    root_slide = create_slide([photo, ext_photo])
                    ext_photo = None
                else:
                    root_slide = create_slide([photo])
            else:
                if orientation == 'V' and ext_photo is None:
                    ext_photo = photo
                elif orientation == 'V':
                    root_slide.add_slide(create_slide([photo, ext_photo]))
                    ext_photo = None
                else:
                    root_slide.add_slide(create_slide([photo]))
        return root_slide

def write_file(file_name, root_slide):
    
if len(sys.argv) != 3:
    print("Usage: slides.py input_file output_file")
    print(len(sys.argv))
else:
    print(read_file(sys.argv[1]))