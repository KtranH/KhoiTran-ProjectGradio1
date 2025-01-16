import gradio as gr

def tab4_interface():
    with gr.Blocks() as tab4:
        gr.Markdown("# Tab 3: Info")
        gr.Label("This is Tab 3 for informational purposes.")
    return tab4
