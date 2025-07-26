import streamlit as st
import requests


API_URL = "http://localhost:8000"

st.set_page_config(page_title="PNG Chat", layout="centered")

if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None


def login_ui():
    st.title("Login to AI Chat")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if not username or not password:
            st.warning("Please fill in all fields.")
            return

        try:
            response = requests.post(
                f"{API_URL}/login",
                json={
                    "username": username,
                    "password": password
                }
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state.token = data["access_token"]
                st.session_state.username = username
                st.rerun()

            else:
                st.error("Invalid credentials or login failed.")
                st.code(response.text)

        except Exception as e:
            st.error(f"Error connecting to server: {str(e)}")



def chat_ui():
    st.title(f"Welcome {st.session_state.username}!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(chat["question"])

        with st.chat_message("assistant"):
            st.markdown(chat["answer"])

    prompt = st.chat_input("Ask your questions...", accept_file=True, file_type=["pdf"])

    if prompt:
        user_question = prompt.text.strip() if prompt.text else None
        uploaded_pdf = prompt.files[0] if prompt.files else None

        headers = {"Authorization": f"Bearer {st.session_state.token}"}

        if uploaded_pdf:
            with st.chat_message("user"):
                st.markdown("Uploaded: " + uploaded_pdf.name)

            files = {
                "file": (uploaded_pdf.name, uploaded_pdf, "application/pdf")
            }
            upload_res = requests.post(f"{API_URL}/upload", files=files, headers=headers)

            if upload_res.status_code == 200:
                st.chat_message("assistant").markdown("PDF uploaded and embedded successfully!")
            else:
                st.chat_message("assistant").markdown("PDF upload failed.")
                st.code(upload_res.text)

        if user_question:
            with st.chat_message("user"):
                st.markdown(user_question)

            try:
                chat_res = requests.post(
                    f"{API_URL}/chat",
                    json={"question": user_question},
                    headers=headers
                )

                if chat_res.status_code == 200:
                    answer = chat_res.json()["answer"]
                else:
                    answer = "Could not get an answer."
                    st.code(chat_res.text)

            except Exception as e:
                answer = f"Error: {str(e)}"

            with st.chat_message("assistant"):
                st.markdown(answer)

            st.session_state.chat_history.append({
                "question": user_question,
                "answer": answer
            })

def load_chat_history():
    st.sidebar.markdown("Your Chat History")

    try:
        res = requests.get(
            f"{API_URL}/chat-history",
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )

        if res.status_code == 200:
            history = res.json()
            if not history:
                st.sidebar.info("No history yet.")
                return

            with st.sidebar.expander("View History", expanded=False):
                for i, chat in enumerate(reversed(history[-5:]), 1):  # last 5
                    st.markdown(f"**{i}. {chat['question']}**")
                    short_ans = chat['answer'].strip().split('\n')[0][:150] + "..."
                    st.caption(short_ans)
                    st.markdown("---")

        else:
            st.sidebar.error("Could not load history")
            st.sidebar.code(res.text)

    except Exception as e:
        st.sidebar.error(f"Error: {str(e)}")



def logout():
    st.session_state.token = None
    st.session_state.username = None
    st.session_state.chat_history = []
    st.rerun()

if not st.session_state.token:
    login_ui()

else:
    chat_ui()