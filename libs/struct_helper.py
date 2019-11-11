class RelativeInfo:

    def __init__(self):
        self.node_id = 0
        self.wp_id = 0
        self.lane_id = 0
        self.nearest_wp = 0
        self.angle = 0


class VmMap:

    def __init__(self):
        self.graph = []
        self.lanes = []
        self.nodes = []
