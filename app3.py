import streamlit as st
import numpy as np
from helper import provide_guidance, predict_career_path
# Set up the main page layout
st.set_page_config(
    page_title="UMap",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="expanded"
)

if "page" not in st.session_state:
    st.session_state.page = "main"  
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "guidance_shown" not in st.session_state:
    st.session_state.guidance_shown = False

def main_page():
    st.title("🧭 UMap : ✨ Navigate the Future U ✨")
    st.sidebar.header("UMap")
    st.sidebar.write("""Our Career Path Prediction and Guidance System will assist you in shaping your future and having a better understanding of a pathway to achieve your goals.""")
    st.sidebar.write("""\nUsing advanced algorithms, this system assesses your unique skills, interests, certifications, and experiences to generate a supervised prediction of potential career paths that align with your strengths.\nThe app analyzes your skill ratings, preferred career areas, and relevant qualifications, comparing these factors against successful career patterns. By capturing a holistic view of your profile, the system offers tailored guidance on career choices and areas of improvement, ensuring the pathway recommended truly resonates with your aspirations. Whether you’re just starting out or looking to make a shift, our app empowers you with insights and resources to confidently take the next step toward a fulfilling career.""")


    
    st.markdown("#### Rate Your Skills and Capabilities")
    coding_skills_rating = st.slider("Coding Skills Rating", 1, 10, 5)
    self_learning_capability = st.radio("Self-Learning Capability", [0, 1], index=1)
    reading_and_writing_skills = st.selectbox("Reading and Writing Skills", [0, 1, 2])
    memory_capability_score = st.selectbox("Memory Capability Score", [0, 1, 2])

    st.markdown("#### Select Your Certifications")
    certifications = st.multiselect("Certifications", ['App Development', 'Distro Making', 'Full Stack', 
                                                      'Hadoop', 'Information Security', 'Machine Learning', 
                                                      'Python', 'R Programming', 'Shell Programming'])

    st.markdown("#### Select the Workshops Attended")
    workshops = st.multiselect("Workshops Attended", ['Cloud Computing', 'Data Science', 'Database Security', 
                                                      'Game Development', 'Hacking', 'System Designing', 
                                                      'Testing', 'Web Technologies'])

    st.markdown("#### Choose Your Interested Subjects")
    interested_subjects = st.multiselect("Interested Subjects", ['Computer Architecture', 'IOT', 'Management', 
                                                                'Software Engineering', 'Cloud Computing', 
                                                                'Data Engineering', 'Hacking', 'Networks', 
                                                                'Parallel Computing', 'Programming'])

    st.markdown("#### Select Your Preferred Career Area")
    interested_career_area = st.multiselect("Interested Career Area", ['Business Process Analyst', 
                                                                       'Cloud Computing', 'Developer', 
                                                                       'Security', 'System Developer', 
                                                                       'Testing'])

    st.markdown("#### Choose the Preferred Type of Company")
    type_of_company = st.selectbox("Preferred Type of Company", ['BPA', 'Cloud Services', 'Finance', 
                                                                'Product Based', 'SAaS Services', 
                                                                'Sales and Marketing', 'Service Based', 
                                                                'Testing and Maintenance Services', 'Web Services', 
                                                                'Product Development'])

    
    def check_required_fields():
        return (coding_skills_rating is not None and self_learning_capability is not None and
                reading_and_writing_skills is not None and memory_capability_score is not None and
                certifications and workshops and interested_subjects and interested_career_area and type_of_company)

   
    def encode_inputs():
        certifications_vector = [1 if cert in certifications else 0 for cert in
                                 ['App Development', 'Distro Making', 'Full Stack', 'Hadoop', 'Information Security',
                                  'Machine Learning', 'Python', 'R Programming', 'Shell Programming']]
        workshops_vector = [1 if workshop in workshops else 0 for workshop in
                            ['Cloud Computing', 'Data Science', 'Database Security', 'Game Development', 'Hacking',
                             'System Designing', 'Testing', 'Web Technologies']]
        subjects_vector = [1 if subject in interested_subjects else 0 for subject in
                           ['Computer Architecture', 'IOT', 'Management', 'Software Engineering', 'Cloud Computing',
                            'Data Engineering', 'Hacking', 'Networks', 'Parallel Computing', 'Programming']]
        career_area_vector = [1 if area in interested_career_area else 0 for area in
                              ['Business Process Analyst', 'Cloud Computing', 'Developer', 'Security', 'System Developer',
                               'Testing']]
        company_vector = [1 if company == type_of_company else 0 for company in
                          ['BPA', 'Cloud Services', 'Finance', 'Product Based', 'SAaS Services', 'Sales and Marketing',
                           'Service Based', 'Testing and Maintenance Services', 'Web Services', 'Product Development']]

        return np.array([coding_skills_rating, self_learning_capability,
                         reading_and_writing_skills, memory_capability_score] +
                        certifications_vector + workshops_vector + subjects_vector +
                        career_area_vector + company_vector).reshape(1, -1)

    
    if 'prediction' not in st.session_state:
        st.session_state.prediction = None
    if 'guidance_shown' not in st.session_state:
        st.session_state.guidance_shown = False

    
    if st.button("🔍 Predict Career Path"):
        if check_required_fields():
            st.session_state.prediction = predict_career_path(encode_inputs())
            st.session_state.guidance_shown = True
            st.success(f"*Predicted Career Path:* {st.session_state.prediction}")
        else:
            st.error("Please fill in all required fields to proceed with prediction and guidance.")
    
    
    if st.session_state.guidance_shown:
        if st.button("📝 Get Guidance"):
            guidance = provide_guidance(st.session_state.prediction)
            st.session_state['guidance_text'] = guidance
            st.info(f"*Guidance:* {guidance}")

        if st.button("📍 View Roadmap"):
            st.session_state.page = "roadmap"
            st.experimental_rerun()    


def roadmap_page():
    st.title("📍 Career Roadmap")
    if "prediction" in st.session_state and st.session_state.prediction:
        st.write(f"Predicted Path: *{st.session_state.prediction}*")
        st.write("Your Career Roadmap:")
        st.write("- *Learn Cloud Fundamentals*")
        st.write("- *Earn AWS Certification*")
        st.write("- *Gain hands-on experience in DevOps*")
    else:
        st.write("No prediction available.")


    if st.button("⬅️ Back to Main Page"):
        st.session_state.page = "main"
        st.experimental_rerun()


if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "roadmap":
    roadmap_page()