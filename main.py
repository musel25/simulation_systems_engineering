import xml.etree.ElementTree as ET
import numpy as np

# Define the namespace dictionary
ns = {'edspn': 'http://pdv.cs.tu-berlin.de/TimeNET/schema/eDSPN'}

# Parse the XML file
tree = ET.parse('elevatorfinal.xml')
root = tree.getroot()

# Build mappings for places and transitions
places = {}
transitions = {}

# Extract places
for place in root.findall('edspn:place', ns):
    pid = place.get('id')
    places[pid] = len(places)

# Extract transitions (assuming immediateTransition is the type you want)
for trans in root.findall('edspn:immediateTransition', ns):
    tid = trans.get('id')
    transitions[tid] = len(transitions)

num_places = len(places)
num_transitions = len(transitions)

# Initialize pre and post matrices
pre_matrix = np.zeros((num_places, num_transitions), dtype=int)
post_matrix = np.zeros((num_places, num_transitions), dtype=int)

# Process arcs (for standard arcs; you may ignore inhibit arcs)
for arc in root.findall('edspn:arc', ns):
    source = arc.get('fromNode')
    target = arc.get('toNode')
    # Try to extract a numeric weight; if not possible, default to 1.
    try:
        weight = int(arc.get('weight'))
    except (ValueError, TypeError):
        weight = 1

    # Determine if the arc is a pre or post arc
    if source in places and target in transitions:
        # Arc from a place to a transition (pre-incidence)
        i = places[source]
        j = transitions[target]
        pre_matrix[i, j] += weight
    elif source in transitions and target in places:
        # Arc from a transition to a place (post-incidence)
        j = transitions[source]
        i = places[target]
        post_matrix[i, j] += weight

# Compute the net incidence matrix: C = post - pre
incidence_matrix = post_matrix - pre_matrix

print("Pre-incidence matrix (C^-):")
print(pre_matrix)
print("\nPost-incidence matrix (C^+):")
print(post_matrix)
print("\nNet Incidence matrix (C = C^+ - C^-):")
print(incidence_matrix)
