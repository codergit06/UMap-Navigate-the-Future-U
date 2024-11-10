import streamlit as st

# Display the roadmap using the guidance in session state
st.title("📍 Your Career Path Roadmap")

if 'guidance_text' in st.session_state:
    # Display the guidance as a roadmap
    st.write(st.session_state.guidance_text)
    st.write("### Suggested Steps:")
    st.write("- Break down the guidance into actionable steps here.")
    st.write("- Include any additional resources or links.")

else:
    st.warning("No guidance found. Please generate your career path first.")