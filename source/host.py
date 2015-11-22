from random import sample, choice
from source.virus import Virus

class Host(object):
    """docstring for Host"""
    def __init__(self, color):
        super(Host, self).__init__()
        self.color = color
        self.immunity = set()
        self.viruses = []
        self.expiry_time = 50
        self.alive_time = 0
        
    def is_infected(self):
        """
        Helper function to tell whether a host is infected or not.
        """
        if len(self.viruses) > 0:
            return True
        else:
            return False
    
    def has_coinfection(self):
        """
        Helper function to tell whether a host has a coinfection or not.
        """
        if len(self.viruses) > 1:
            return True
        else:
            return False
        
    def replicate_virus(self):
        """
        Command to replicate a virus that's present inside the host.
        
        If infected with only a single virus, then replicate that virus.
        
        If co-infected with two viruses, then randomly choose one 
        segment from each virus. Progeny may not necessarily be a 
        mixed virus.
        """
        if not self.has_coinfection():
            virus = choice(self.viruses)
            seg1, seg2 = virus.seg1color, virus.seg2color
            new_virus = Virus(seg1, seg2)
            
        elif self.has_coinfection():
            # Perform reassortment
            v1, v2 = sample(self.viruses, 2)

            seg1 = choice([v1.seg1color, v2.seg1color])
            seg2 = choice([v1.seg2color, v2.seg2color])

            new_virus = Virus(seg1, seg2)
        
        self.viruses.append(new_virus)
        
    def increment_time(self):
        """
        Command for incrementing the infection time of each virus in the
        host. Should be called upon each time step increase.
        """
        for v in self.viruses:
            v.infection_time += 1
            
            if v.infection_time > v.expiry_time:
                self.immunity.add(v.seg1color)
        self.alive_time += 1
        
    def remove_old_viruses(self):
        """
        Command to remove old viruses. Should be called upon each time
        step increase. 
        """
        for v in self.viruses:
            if v.infection_time > v.expiry_time:
                self.viruses.remove(v)
    
    def remove_immune_viruses(self):
        """
        Command to remove viruses for which the host has immunity
        against. Should be called upon each time step increase.
        Immunity is determined by the list of colors in the
        self.immunity attribute that match with segment 1 of a virus.
        """
        for v in self.viruses:
            if v.seg1color in self.immunity:
                self.viruses.remove(v)