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
            #print(list(set(self.get_tags()).intersection(slide.get_tags())))
            if len(list(set(self.get_tags()).intersection(slide.get_tags()))) > 0:
                if len(list(set(self.next.get_tags()).intersection(slide.get_tags()))) > 0:
                    self.insert_right(slide)
            else:
                self.next.add_slide(slide)


class Category:
    def __init__(self):
        self.categories = {}

    def categorize_slide(self, slide):
        for tag in slide.get_tags():
            if tag in self.categories:
                self.categories[tag].append(slide)
            else:
                self.categories[tag] = [slide]


def add_slide(root_slide, slide):
    current_slide = root_slide

    while True:
        #print([x.id for x in current_slide.photos])
        if current_slide.next is None:
            current_slide.next = slide
            break
        else:
            if len(list(set(current_slide.get_tags()).intersection(slide.get_tags()))) > 0:
                if len(list(set(current_slide.next.get_tags()).intersection(slide.get_tags()))) > 0:
                    current_slide.insert_left(slide)

                    break

                current_slide = current_slide.next
            else:
                current_slide = current_slide.next
    return slide


def create_slide(photo):
    return Slide(photo)


def read_file(file_name):
    with open(file_name) as f:
        N = f.readline().strip()
        root_slide = None

        ext_photo = None
        last_added = None

        categories = Category
        for i in range(int(N)):
            line = f.readline()

            id = i
            orientation = line.split()[0]
            tags = line.split()[2:]
            #print(tags)
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
                    if last_added is not None:
                        last_added = add_slide(last_added, create_slide([photo, ext_photo]))
                    else:
                        last_added = add_slide(root_slide, create_slide([photo, ext_photo]))

                    ext_photo = None
                else:
                    if last_added is not None:
                        last_added = add_slide(last_added, create_slide([photo]))
                    else:
                        last_added = add_slide(root_slide, create_slide([photo]))

        return root_slide


def write_file(file_name, root_slide):
    count = 1
    current_slide = root_slide
    while True:
        if current_slide.next is not None:
            current_slide = current_slide.next
            count = count + 1
        else:
            break

    with open(file_name, "w+") as f:
        f.write("%s\n" % (str(count)))
        current_slide = root_slide
        while True:
            if len(current_slide.photos) > 1:
                f.write("%s %s\n" % (str(current_slide.photos[0].id), str(current_slide.photos[1].id)))
            else:
                f.write("%s\n" % (str(current_slide.photos[0].id)))
            if current_slide.next is not None:
                current_slide = current_slide.next
            else:
                break

if len(sys.argv) != 3:
    print("Usage: slides.py input_file output_file")

else:

    write_file(sys.argv[2], read_file(sys.argv[1]))
