import pandas as pd
import networkx as nx
from itertools import combinations

# --- Phase 1: Artifacts ---
# Import the artifacts.py script.
# This will run the file, populating the 'all_metadata' list.
import Artifacts

# Access the all_metadata list from the artifacts module
df = pd.DataFrame(Artifacts.all_metadata)

print("--- Similarity Model ---")

# --- Step 1: Find Similarity Pockets (Sp) ---
# An Sp is a group of 2 or more artifacts sharing the
# same metadata field-value pair in the same source.

# Group by source, field, and value
grouped = df.groupby(['source_id', 'field', 'value'])

# Filter for groups that have more than one unique artifact
sp_groups = grouped.filter(lambda x: x['artifact_id'].nunique() > 1)

# 'sp_groups' is a DataFrame containing all metadata entries
# that are part of a Similarity Pocket.
sp_members = set(tuple(x) for x in sp_groups[
    ['source_id', 'artifact_id', 'field', 'value']
].values)

print(f"Found {len(sp_groups)} metadata entries in Similarity Pockets.")

# --- Step 2: Find Similarity Groups (Sg) ---
# An Sg is the largest union of Sp's, clustered by transitive closure.
# This is a graph problem: artifacts are nodes, sharing an Sp is an edge.

Sg_graph = nx.Graph()

# Get all artifacts that are in any Sp
sp_artifacts = sp_groups['artifact_id'].unique()
Sg_graph.add_nodes_from(sp_artifacts)

# For each Sp (each group of source/field/value),
# add edges between all artifacts in that group.
for (source, field, value), group_df in sp_groups.groupby(['source_id', 'field', 'value']):
    artifacts_in_sp = group_df['artifact_id'].unique()
    
    # Add edges between all pairs in this pocket
    for node1, node2 in combinations(artifacts_in_sp, 2):
        Sg_graph.add_edge(node1, node2)

# The connected components are the Similarity Groups
similarity_groups = list(nx.connected_components(Sg_graph))
print(f"Found {len(similarity_groups)} Similarity Groups (Sg).")


print("\n--- Unique Model ---")

# --- Step 1: Find Unique Pockets (UP) ---
# A UP accounts for all metadata pairs that FAILED the Sp condition.
# These are entries that are NOT in our 'sp_members' set.

# We can find the indices of the rows in 'sp_groups'
sp_indices = sp_groups.index

# Get all rows from the original 'df' that are NOT in 'sp_groups'
up_df = df.drop(sp_indices)

# 'up_df' now contains only Unique Pockets.
print(f"Found {len(up_df)} metadata entries in Unique Pockets (UP).")

# --- Step 2: Find Unique Groups (UG) ---
# A UG is the set of all UPs that belong to the
# same artifact ID within a source.

# We just need to group the 'up_df' by artifact_id
ug_groups = {}
for (artifact_id), group_df in up_df.groupby(['artifact_id']):
    # Store all unique (field, value) pairs for this artifact
    ug_groups[artifact_id] = set(
        tuple(x) for x in group_df[['field', 'value']].values
    )

print(f"Found {len(ug_groups)} Unique Groups (UG).")

# --- Step 3: Find Unique Associations (UA) ---
# This is the final step. A UA is the largest union of UGs 
# that have a sparse match, even across different fields.
#
# This means we connect two UGs (artifacts) if they share
# *any metadata VALUE*, even if the fields are different.

UA_graph = nx.Graph()
UA_graph.add_nodes_from(ug_groups.keys())

# Create a simple lookup dict of {artifact -> set(values)}
ug_values = {
    artifact: {val for (field, val) in fv_set}
    for artifact, fv_set in ug_groups.items()
}

# Iterate through all unique pairs of UGs
for ug1_id, ug2_id in combinations(ug_groups.keys(), 2):
    
    # Get their sets of unique values
    values1 = ug_values[ug1_id]
    values2 = ug_values[ug2_id]
    
    # Find the intersection
    sparse_matches = values1.intersection(values2)
    
    # Remove trivial matches (e.g., '<null>', '0', '', etc.)
    trivial_values = {'', '0', '<null>', 'None', 'n/a'}
    sparse_matches = sparse_matches - trivial_values
    
    # If there is at least one non-trivial sparse match,
    # they are associated.
    if len(sparse_matches) > 0:
        UA_graph.add_edge(ug1_id, ug2_id)
        # You could store the matches on the edge
        UA_graph.edges[ug1_id, ug2_id]['matches'] = sparse_matches

# The connected components are the Unique Associations
unique_associations = list(nx.connected_components(UA_graph))
print(f"Found {len(unique_associations)} Unique Associations (UA).")

# Now you can analyze 'unique_associations'
print("\nUnique Associations Found:")
for i, ua in enumerate(unique_associations):
    print(f"  UA Cluster {i+1}: {ua}")