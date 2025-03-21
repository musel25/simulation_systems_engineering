import xml.etree.ElementTree as ET
import numpy as np

# Parse the EDSPN XML file
tree = ET.parse('your_file.edspn')
root = tree.getroot()

# Create mappings for places and transitions
places = {}
transitions = {}

# Adjust the tag names based on your EDSPN file structure
for place in root.findall('.//place'):
    place_id = place.get('id')
    places[place_id] = len(places)

for transition in root.findall('.//transition'):
    trans_id = transition.get('id')
    transitions[trans_id] = len(transitions)

# Initialize pre and post matrices
num_places = len(places)
num_transitions = len(transitions)
pre_matrix = np.zeros((num_places, num_transitions), dtype=int)
post_matrix = np.zeros((num_places, num_transitions), dtype=int)

# Process arcs (adjust tag names and attribute names as needed)
for arc in root.findall('.//arc'):
    source = arc.get('source')
    target = arc.get('target')
    # Assume weight attribute exists; default to 1 if not
    weight = int(arc.get('weight', '1'))

    # Check if arc is from a place to a transition (pre arc)
    if source in places and target in transitions:
        i = places[source]
        j = transitions[target]
        pre_matrix[i, j] += weight
    # Check if arc is from a transition to a place (post arc)
    elif source in transitions and target in places:
        j = transitions[source]
        i = places[target]
        post_matrix[i, j] += weight

# Compute the net incidence matrix: C = post - pre
incidence_matrix = post_matrix - pre_matrix

# Display the matrices
print("Pre-incidence matrix (C^-):")
print(pre_matrix)
print("\nPost-incidence matrix (C^+):")
print(post_matrix)
print("\nNet Incidence matrix (C = C^+ - C^-):")
print(incidence_matrix)
