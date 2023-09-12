# import spacy

# class RequirementCategorizer:
#     def __init__(self):
#         self.nlp = spacy.load("en_core_web_sm")
#         self.categories = {
#             "Functional Requirements": ["behavior", "functionality", "capabilities", "create"],
#             "Non-Functional Requirements": ["qualities", "characteristics", "constraints"],
#             "Business Requirements": ["goals", "objectives", "improvements"],
#             "User Requirements": ["users' needs", "expectations", "behaviors"],
#             "System Requirements": ["technical specifications", "constraints"],
#             "Design Requirements": ["design constraints", "guidelines"],
#             "Regulatory or Compliance Requirements": ["regulations", "compliance"],
#             "Quality Assurance Requirements": ["quality assurance", "testing"],
#             "Performance Requirements": ["performance characteristics", "response time"],
#             "Interface Requirements": ["interactions", "data exchange"],
#             "Security Requirements": ["security needs"]
#         }

#     def categorize(self, requirement):
#         doc = self.nlp(requirement)
#         ent_labels = [ent.label_ for ent in doc.ents]

#         for category, keywords in self.categories.items():
#             # if any(keyword in requirement_tokens for keyword in keywords):
#             #     print(category)
#             #     return category
#             if any(keyword in requirement for keyword in keywords):
#                 return category
#         return "Uncategorized"


# Exemples d'exigences
# requirements = [
#     "Use office automation software such as Microsoft Office to create and edit documents presentations graphics tables electronic drafts and electronic mail",
#     "Ensure that the system responds within 2 seconds for user requests",
#     "Comply with data privacy regulations and protect user information"
# ]

# categorizer = RequirementCategorizer()

# for requirement in requirements:
#     category = categorizer.categorize(requirement)
#     print(f"Exigence: {requirement}")
#     print(f"Catégorie: {category}\n")


def get_requirement_type(sentence):
    sentence_lower = sentence.lower()
    functional_keywords = ["shall", "must", "should", "have to", "need to"]
    non_functional_keywords = [
        "performance",
        "security",
        "reliability",
        "usability",
        "scalability",
        "maintainability",
        "availability",
    ]
    business_keywords = ["goal", "objective", "strategic", "improvement", "initiative"]
    user_keywords = ["user", "stakeholder", "experience"]
    system_keywords = [
        "hardware",
        "software",
        "network",
        "infrastructure",
        "compatibility",
        "integration",
        "deployment",
    ]
    design_keywords = ["architectural", "interface", "database", "coding"]
    regulatory_keywords = [
        "legal",
        "industry",
        "government",
        "data protection",
        "privacy",
    ]
    quality_keywords = [
        "testing",
        "verification",
        "validation",
        "documentation",
        "change management",
        "version control",
    ]
    performance_keywords = [
        "performance",
        "response time",
        "throughput",
        "resource utilization",
        "capacity",
    ]
    interface_keywords = [
        "interaction",
        "data exchange",
        "external entities",
        "protocols",
        "formats",
        "API",
    ]
    security_keywords = ["security", "government"]

    if any(keyword in sentence_lower for keyword in functional_keywords):
        return "Functional Requirements"
    elif any(keyword in sentence_lower for keyword in non_functional_keywords):
        return "Non-Functional Requirements"
    elif any(keyword in sentence_lower for keyword in business_keywords):
        return "Business Requirements"
    elif any(keyword in sentence_lower for keyword in user_keywords):
        return "User Requirements"
    elif any(keyword in sentence_lower for keyword in system_keywords):
        return "System Requirements"
    elif any(keyword in sentence_lower for keyword in design_keywords):
        return "Design Requirements"
    elif any(keyword in sentence_lower for keyword in regulatory_keywords):
        return "Regulatory or Compliance Requirements"
    elif any(keyword in sentence_lower for keyword in quality_keywords):
        return "Quality Assurance Requirements"
    elif any(keyword in sentence_lower for keyword in performance_keywords):
        return "Performance Requirements"
    elif any(keyword in sentence_lower for keyword in interface_keywords):
        return "Interface Requirements"
    elif any(keyword in sentence_lower for keyword in security_keywords):
        return "Security Requirements"
    else:
        return "Other"
