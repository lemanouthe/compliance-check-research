def identify_relationships(current_requirement, all_requirements):
    related_requirements = []

    for requirement in all_requirements:
        if requirement != current_requirement:
            # Vous pouvez définir ici une logique pour évaluer la similarité entre les exigences
            # Par exemple, vous pouvez utiliser des techniques de traitement du langage naturel (NLP)
            # pour calculer la similarité entre les textes des exigences.
            # Dans cet exemple, nous considérons simplement que les exigences ayant le même type sont liées.
            if (
                requirement["requirement_type"]
                == current_requirement["requirement_type"]
            ):
                related_requirements.append(requirement["requirement_id"])

    return related_requirements
