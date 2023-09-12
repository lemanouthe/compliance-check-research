import re

text = """
3.1. Support Services. The Contractor shall provide Program Management Support Services to
AFMRA/SG5 as described in the following paragraphs by task.
3.1.1. TASK I – EXECUTIVE ADMINISTRATIVE SUPPORT
The contractor shall provide one mid-senior level Executive Administrative Support to two
Government executives and approximately 40 personnel within the SG5 Capability Development
Division, located at Defense Health Headquarters (DHHQ), 7700 Arlington Blvd., Falls Church, VA.
3.1.1.1. Use office automation software, such as Microsoft Office, to create and edit documents,
presentations, graphics, tables, electronic drafts, and electronic mail. Update existing databases or
spreadsheets. Review, edit, and update documents to include checking for proper format, spelling,
grammar, capitalization, and punctuation. Prepare and submit documents in appropriate formats IAW
the latest Air Force Handbook (AFH) 33-337, The Tongue and Quill.
3.1.1.2. Receive telephone calls, greet, and prepare for visitors, and determine the nature of the calls
or visits; screen for requests that can be handled without assistance. Update and maintain office
procedures to ensure effective and efficient operations. Assist division personnel in locating and
selecting the appropriate guidelines, references, and procedures for application to specific taskings and
inquiries. Ensure correspondence and communication with returned calls, emails, and faxes are
promptly addressed within one (1) business day.
3.1.1.3. Manage division’s Temporary Duty (TDY) approval process. Coordinate and track all
division funded and cross organizational TDYs. Plan and coordinate travel arrangements for
executives within 24 hours of request in the Defense Travel System (DTS). Travel arrangements shall
include making reservations, scheduling transportation, securing protocol and area approvals,
prepare travel itineraries and prepare travel orders based on general travel intentions or known
preferences of the traveler IAW established travel regulations. All military and government civilian
travel must be IAW the Joint Travel Regulation (JTR ) for Department of Defense (DoD) Uniformed
Service members and Civilian Employees at:
http://www.defensetravel.dod.mil/Docs/perdiem/JTR.pdf.
"""

# Use regular expressions to find the requirements
pattern = r"(\d+\.\d+\.\d+\.\d+\.\s+(.*?)(?=\d+\.\d+\.\d+\.\d+\.|\Z))"
matches = re.findall(pattern, text, re.DOTALL)
# requirements = re.findall(pattern, text)

# Print the extracted requirements
for i, match in enumerate(matches, start=1):
    _, requirement = match
    sentences = re.split(r"(?<=[.!?]) +", requirement)
    print(f"Exigence {i}:")
    for sentence in sentences:
        print(f" - {sentence.strip()}")
    print()
    # print(f"{i}. {requirement.strip()}\n")
    # print(f"Requirement {i}: Section {section_number}, {requirement.strip()}\n")
    # print(f"Requirement {i}:")
    # print(f"Section Number: {section_number}")
    # print(f"Requirement Detail: {requirement.strip()}\n")
