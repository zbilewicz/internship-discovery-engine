import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Internship Discovery Engine")

if "step" not in st.session_state:
    st.session_state.step = 1

# ----------------------------
# Location Data + Helpers
# ----------------------------

REGIONS = {
    "Europe": ["Netherlands", "Germany", "France", "Belgium", "Spain", "Italy"],
    "North America": ["United States", "Canada"],
    "Asia": ["Singapore", "Japan", "India"],
}

def toggle_no_preference():
    if st.session_state.get("no_location_preference", False):
        for region_name, countries in REGIONS.items():
            st.session_state[f"region_{region_name}"] = False
            for c in countries:
                st.session_state[f"{region_name}_{c}"] = False

def toggle_region(region_name, countries):
    region_key = f"region_{region_name}"
    new_val = st.session_state.get(region_key, False)

    if new_val:
        st.session_state["no_location_preference"] = False

    for c in countries:
        st.session_state[f"{region_name}_{c}"] = new_val

# -----------------------------------
# STEP 1 — EDUCATION & LOGISTICS
# -----------------------------------

if st.session_state.step == 1:

    st.header("Step 1 — Education & Logistics")

    university = st.text_input("University")
    major = st.text_input("Major")

    education_level = st.selectbox(
        "Education Level",
        ["Bachelor", "Master", "PhD"]
    )

    year_of_study = st.selectbox(
        "Year of Study",
        ["1st", "2nd", "3rd", "4th+", "Graduating"]
    )

    st.subheader("Internship Timing")

    current_year = datetime.now().year

    start_month = st.selectbox(
        "Preferred Start Month",
        ["January","February","March","April","May","June",
         "July","August","September","October","November","December"]
    )

    start_year = st.number_input(
        "Preferred Start Year",
        min_value=current_year,
        max_value=current_year + 5,
        value=current_year
    )

    duration = st.selectbox(
        "Preferred Duration",
        ["2–3 months", "4–6 months", "6+ months", "Flexible"]
    )

    # ----------------------------
    # LOCATION SECTION (RESTORED)
    # ----------------------------

    st.subheader("Location Preferences")

    st.checkbox(
        "Doesn't matter",
        key="no_location_preference",
        on_change=toggle_no_preference,
    )

    selected_countries = []

    for region_name, countries in REGIONS.items():

        st.checkbox(
            region_name,
            key=f"region_{region_name}",
            on_change=toggle_region,
            args=(region_name, countries),
        )

        for c in countries:
            cols = st.columns([0.08, 0.92])
            with cols[1]:
                st.checkbox(c, key=f"{region_name}_{c}")

            if st.session_state.get(f"{region_name}_{c}", False):
                selected_countries.append(c)

    remote_allowed = st.checkbox("Open to remote internships")

    if st.button("Next"):
        st.session_state.profile_step1 = {
            "university": university,
            "major": major,
            "education_level": education_level,
            "year_of_study": year_of_study,
            "start_date": f"{start_month} {start_year}",
            "duration": duration,
            "preferred_countries": selected_countries,
            "remote_allowed": remote_allowed
        }
        st.session_state.step = 2
        st.rerun()

# -----------------------------------
# STEP 2 — CV
# -----------------------------------

elif st.session_state.step == 2:

    st.header("Step 2 — CV")

    cv_text = st.text_area("Paste your CV text", height=250)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back"):
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button("Next"):
            st.session_state.profile_step2 = {
                "cv_text": cv_text
            }
            st.session_state.step = 3
            st.rerun()

# -----------------------------------
# STEP 3 — PREFERENCES
# -----------------------------------

elif st.session_state.step == 3:

    st.header("Step 3 — Preferences & Direction")

    # ----------------------------
    # Role interests (checkboxes)
    # ----------------------------
    st.subheader("Role Interests")

    role_type = []
    if st.checkbox("Machine Learning", key="role_ml"): role_type.append("Machine Learning")
    if st.checkbox("Data Engineering", key="role_de"): role_type.append("Data Engineering")
    if st.checkbox("Analytics / BI", key="role_an"): role_type.append("Analytics / BI")
    if st.checkbox("Backend Engineering", key="role_be"): role_type.append("Backend Engineering")
    if st.checkbox("Research", key="role_re"): role_type.append("Research")
    if st.checkbox("Startup Generalist", key="role_sg"): role_type.append("Startup Generalist")

    # ----------------------------
    # Company type (checkboxes)
    # ----------------------------
    st.subheader("Company Type Preference")

    company_type = []
    if st.checkbox("Big Tech (FAANG-style)", key="ct_bt"): company_type.append("Big Tech")
    if st.checkbox("Large Corporate", key="ct_lc"): company_type.append("Large Corporate")
    if st.checkbox("Scale-up", key="ct_su"): company_type.append("Scale-up")
    if st.checkbox("Startup", key="ct_st"): company_type.append("Startup")
    if st.checkbox("Research Lab", key="ct_rl"): company_type.append("Research Lab")
    if st.checkbox("No preference", key="ct_np"): company_type.append("No preference")

    # Optional: if "No preference" is checked, ignore others (MVP clean behavior)
    if "No preference" in company_type and len(company_type) > 1:
        st.warning("You selected 'No preference' plus other options. For matching, we'll treat this as 'No preference'.")

    # ----------------------------
    # Values (checkboxes)
    # ----------------------------
    st.subheader("What matters most to you?")

    values = []
    if st.checkbox("Impact-driven mission", key="v_impact"): values.append("Impact-driven mission")
    if st.checkbox("High salary", key="v_salary"): values.append("High salary")
    if st.checkbox("Learning & mentorship", key="v_learn"): values.append("Learning & mentorship")
    if st.checkbox("Prestige / brand", key="v_prestige"): values.append("Prestige / brand")
    if st.checkbox("Work-life balance", key="v_wlb"): values.append("Work-life balance")
    if st.checkbox("Cutting-edge tech", key="v_cutting"): values.append("Cutting-edge tech")
    if st.checkbox("Fast growth / ownership", key="v_growth"): values.append("Fast growth / ownership")

    # ----------------------------
    # Free text (for later AI)
    # ----------------------------
    st.subheader("Describe your dream internship")

    dream_job = st.text_area(
        "What would your ideal internship look like?",
        placeholder="e.g. I want to work on applied ML in an impact-driven company, with mentorship and ownership."
    )

    # ----------------------------
    # Navigation
    # ----------------------------
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back"):
            st.session_state.step = 2
            st.rerun()

    with col2:
        if st.button("Finish"):
            full_profile = {
                "step1": st.session_state.get("profile_step1"),
                "step2": st.session_state.get("profile_step2"),
                "step3": {
                    "role_type": role_type,
                    "company_type": company_type,
                    "values": values,
                    "dream_job": dream_job
                }
            }

            st.success("Profile Completed")
            st.json(full_profile)