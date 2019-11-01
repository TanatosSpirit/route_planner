class MapObject:
    def __init__(self):
        self.name = ''
        self.vm_id = -1
        self.obj_id = -1

    def add_name(self, name):
        self.name = name

    def add_vm_id(self, vm_id):
        self.vm_id = vm_id

    def add_obj_id(self, obj_id):
        self.obj_id = obj_id
