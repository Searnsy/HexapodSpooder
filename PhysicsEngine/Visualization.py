
class Visualization:
    def __init__(self):
        self.objects = []
        self.frame

    def add_object(self, obj):
        self.objects.append(obj)

    def draw_frame(self):
        for obj in self.objects:
            obj.draw()
