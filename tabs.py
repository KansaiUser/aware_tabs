import gradio as gr
from loguru import logger
import sys
# This works great but it shares a comon global variable shared among multiple users
# Configure loguru to output to console
logger.remove()
logger.add(sys.stderr, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>")

# Global variable to track current tab
current_tab = "Tab 1"

def on_tab_change(evt: gr.SelectData):
    """Callback function when tab changes"""
    global current_tab
    if isinstance(evt, gr.SelectData):
        # Get the selected tab name from the event
        tab_index = evt.index
        tab_names = ["Tab 1", "Tab 2", "Tab 3"]
        if 0 <= tab_index < len(tab_names):
            current_tab = tab_names[tab_index]
            logger.info(f"Tab changed to {current_tab}")

def show_selected_tab():
    """Button click handler to display current tab"""
    return f"Currently selected tab: {current_tab}"

with gr.Blocks(title="Multi-Tab Application") as demo:
    gr.Markdown("# Multi-Tab Application")
    
    # Create tabs - force Tab 1 to be visible by making it active
    with gr.Tabs(selected=0) as tabs:  # Use index 0 to force select first tab
        with gr.TabItem("Tab 1", id="tab1"):
            gr.Markdown("## Welcome to Tab 1")
            gr.Textbox(label="Input 1", placeholder="Enter text here...")
            gr.Button("Action 1")
            
        with gr.TabItem("Tab 2", id="tab2"):
            gr.Markdown("## Welcome to Tab 2")
            gr.Number(label="Input 2", value=0)
            gr.Checkbox(label="Option 2")
            
        with gr.TabItem("Tab 3", id="tab3"):
            gr.Markdown("## Welcome to Tab 3")
            gr.Dropdown(choices=["Option A", "Option B", "Option C"], label="Select Option")
            gr.Slider(0, 100, label="Slider")
    
    # Add tab change event after creating all tabs
    tabs.select(on_tab_change, inputs=None, outputs=None)
    
    # Output text and button outside tabs
    gr.Markdown("---")
    output_text = gr.Textbox(
        label="Current Tab Display",
        placeholder="Click the button to see the current tab...",
        interactive=False
    )
    show_tab_btn = gr.Button("Show Selected Tab", variant="primary")
    show_tab_btn.click(show_selected_tab, inputs=None, outputs=output_text)

if __name__ == "__main__":
    # Log initial tab
    logger.info(f"Application started. Initial tab: {current_tab}")
    demo.launch()