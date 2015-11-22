from source.host import Host 
from source.virus import Virus
from random import choice, sample, random
from copy import deepcopy
# from scipy.stats import bernoulli
from collections import Counter, defaultdict

# import matplotlib.pyplot as plt

from time import time


def bernoulli(p):
    return int(random() > p)


start = time()

hosts = []
n_hosts = 5000
for i in range(n_hosts):
    if i < n_hosts / 2:
        hosts.append(Host(color='blue'))
    else:
        hosts.append(Host(color='red'))

# Pick 5 red hosts and 5 blue hosts at random, and infect it with a virus of the same color.
blue_hosts = [h for h in hosts if h.color == 'blue']
blue_hosts = sample(blue_hosts, 5)
blue_virus = Virus(seg1color='blue', seg2color='blue')
for h in blue_hosts:
    h.viruses.append(blue_virus)

red_hosts = [h for h in hosts if h.color == 'red']
red_hosts = sample(red_hosts, 5)
red_virus = Virus(seg1color='red', seg2color='red')
for h in red_hosts:
    h.viruses.append(red_virus)


p_immune = 1E-3   # 1 = always successful even under immune pressure
                  # 0 = always unsuccessful under immune pressure.
p_replicate = 0.95   # probability of replication given that a host is infected.
p_contact   = 1 - 1E-1/n_hosts  # probability of contacting a host of the same color.
p_same_color = 0.99   # probability of successful infection given segment of same color.
p_diff_color = 0.9    # probability of successful infection given segment of different color.
 
# Set up number of timesteps to run simulation
n_timesteps = 1000

# Set up a defaultdict for storing data
data = defaultdict(list)


# Run simulation
for t in range(n_timesteps):  
    # First part, clear up old infections.
    for h in hosts:
        h.increment_time()
        h.remove_old_viruses()
        h.remove_immune_viruses()
        
    # Step to replicate viruses present in hosts.
    infected_hosts = [h for h in hosts if h.is_infected()]
    for h in infected_hosts:
        if bernoulli(p_replicate): # we probabilistically allow replication to occur
            h.replicate_virus()
    
    # Step to transmit the viruses present in hosts.
    infected_hosts = [h for h in hosts if h.is_infected()]
    num_contacts = 0
    for h in infected_hosts:
        same_color = bernoulli(p_contact)
        if same_color:
            new_host = choice([h2 for h2 in hosts if h2.color == h.color])
            num_contacts += 0
        else:
            new_host = choice([h2 for h2 in hosts if h2.color != h.color])
            num_contacts += 1
        virus = h.viruses[-1] # choose the newly replicated virus every time.
        
        # Determine whether to transmit or not.
        p_transmit = 1
        ### First, check immunity ###
        if virus.seg1color in new_host.immunity:
            p_transmit = p_transmit * p_immune
        elif virus.seg1color not in new_host.immunity:
            pass
        
        ### Next, check seg1.
        if virus.seg1color == new_host.color:
            p_transmit = p_transmit * p_same_color
        else:
            p_transmit = p_transmit * p_diff_color
        
        ### Finally, check seg2.
        if virus.seg2color == new_host.color:
            p_transmit = p_transmit * p_same_color
        else:
            p_transmit = p_transmit * p_diff_color

        # Determine whether to transmit or not, by using a Bernoulli trial.
        transmit = bernoulli(p_transmit)
        
        # Perform transmission step
        if transmit:
            new_host.viruses.append(virus)
            # Capture data in the summary graph.
            # if virus.is_mixed():
                # G.edge[h.color][new_host.color]['mixed'] += 1
            # else:
                # G.edge[h.color][new_host.color]['clonal'] += 1
        else:
            pass
        
        
    ### INSPECT THE SYSTEM AND RECORD DATA###
    
    num_immunes = 0  # num immune hosts
    num_infected = 0  # num infected hosts
    num_blue_immune = 0  # num blue immune hosts
    num_red_immune = 0  # num red immune hosts
    num_uninfected = 0  # num uninfected hosts
    num_mixed = 0  # num mixed viruses
    num_original = 0  # num original colour viruses
    num_red_virus = 0  # num red viruses
    num_blue_virus = 0  # num blue viruses
    
    for h in hosts:
        if len(h.immunity) > 0:
            num_immunes += 1
        if h.is_infected() > 0:
            num_infected += 1
        if 'blue' in h.immunity:
            num_blue_immune += 1
        if 'red' in h.immunity:
            num_red_immune += 1
        if not h.is_infected():
            num_uninfected += 1
            
        for v in h.viruses:
            if v.is_mixed():
                num_mixed += 1
            else:
                if v.seg1color == 'blue' and v.seg2color == 'blue':
                    num_blue_virus += 1
                elif v.seg1color == 'red' and v.seg2color == 'red':
                    num_red_virus += 1
                num_original += 1
    
    # Record data that was captured
    data['n_immune'].append(num_immunes)
    data['n_infected'].append(num_infected)
    data['n_blue_immune'].append(num_blue_immune)
    data['n_red_immune'].append(num_red_immune)
    data['n_uninfected'].append(num_uninfected)
    data['n_mixed'].append(num_mixed)
    data['n_original'].append(num_original)
    data['n_red_virus'].append(num_red_virus)
    data['n_blue_virus'].append(num_blue_virus)
    data['n_contacts'].append(num_contacts)
    ### INSPECT THE SYSTEM ###


end = time()

print(end - start)
    