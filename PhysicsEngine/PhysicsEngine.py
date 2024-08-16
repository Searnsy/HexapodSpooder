import itertools


class PhysicsEngine:
    def __init__(self, time_delta=0.1):
        self.objects = []
        self.time_delta = time_delta

    def add_object(self, obj):
        if obj not in self.objects:
            self.objects.append(obj)

    def check_collisions(self):
        for obj1, obj2 in itertools.combinations(self.objects, 2):
            obj1.check_collision(obj2)

    def step_time(self):
        for obj in self.objects:
            obj.step_time(self.time_delta)
        self.check_collisions()
