import streamlit as st
import json

# --- Load result from JSON file ---
try:
    with open("result.json") as f:
        result = json.load(f)
except FileNotFoundError:
    st.error("result.json not found. Please generate it from the notebook.")
    st.stop()

st.title("Client Insurance Profile")

# --- Client Profile ---
sections = result.get("sections", [])
if sections:
    with st.expander("Client Profile", expanded=True):
        section = sections[0]
        for k, v in section.items():
            st.write(f"**{k.replace('_',' ').title()}:** {v}")
else:
    st.write("No client profile data available.")

# --- Life Stages & Recommended Shield Plans ---
life_stages = result.get("life_stages", [])
shield_plans_data = result.get("shield_plan_recommendations", {})

# Handle nested dict structure
if isinstance(shield_plans_data, dict) and "ShieldPlanRecommendation" in shield_plans_data:
    plans = shield_plans_data["ShieldPlanRecommendation"]
elif isinstance(shield_plans_data, list):
    plans = shield_plans_data
else:
    plans = []

if life_stages:
    st.subheader("Life Stages & Recommended Shield Plans")
    for stage in life_stages:
        stage_name = stage.get("stage_name", "Unnamed Stage")
        age_range = stage.get("age_range", "N/A")
        features = stage.get("features", {})

        with st.expander(f"{stage_name} (Age Range: {age_range})"):
            if features:
                st.write("**Features:**")
                for fk, fv in features.items():
                    st.write(f"- {fk.replace('_',' ').title()}: {fv}")

            # tie shield plans to this stage
            plans = [p for p in plans if isinstance(p, dict)]

            stage_plans = [
                p for p in plans 
                if str(p.get("projected_life_stage", "")).lower() == stage_name.lower()
            ]
            if stage_plans:
                st.write("**Recommended Shield Plans:**")
                for plan in stage_plans:
                    plan_name = plan.get("plan_name", "Unnamed Plan")
                    with st.expander(plan_name):
                        st.write(f"**Reason:** {plan.get('reason', '')}")
                        st.write(f"**Hospital Class:** {plan.get('hospital_class', '')}")
                        st.write(f"**Annual Coverage Limit:** {plan.get('annual_coverage_limit', '')}")
                        st.write(f"**Panel Doctors:** {plan.get('panel_doctors', '')}")
                        st.write(f"**Waiting Time:** {plan.get('waiting_time', '')}")
                        st.write(f"**Access to Treatment:** {plan.get('access_to_treatment', '')}")
                        st.write(f"**Out of Pocket Cost:** {plan.get('out_of_pocket_cost', '')}")
                        st.write(f"**Suitable For:** {plan.get('suitable_for', '')}")
            else:
                st.write("_No recommended plans for this life stage._")
else:
    st.write("No life stages available.")

# --- Summary ---
summary = result.get("summary")
if summary:
    st.subheader("Summary")
    st.write(summary)
