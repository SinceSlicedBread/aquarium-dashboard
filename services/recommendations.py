from model import Species
from compatibility import overall_score
def suggest_additions(tank_species, limit=10):

    candidates = Species.query.all()
    tank_ids = {fish.id for fish in tank_species}
    suggestions = []

    for candidate in candidates:
        if candidate.id in tank_ids:
            continue

        community = (tank_species + [candidate])
        score = overall_score(community)
        suggestions.append({
            "species": candidate,
            "score": score,
        })
    suggestions.sort(key=lambda x:x["score"], reverse=True)

    return suggestions[:limit]


def lowest_scoring_species(species_scores):

    lowest_id = min(species_scores, key=species_scores.get)

    return lowest_id


def suggest_replacements(tank_species, weakest_species_id, limit=10):

    base_community = [
        fish for fish in tank_species if fish.id != weakest_species_id
    ]

    candidates = Species.query.all()

    existing_ids = {
        fish.id for fish in base_community
    }

    suggestions = []

    for candidate in candidates:
        if candidate.id in existing_ids:
            continue

        community = (base_community + [candidate])
        score = overall_score(community)

        suggestions.append({
            "species": candidate,
            "score": score,
        })

    suggestions.sort(key=lambda x:x["score"], reverse=True)

    return suggestions[:limit]



