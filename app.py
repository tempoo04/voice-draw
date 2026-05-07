import streamlit as st
import threading
import recorder
import transcriptor
import painter
from config import APP_LAYOUT, APP_PAGE_TITLE, APP_TITLE, AUDIO_PROMPT_PATH, ICON_DIR

if "record_active" not in st.session_state:
    st.session_state.record_active = threading.Event()
    st.session_state.recording_status = "Baslamaya haziriz!"
    st.session_state.recording_completed = False
    st.session_state.latest_image = ""
    st.session_state.messages = []
    st.session_state.frames = []

def start_recording():
    st.session_state.record_active.set()
    st.session_state.frames = []
    st.session_state.recording_status = "Sesiniz Kaydediliyor..."
    st.session_state.recording_completed = False

    threading.Thread(
        target=recorder.record,
        args=(st.session_state.record_active, st.session_state.frames),
        daemon=True,
    ).start()

def stop_recording():
    st.session_state.record_active.clear()
    st.session_state.recording_status = "Kayit tamamlandi!"
    st.session_state.recording_completed = True



st.set_page_config(page_title=APP_PAGE_TITLE, layout=APP_LAYOUT, page_icon=str(ICON_DIR / "app_icon.png"))
st.image(image=str(ICON_DIR / "top_banner.png"), use_container_width=True)
st.title(f"{APP_TITLE}: Sesli Cizim")
st.divider()

col_audio, col_image = st.columns([1,4])

with col_audio:
    st.subheader("Ses Kayit")
    st.divider()
    status_message = st.info(st.session_state.recording_status)
    st.divider()

    subcol_left , subcol_right = st.columns([1,2])

    with subcol_left:
        start_btn = st.button("Start", on_click= start_recording, disabled= st.session_state.record_active.is_set())
        stop_btn = st.button("Stop", on_click= stop_recording, disabled= not st.session_state.record_active.is_set())
    with subcol_right:
        recorded_audio = st.empty()

        if st.session_state.recording_completed:
            recorded_audio.audio(data=str(AUDIO_PROMPT_PATH))

    st.divider()
    latest_image_use = st.checkbox(label = "Son Resmi Kullan")

with col_image:
    st.subheader("Image Output")
    st.divider()

    for message in st.session_state.messages:

        if message["role"] == "assistant":
            with st.chat_message(name=message["role"], avatar=str(ICON_DIR / "ai_avatar.png")):
                st.warning("Sizin icin olusturdugum gorsel:")
                st.image(image=message["content"], width=300)

        elif message["role"] == "user":
            with st.chat_message(name=message["role"], avatar=str(ICON_DIR / "user_avatar.png")):
                st.success(message["content"])

    if stop_btn:
        with st.chat_message(name="user", avatar=str(ICON_DIR / "user_avatar.png")):
            voice_prompt = transcriptor.transcribe_with_whisper(audio_file_name=str(AUDIO_PROMPT_PATH))
            st.success(voice_prompt)


        st.session_state.messages.append({"role":"user", "content": voice_prompt})
        with st.chat_message(name="assistant", avatar=str(ICON_DIR / "ai_avatar.png")):
            st.warning("Sizin icin olusturdugum gorsel:")

            if latest_image_use and st.session_state.latest_image:
                image_file_name = painter.generate_image(image_path=st.session_state.latest_image, prompt=voice_prompt)
            else:
                image_file_name = painter.generate_image_with_dalle(prompt=voice_prompt)

            st.image(image=image_file_name, width=300)

        st.session_state.messages.append({"role":"assistant", "content": image_file_name})
        st.session_state.latest_image = image_file_name









































