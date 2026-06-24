import streamlit as st
import os

# Optional OpenAI support
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False


# -----------------------------
# CORE PROMPT BUILDER
# -----------------------------
def build_prompt(topic, level, ability, output_type):
    return f"""
You are an expert Social Studies teacher designing Inquiry-Based Learning (IBL) lessons.

Topic: {topic}
Level: {level}
Student Ability: {ability}
Output Type: {output_type}

Generate:

1. Essential Question (big inquiry question)
2. 3–5 guiding questions
3. Key misconceptions (if relevant)
4. Suggested IBL lesson flow (5 stages):
   - Tuning In
   - Finding Out
   - Sorting Out
   - Going Further
   - Reflecting
5. 3 "Spark Ideas" (provocative hooks for students)

Make it practical for classroom use.
Keep language clear and teacher-friendly.
"""


# -----------------------------
# OPENAI GENERATION (if available)
# -----------------------------
def generate_with_ai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful Social Studies curriculum designer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# -----------------------------
# FALLBACK (NO API KEY)
# -----------------------------
def generate_fallback(topic, level, ability, output_type):
    return f"""
### 🌟 IBL SPARKS (Fallback Mode)

**Topic:** {topic}  
**Level:** {level}  
**Ability Group:** {ability}  

---

### ❓ Essential Question
What makes {topic} important in shaping societies?

---

### 🔎 Guiding Questions
- How did {topic} develop over time?
- What challenges were faced?
- How did people respond to these challenges?

---

### ⚠️ Possible Misconceptions
- Students may think history develops in a straight line
- Students may assume all societies progress in the same way

---

### 🧭 IBL Lesson Flow

**Tuning In**
- Show a striking image or scenario about {topic}

**Finding Out**
- Students gather basic facts through guided sources

**Sorting Out**
- Group findings into themes (social, political, economic)

**Going Further**
- Compare with another civilisation or context

**Reflecting**
- “What surprised me about {topic}?”

---

### 💡 Spark Ideas
- “Was {topic} more advanced than modern society in some ways?”
- “What would you change if you lived in that time?”
- “Is progress always positive?”
"""


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="IBL Sparks Generator", layout="wide")

st.title("🔥 IBL Sparks Idea Generator (Social Studies)")

st.sidebar.header("Lesson Settings")

topic = st.sidebar.text_input("Topic", "Indus Valley Civilization")
level = st.sidebar.selectbox("Level", ["P5", "P6", "Secondary", "General"])
ability = st.sidebar.selectbox("Ability Group", ["HP", "MP", "LP", "Mixed"])
output_type = st.sidebar.selectbox(
    "Output Type",
    ["Inquiry Questions", "Full IBL Lesson", "Spark Cards"]
)

generate = st.sidebar.button("Generate IBL Sparks 🚀")


# -----------------------------
# OUTPUT
# -----------------------------
if generate:
    with st.spinner("Generating IBL Sparks..."):

        prompt = build_prompt(topic, level, ability, output_type)

        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            result = generate_with_ai(prompt)
        else:
            result = generate_fallback(topic, level, ability, output_type)

    st.markdown(result)


# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("IBL Sparks Generator | Built with Streamlit")
