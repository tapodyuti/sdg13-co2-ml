# app_vision.py

import streamlit as st
from PIL import Image
from detector import detect_from_multiple
from assembler import assemble_home_inventory, get_total_inventory
from calculator import get_full_report
from suggestions import generate_suggestions
from config import ROOM_TYPES, APPLIANCE_POWER

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="SDG-13 Home Carbon Estimator",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 SDG-13 Home Carbon & Bill Estimator")
st.markdown("**Upload photos of each room → AI detects appliances → Get CO₂ + Bill estimate**")
st.divider()

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
if "room_inventories" not in st.session_state:
    st.session_state.room_inventories = {}

if "report_ready" not in st.session_state:
    st.session_state.report_ready = False

# ─────────────────────────────────────────
# STEP 1: UPLOAD PHOTOS PER ROOM
# ─────────────────────────────────────────
st.header("📸 Step 1: Upload Room Photos")
st.info("You can upload multiple photos per room. AI will combine all detections.")

for room in ROOM_TYPES:
    with st.expander(f"📷 {room}", expanded=False):
        uploaded_files = st.file_uploader(
            f"Upload photos of {room} (select multiple)",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key=f"uploader_{room}"
        )

        if uploaded_files:
            # Show thumbnails
            cols = st.columns(min(len(uploaded_files), 4))
            images = []
            for i, file in enumerate(uploaded_files):
                img = Image.open(file).convert("RGB")
                images.append(img)
                with cols[i % 4]:
                    st.image(img, caption=f"Photo {i+1}", width=200)

            # Manual plug count input
            plug_count = st.number_input(
                f"🔌 How many plug points/outlets visible in {room}?",
                min_value=0,
                max_value=20,
                value=0,
                step=1,
                key=f"plugs_{room}"
            )

            # Detect button per room
            if st.button(f"🔍 Detect Appliances in {room}", key=f"detect_{room}"):
                with st.spinner(f"Analysing {len(images)} photo(s) of {room}..."):
                    detected = detect_from_multiple(images)

                # Add manual plug count
                if plug_count > 0:
                    detected["plug_point"] = plug_count

                if detected:
                    st.session_state.room_inventories[room] = detected
                    st.success(f"✅ Detected in {room}:")
                    for appliance, count in detected.items():
                        label = APPLIANCE_POWER.get(
                            appliance, {}
                        ).get("label", appliance)
                        st.write(f"   • {count} × {label}")
                else:
                    st.warning(
                        f"⚠️ No appliances auto-detected in {room}. "
                        f"Use Step 2 below to add manually."
                    )
                    st.session_state.room_inventories[room] = {}

                # Save plug count regardless
                if plug_count > 0:
                    st.session_state.room_inventories.setdefault(room, {})
                    st.session_state.room_inventories[room]["plug_point"] = plug_count


st.divider()

# ─────────────────────────────────────────
# STEP 2: MANUAL OVERRIDE
# ─────────────────────────────────────────
st.header("✏️ Step 2: Review & Adjust (Optional)")
st.info("Didn't detect something? Add or correct appliances manually.")

for room in ROOM_TYPES:
    if room in st.session_state.room_inventories:
        with st.expander(f"Edit {room} inventory", expanded=False):
            inventory = st.session_state.room_inventories[room]

            for appliance_key, data in APPLIANCE_POWER.items():
                current = inventory.get(appliance_key, 0)
                new_val = st.number_input(
                    f"{data['label']}",
                    min_value=0,
                    max_value=10,
                    value=current,
                    key=f"manual_{room}_{appliance_key}"
                )
                if new_val > 0:
                    st.session_state.room_inventories[room][appliance_key] = new_val
                elif appliance_key in st.session_state.room_inventories[room]:
                    del st.session_state.room_inventories[room][appliance_key]

st.divider()

# ─────────────────────────────────────────
# STEP 3: GENERATE REPORT
# ─────────────────────────────────────────
st.header("📊 Step 3: Generate Report")

if st.button("🚀 Generate Full Report", type="primary"):
    if not st.session_state.room_inventories:
        st.error("❌ Please upload and detect appliances in at least one room first.")
    else:
        with st.spinner("Generating your carbon report..."):

            # Assemble and deduplicate
            assembled = assemble_home_inventory(
                st.session_state.room_inventories
            )
            total_inventory = get_total_inventory(assembled)
            report = get_full_report(assembled)
            totals = report["__totals__"]
            suggestions = generate_suggestions(
                total_inventory,
                totals["total_kwh"]
            )

        st.divider()
        st.header("🏠 Your Home Carbon Report")

        # ── TOTALS ───────────────────────────────────
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="⚡ Monthly Consumption",
                value=f"{totals['total_kwh']} kWh"
            )

        with col2:
            st.metric(
                label="💰 Estimated Bill",
                value=f"₹{totals['total_bill']}"
            )

        with col3:
            st.metric(
                label="🌍 CO₂ Emitted",
                value=f"{totals['total_co2']} kg"
            )

        st.divider()

        # ── ROOM BREAKDOWN ───────────────────────────
        st.subheader("🏘️ Room-wise Breakdown")

        for room, data in report.items():
            if room == "__totals__":
                continue

            if not data["inventory"]:
                continue

            with st.expander(f"🚪 {room} — {data['total_kwh']} kWh | ₹{data['bill']} | {data['total_co2']} kg CO₂"):

                # Appliance table
                rows = []
                for appliance, info in data["breakdown"].items():
                    label = APPLIANCE_POWER.get(
                        appliance, {}
                    ).get("label", appliance)
                    rows.append({
                        "Appliance": label,
                        "Count": info["count"],
                        "Monthly kWh": info["kwh"],
                        "CO₂ (kg)": info["co2"],
                    })

                import pandas as pd
                if rows:
                    df = pd.DataFrame(rows)
                    st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()

        # ── SUGGESTIONS ──────────────────────────────
        st.subheader("💡 Personalised Reduction Suggestions")
        st.markdown("Follow these steps to **reduce your emissions and save money:**")

        total_potential_kwh  = min(sum(s["kwh_saved"]  for s in suggestions), totals["total_kwh"] * 0.80)
        total_potential_co2  = min(sum(s["co2_saved"]  for s in suggestions), totals["total_co2"] * 0.80)
        total_potential_bill = min(sum(s["bill_saved"] for s in suggestions), totals["total_bill"] * 0.80)




        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("⚡ Potential kWh Saving",  f"{round(total_potential_kwh, 1)} kWh/month")
        sc2.metric("💰 Potential Bill Saving",  f"₹{round(total_potential_bill, 1)}/month")
        sc3.metric("🌍 Potential CO₂ Saving",   f"{round(total_potential_co2, 1)} kg/month")

        st.markdown("")

        for i, s in enumerate(suggestions, 1):
            with st.expander(
                f"{s['icon']} {s['priority']} — {s['action']}"
            ):
                st.write(f"**Why:** {s['reason']}")
                c1, c2, c3 = st.columns(3)
                c1.metric("⚡ kWh Saved", f"{s['kwh_saved']} kWh/month")
                c2.metric("💰 Bill Saved", f"₹{s['bill_saved']}/month")
                c3.metric("🌍 CO₂ Saved", f"{s['co2_saved']} kg/month")

        st.divider()

        # ── SDG-13 IMPACT SCORE ──────────────────────
        st.subheader("🌱 Your SDG-13 Impact Score")

        # Score based on CO2 per person (assume 4 occupants average)
        co2_per_person = totals["total_co2"] / 4

        if co2_per_person < 50:
            score = "🌟 Excellent"
            color = "green"
            message = "Your household has a very low carbon footprint. Keep it up!"
        elif co2_per_person < 100:
            score = "✅ Good"
            color = "blue"
            message = "Your carbon footprint is below average. Small improvements can make it excellent."
        elif co2_per_person < 200:
            score = "⚠️ Average"
            color = "orange"
            message = "Your footprint is average. Follow the suggestions above to improve."
        else:
            score = "🔴 High"
            color = "red"
            message = "Your footprint is high. Prioritise HIGH suggestions above immediately."

        st.markdown(f"### {score}")
        st.info(message)
        st.markdown(
            f"**Monthly CO₂ per person:** {co2_per_person:.1f} kg "
            f"| **Annual:** {co2_per_person * 12:.1f} kg"
        )

        st.divider()
        st.success("✅ Report complete! Share this with your family to take climate action together. 🌍")
