# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import csv
import glob

from typing import NamedTuple, DefaultDict, Dict, List, Tuple
from collections import defaultdict, Counter
from pprint import pprint
# -

NUM_SENATORS = 100

Senator = NamedTuple('Senator', [('name', str), ('party', str), ('state', str)])
VoteValue = int
VoteHistory = Tuple[VoteValue, ...]

vote_value = {'Yea': 1, 'Nay': -1, 'Not Voting': 0} # type: Dict[str, VoteValue]

accumulated_record = defaultdict(list) # type: DefaultDict[Senator, List[VoteValue]]

# # Load votes

for filename in glob.glob('congress_data/*.csv'):    
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)
        vote_topic = next(reader)
        headers = next(reader)
        for person, state, distric, vote, name, party in reader:
            senator = Senator(name, party, state)
            accumulated_record[senator].append(vote_value[vote])

# # Transform the record into a plain dict that maps to tuple of votes

record = {senator: tuple(votes) for senator, votes in accumulated_record.items()}  # type: Dict[Senator, VoteHistory]

# # Use k-means to locate the cluster centroids, assign each senator to the nearest cluster

from kmeans import k_means, assign_data

centroids = k_means(record.values(), k=3)

clustered_votes = assign_data(centroids, record.values())

# # Build a reverse mapping from a vote history to a list of senators who voted that way

votes_to_senators = defaultdict(list)  # type: DefaultDict[VoteHistory, List[Senator]]

for senator, votehistory in record.items():
    votes_to_senators[votehistory].append(senator)

assert sum([len(cluster) for cluster in votes_to_senators.values()]) == NUM_SENATORS

# # Display the clusters and the members (senators) of each cluster

for i, votes_in_cluster in enumerate(clustered_votes.values(), start=1):
    print(f'----- Voting Cluster #{i} -----')
    party_totals = Counter()
    for votes in set(votes_in_cluster):
        for senator in votes_to_senators[votes]:
            print(senator)
            party_totals[senator.party] += 1
    print(party_totals)


