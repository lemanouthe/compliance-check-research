import os
import json
from src import (
    extract_requirements_from_text_file,
    is_requirement,
    get_confidence_factor,
    get_requirement_type,
    get_requirement_domain,
    get_rfp_domain,
    identify_relationships,
)


def main():
    # directory_path = '/Users/mamoutou.doumbia/Desktop/ComplianceCheck/research/data'
    # supported_file_extensions = ['.txt']
    extracted_requirements_list = []

    file_path = "/Users/mamoutou.doumbia/Desktop/ComplianceCheck/research/data/texteN3.txt"  # Remplacez par le chemin vers votre fichier
    filename = os.path.basename(file_path)
    # for filename in os.listdir(directory_path):
    #     if any(filename.endswith(ext) for ext in supported_file_extensions):
    #         file_path = os.path.join(directory_path, filename)
    requirements = extract_requirements_from_text_file(file_path)

    all_requirements_data = []

    for req in requirements:
        # Créez un dictionnaire représentant une exigence
        if is_requirement(req):
            # print(req)
            requirement_data = {
                "requirement_id": len(extracted_requirements_list) + 1,
                "original_RFP_context": filename,
                "extracted_requirements": req.strip(),
                "requirement_type": get_requirement_type(req),
                "RFP_domain": get_rfp_domain(req),
                "requirement_domain": get_requirement_domain(req),
                "confidence_factor": get_confidence_factor(req),
                "relationships": [],
            }
            extracted_requirements_list.append(requirement_data)

            # Identifier les exigences liées à la demande actuelle
            requirement_data["relationships"] = identify_relationships(
                requirement_data, all_requirements_data
            )

            # Ajouter les données d'exigence à la liste de toutes les exigences
            all_requirements_data.append(requirement_data)

    # Convertissez la liste en JSON et enregistrez-la dans un fichier
    with open("extracted_requirements.json", "w") as json_file:
        json.dump(extracted_requirements_list, json_file, indent=4)


if __name__ == "__main__":
    main()
