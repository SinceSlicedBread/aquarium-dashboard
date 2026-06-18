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