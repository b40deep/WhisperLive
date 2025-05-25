import gradio as gr


# Gradio Function that calls the transcription client
def gradio_function(audio, transcription_state):
    # Return the current transcription result from the state
    return "sample transcription"   # Return the current transcription state as the result

# Setup Gradio Interface using Blocks
with gr.Blocks() as demo:
    transcription_state = gr.State("Transcription not started.")  # Initialize state with a default value
    audio_input = gr.Audio(sources="microphone", type="filepath", label="Speak into the microphone")
    output_text = gr.Textbox(label="Transcription", interactive=True)
    start_button = gr.Button("Start Transcription")

    start_button.click(fn=gradio_function, inputs=[audio_input, transcription_state], outputs=[output_text])

# Launch Gradio app
demo.launch()
