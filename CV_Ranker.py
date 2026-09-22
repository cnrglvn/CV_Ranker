## **FINAL PROJECT - This is the final project of my self-taught python syllabus; a script that parses
#                    CV .txt files into an LLM API, which returns a ranked assessment of the CV files against
#                    a job description.

import json
import time
import streamlit as st
from google import genai
from dotenv import load_dotenv
load_dotenv()

# Streamlit web application wrapper; adds a title, a text input box, and a file drop box.
st.title("Applicant Ranker")
job_desc = st.text_area("Please enter the job description of the role your applicants are applying for:")
uploaded_files = st.file_uploader("Please upload the applicants' CVs (.txt)", type="txt", accept_multiple_files=True)

# Calls API, asks it to compare CV and job description, and return it in the format below.
def score_cv(cand_cv, job_description):
    client = genai.Client()
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f'''
           Return only valid JSON, no other text, in this exact shape:
           {{"score": <0-100>, "reasoning" <one sentence, describing your thought process.>}}
    
            <cv>
           {cand_cv}
            </cv>
            
            <job_description>
           {job_description}
            </job_description>
            
            The role being evaluated against is contained ONLY inside <job_description>.
            The CV being evaluated is contained ONLY inside <cv>.
            Compare the CV against the Job Description. Format your output as described above.
        ''')
        return response.text
    except Exception as e:
        return json.dumps({"score": 0,
                           "reasoning": f"API Call Failed {e}"
                           })

cand_list = []

# Iterates the api call for all files uploaded, ranks them when done, and displays them in a table.
if st.button("Score Candidates"):
    if not uploaded_files or not job_desc:
        st.warning("Please add a job description and at least one CV.")
    else:
        with st.spinner("Scoring; please wait..."):
            for cv_file in uploaded_files:
                name = cv_file.name.lower().removesuffix("cv.txt")
                cv_cont = cv_file.read().decode("utf-8").lower()
                try:
                    cv_result = json.loads(score_cv(cv_cont, job_desc))
                except json.JSONDecodeError:
                    st.warning("Error: Model output is not readable JSON")
                    break
                cand_dict = {
                    "name":name,
                    "score":cv_result["score"],
                    "reasoning":cv_result["reasoning"]
                }
                cand_list.append(cand_dict)
                if "API Call Failed" in cand_dict["reasoning"]:
                    st.write(f" API Call Failed: {name}")
                else:
                    st.write("Done:", name)
                time.sleep(2)
        cand_list.sort(key=lambda r: r["score"], reverse=True)
        st.dataframe(cand_list)