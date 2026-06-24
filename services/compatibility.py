from itertools import combinations

def range_similarity(min1, max1, min2, max2):
    overlap = max(0, min(max1, max2) - max(min1, min2))
    union = max(max1, max2) - min(min1, min2)

    return overlap / union


def pairwise_compatibility(species, attribute):
    scores = []
    for a, b in combinations(species, 2):
        score = range_similarity(getattr(a, f"{attribute}_min"),
                                 getattr(a, f"{attribute}_max"),
                                 getattr(b, f"{attribute}_min"),
                                 getattr(b, f"{attribute}_max"))
        scores.append(score)

    if not scores:
        return 1.0

    return sum(scores) / len(scores)


def overall_score(species):
    temp = pairwise_compatibility(species, "temp")
    ph = pairwise_compatibility(species, "ph")
    gh = pairwise_compatibility(species, "gh")

    return round((temp + ph + gh) / 3 * 100, 1)


def species_scores(species, attribute):
    results = {}
    for fish in species:
        comparisons = []

        for other in species:
            if fish.id == other.id:
                continue

            score = range_similarity(getattr(fish, f"{attribute}_min"),
                                    getattr(fish, f"{attribute}_max"),
                                    getattr(other, f"{attribute}_min"),
                                    getattr(other, f"{attribute}_max"))
            comparisons.append(score)

        results[fish.id] = sum(comparisons) / len(comparisons)

    return results

def calculate_overlap(species_list, attribute):
    ## Attribute can be temp, ph or gh
    if not species_list:
        return None

    overlap_min = max(getattr(s, f"{attribute}_min") for s in species_list)
    overlap_max = min(getattr(s, f"{attribute}_max") for s in species_list)

    return {
        "min": overlap_min,
        "max": overlap_max,
        "compatible": overlap_min <= overlap_max
    }


def calculate_water_quality(species_list):
    if not species_list:
        return None

    #nitrite_max = min(s.nitrite_max for s in species_list)
    nitrate_max = min(s.nitrate_max for s in species_list)

    return {
        #"nitrite_max": nitrite_max,
        "nitrate_max": nitrate_max
    }

def compatibility_score(results):
    total = len(results)
    compatible = sum(1 for r in results.values() if r["compatible"])

    return round(compatible / total * 100)