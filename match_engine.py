import pandas as pd
import ast
from user_profile import USER_PROFILE


def compute_match(row):
    raw_score = 0

    # Parse structured dictionaries safely
    required = (
        ast.literal_eval(row["required_skills"])
        if isinstance(row["required_skills"], str)
        else row["required_skills"]
    )

    preferred = (
        ast.literal_eval(row["preferred_skills"])
        if isinstance(row["preferred_skills"], str)
        else row["preferred_skills"]
    )

    user_skills = USER_PROFILE["skills"]
    location_prefs = USER_PROFILE["preferred_locations"]

    # --------------------------
    # 1️⃣ Required skill evaluation
    # --------------------------
    for skill, required_level in required.items():
        user_level = user_skills.get(skill, 0)

        if user_level >= required_level:
            raw_score += 4  # strong reward
        else:
            gap = required_level - user_level
            raw_score -= gap * 4  # strong penalty

    # --------------------------
    # 2️⃣ Preferred skill bonus
    # --------------------------
    for skill, preferred_level in preferred.items():
        user_level = user_skills.get(skill, 0)

        if user_level >= preferred_level:
            raw_score += 1  # smaller bonus

    # --------------------------
    # 3️⃣ Location bonus
    # --------------------------
    for pref in location_prefs:
        if pref.lower() in str(row["location"]).lower():
            raw_score += 2
            break

    return raw_score


def normalize_scores(df):
    min_score = df["raw_score"].min()
    max_score = df["raw_score"].max()

    if max_score == min_score:
        df["final_score"] = 50
    else:
        df["final_score"] = (
            (df["raw_score"] - min_score) / (max_score - min_score)
        ) * 100

    df["final_score"] = df["final_score"].round(2)

    return df


def main():
    df = pd.read_csv("data/internships_structured.csv")

    df["raw_score"] = df.apply(compute_match, axis=1)

    df = normalize_scores(df)

    df_sorted = df.sort_values(by="final_score", ascending=False)

    top = df_sorted.head(10)

    for _, row in top.iterrows():
        print(
            f"{row['company']} | {row['title']} | "
            f"{row['location']} | {row['final_score']}%"
        )

    df_sorted.to_csv("data/internships_ranked.csv", index=False)
    print("\nSaved: data/internships_ranked.csv")


if __name__ == "__main__":
    main()