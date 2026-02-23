import re
import pandas as pd
from skills import SKILLS


# Flatten skill dictionary into a single list
ALL_SKILLS = sorted(
    {skill.lower() for category in SKILLS.values() for skill in category}
)


SECTION_PATTERNS = {
    "requirements": r"(requirements|what you'll need|qualifications|must have)",
    "preferred": r"(preferred|nice to have|bonus|good to have)"
}


def split_sections(text: str):
    """
    Splits job description into requirement and preferred sections.
    Returns dictionary with raw text segments.
    """
    lower = (text or "").lower()

    sections = {
        "requirements": "",
        "preferred": ""
    }

    req_match = re.search(SECTION_PATTERNS["requirements"], lower)
    pref_match = re.search(SECTION_PATTERNS["preferred"], lower)

    if req_match:
        sections["requirements"] = lower[req_match.start():]

    if pref_match:
        sections["preferred"] = lower[pref_match.start():]

    return sections


def estimate_level(section_text: str, skill: str):
    """
    Estimate required level based on context words near skill.
    Level scale: 1 (basic), 2 (intermediate), 3 (strong)
    """

    # Search small window around skill mention
    window_pattern = rf".{{0,40}}{re.escape(skill)}.{{0,40}}"
    matches = re.findall(window_pattern, section_text)

    for snippet in matches:
        if re.search(r"(expert|extensive|5\+ years|strong experience|advanced)", snippet):
            return 3
        elif re.search(r"(experience|proficient|solid|hands-on)", snippet):
            return 2
        elif re.search(r"(familiarity|exposure|basic|knowledge of)", snippet):
            return 1

    # Default level if found but no signal words
    return 2


def extract_structured_skills(text: str):
    """
    Extract structured required and preferred skills with estimated levels.
    """

    sections = split_sections(text)

    required = {}
    preferred = {}

    for skill in ALL_SKILLS:

        # Word boundary matching
        pattern = rf"\b{re.escape(skill)}\b"

        # Required section
        if sections["requirements"] and re.search(pattern, sections["requirements"]):
            level = estimate_level(sections["requirements"], skill)
            required[skill] = level

        # Preferred section
        if sections["preferred"] and re.search(pattern, sections["preferred"]):
            level = estimate_level(sections["preferred"], skill)
            preferred[skill] = level

    return required, preferred


def main():
    df = pd.read_csv("data/internships_raw.csv")

    structured_required = []
    structured_preferred = []

    for desc in df["description_raw"].fillna(""):

        required, preferred = extract_structured_skills(desc)

        structured_required.append(required)
        structured_preferred.append(preferred)

    df["required_skills"] = structured_required
    df["preferred_skills"] = structured_preferred

    df.to_csv("data/internships_structured.csv", index=False)

    print("Saved: data/internships_structured.csv")


if __name__ == "__main__":
    main()