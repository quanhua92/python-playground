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

from pprint import pprint
from typing import *

from functools import partial
from collections import defaultdict
from math import fsum, sqrt
from random import sample

Point = Tuple[int, ...]
Centroid = Point


def mean(data: Iterable[float]) -> float:
    'Accurate arithmetic mean'
    data = list(data)
    return fsum(data) / len(data)


# fsum, sqrt, zip as arguments so that can be loaded locally in the function -> faster than load globally. 
#
# Use ```from dis import dis; dis(dist);``` to see local/global

def dist(p: Point, q: Point, fsum=fsum, sqrt=sqrt, zip=zip) -> float:
    'Euclidean distance function for multi-dimensional data'
    return sqrt(fsum([(x - y) ** 2 for x, y in zip(p, q)]))


def assign_data(centroids: Sequence[Point], data: Iterable[Point]) -> Dict[Centroid, List[Point]]:
    'Group the data points to the closest centroid'
    d = defaultdict(list)
    for point in data:
        closest_centroid = min(centroids, key=partial(dist, point))
        d[closest_centroid].append(point)
    return dict(d)


def transpose(data):
    return list(zip(*data))


def compute_centroids(groups: Iterable[Sequence[Point]]) -> List[Centroid]:
    'Compute the centroid of each group'
    return [tuple(map(mean, transpose(group))) for group in groups]


def k_means(data: Iterable[Point], k: int=2, iterations: int=50) -> List[Centroid]:
    data = list(data)
    centroids = sample(data, k)
    for i in range(iterations):
        labeled = assign_data(centroids, data)
        centroids = compute_centroids(labeled.values())
    return centroids


if __name__ == "__main__":
    points = [
        (10, 41, 23),
        (22, 30, 29),
        (11, 42, 5),
        (20, 32, 4),
        (12, 40, 12),
        (21, 36, 23),
    ]

    centroids = k_means(points, k=3)

    d = assign_data(centroids, points)
    
    pprint(d, width=50)
