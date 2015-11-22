class Virus(object):
    """docstring for Virus"""
    def __init__(self, seg1color, seg2color):
        super(Virus, self).__init__()
        self.seg1color = seg1color
        self.seg2color = seg2color
        self.infection_time = 0  # time of infection
        self.expiry_time = 5  # num. days to immunity
        
    def is_mixed(self):
        if self.seg1color != self.seg2color:
            return True
        else:
            return False