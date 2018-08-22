# -----------------------
import unicodedata
# -----------------------

# ================
#   image class
# ================
class image_class():
    def __init__(self, filename, directory, id=0):
        self.filename = filename
        self.directory = directory
        self.id = id
        ##self.id = int(unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').split(".")[:-1][0])
