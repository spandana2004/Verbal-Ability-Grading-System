import streamlit as st
from main import speech_to_text, analyze_audio, analyze_text, provide_feedback
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Speech to Text and Text Analysis Dashboard",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for styling
st.markdown("""
    <style>
    /* Dashboard Layout */
    .dashboard-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
        margin-top: 30px;
    }
    .dashboard-section{
            width:60%;
            }
    .content{
            width:100%;
            font-weight:bold;
            }
    .dashboard-section, .content1{
        padding: 20px;
        background-color: #f5f5f5;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
        display: flex;
        justify-content: center;
        align-items: center; /* Align items vertically */
        margin-left: auto;
        margin-right: auto;
    }

    .dashboard-section h2 {
    
        font-size: 1.8em;
        margin-bottom: 10px;
    }

    .dashboard-section .content {
        margin-top: 15px;
    }

    .dashboard-section .content p {
        line-height: 1.6;
    }

    .dashboard-section .content img {
        max-width: 100%;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .sub {
        text-align: center;
    }
    
    .center-button {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 30px;
    }
    .tips-container {
        text-align: left;
    }
    h2 {
        text-align: center;
            color: 	#383838;
    }
    button {
        align-items: center;
    }
    .centered-div {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 50%;
        /* Adjust as needed */
    }
    .center{
            margin-right:100px;
            }
            .main{
            color: 	#383838;
            background-color:	#eeeeee;
            }
            h4
            {
            color: 	#383838;
            }
            #one{
            font-weight:bolder;
            }
    </style>
""", unsafe_allow_html=True)

# Main function for the dashboard layout
def main():
    # Section 1: Speech to Text Recognition
    st.markdown('<div class="dashboard-section"><h2>Verbal Ability Grading System</h2></div>', unsafe_allow_html=True)
    
    # Adding an image related to speech recognition
    st.markdown('<div style="margin-bottom: 30px;"></div>', unsafe_allow_html=True)
    st.markdown('<div><h4>About</h4></div>', unsafe_allow_html=True)
    st.markdown('<div class="content1" style = "margin-bottom:30px;text-align:justify;">The Verbal Ability Grading System assesses an individual\'s proficiency in spoken language based on various criteria such as fluency, vocabulary usage, grammar accuracy, coherence, and readability. Each metric contributes to an overall evaluation of verbal communication skills, helping to gauge how effectively one can express ideas, articulate thoughts, and engage in dialogue. Higher scores indicate stronger verbal abilities, reflecting clarity, articulation, and the ability to convey messages with precision and coherence. This grading system is valuable in educational, professional, and personal contexts, offering insights into language skills development and areas for improvement.</div>', unsafe_allow_html=True)
    st.markdown("<div><h4>Assessment Test</h4></div>", unsafe_allow_html=True)
    st.markdown('<div class="content1" style = "margin-bottom:30px;">Click on &nbsp;<b id = "one">Take Test</b>&nbsp; to take the Grading Test.</div>', unsafe_allow_html=True)
   
    # Button centered within the div
    columns = st.columns((2, 2, 0.5))
    button_pressed = columns[1].button('Take Test')
    

    
    
    if button_pressed:
        with st.spinner("Recording... Please wait..."):
            text, audio = speech_to_text()
        
        st.markdown("### Recognized Text")
        st.success(text)
    
        if audio:
            st.audio(audio.get_wav_data(), format='audio/wav')
        
        if text not in ["Sorry, I did not understand the audio", "Sorry, my speech service is down"]:
            with st.spinner("Analyzing text..."):
                analysis_results = analyze_text(text)
                audio_results = analyze_audio(audio)
                combined_scores = {**analysis_results, **audio_results}
                rating = provide_feedback(combined_scores)

            st.markdown("### Analysis Results")
            st.markdown('<div class="content">', unsafe_allow_html=True)

            # Creating tabs for interactive sections
            tab1, tab2, tab3, tab4 = st.tabs(["Text Analysis", "Audio Analysis", "Combined Scores", "Feedback"])

            with tab1:
                st.subheader("Text Analysis")
                st.dataframe(pd.DataFrame(list(analysis_results.items()), columns=["Metric", "Score"]).set_index("Metric"))

            with tab2:
                st.subheader("Audio Analysis")
                st.dataframe(pd.DataFrame(list(audio_results.items()), columns=["Metric", "Score"]).set_index("Metric"))

            with tab3:
                st.subheader("Combined Scores")
                st.dataframe(pd.DataFrame(list(combined_scores.items()), columns=["Metric", "Score"]).set_index("Metric"))

                st.markdown("### Visual Representation of Scores")
                st.plotly_chart(create_score_bar_chart(combined_scores))

            with tab4:
                st.markdown("### Feedback")
                new_feedback = list(rating.split("\n"))
                for feedback in new_feedback:
                    st.write(feedback)

            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("### Tips to Improve Speaking Skills")
            st.markdown('<div class="content tips-container">', unsafe_allow_html=True)
            st.write("""
                1. **Practice Regularly**: Consistent practice helps you become more fluent and confident.
                2. **Listen and Repeat**: Mimic native speakers by listening to and repeating sentences.
                3. **Expand Your Vocabulary**: Learn new words daily and use them in sentences.
                4. **Work on Pronunciation**: Pay attention to the correct pronunciation of words.
                5. **Engage in Conversations**: Participate in conversations with native speakers whenever possible.
                6. **Read Aloud**: Reading aloud improves your pronunciation and helps you practice intonation.
                7. **Record Yourself**: Record your speech and listen to it to identify areas for improvement.
                8. **Take Breaks**: Pausing between thoughts can help you speak more clearly and avoid filler words.
                9. **Use Gestures**: Non-verbal communication, like gestures, can help convey your message more effectively.
                10. **Stay Relaxed**: Try to stay calm and relaxed while speaking to avoid nervousness affecting your speech.
            """)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Section 2: Placeholder for additional dashboard sections
    # Additional sections can be added here in the future

    st.markdown('</div>', unsafe_allow_html=True)

def create_score_bar_chart(scores):
    fig = go.Figure(data=[
        go.Bar(name='Scores', x=list(scores.keys()), y=list(scores.values()))
    ])
    fig.update_layout(
        title='Analysis Scores',
        xaxis_title='Metrics',
        yaxis_title='Scores',
        yaxis=dict(range=[0, 10]),
    )
    return fig

if __name__ == "__main__":
    main()
