import gradio as gr

def tab3_interface():
    with gr.Blocks() as tab3:
        gr.Markdown("# Tab 3: Info")
        gr.Label("This is Tab 3 for informational purposes.")
    return tab3
