import gradio as gr
from loguru import logger
import sys
# Now it works!
# Configure loguru to output to console
logger.remove()
logger.add(sys.stderr, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>")

def on_tab_change(evt: gr.SelectData):
    """Callback function when tab changes - uses session state"""
    if isinstance(evt, gr.SelectData):
        # Get the selected tab name from the event
        tab_index = evt.index
        tab_names = ["Tab 1", "Tab 2", "Tab 3"]
        if 0 <= tab_index < len(tab_names):
            # Store in session state instead of global variable
            return tab_names[tab_index]
    return "Tab 1"  # Default fallback

def show_selected_tab(current_tab):
    """Button click handler to display current tab"""
    return f"Currently selected tab: {current_tab}"

def update_tab_display():
    """Update the tab display based on session state"""
    return "Click the button to see the current tab..."

with gr.Blocks(title="Multi-Tab Application") as demo:
    # Use session state to track current tab per user
    current_tab = gr.State(value="Tab 1")
    
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
    
    # Add tab change event - updates the session state
    tabs.select(
        fn=on_tab_change,
        inputs=None,
        outputs=current_tab
    )
    
    # Output text and button outside tabs
    gr.Markdown("---")
    output_text = gr.Textbox(
        label="Current Tab Display",
        placeholder="Click the button to see the current tab...",
        interactive=False
    )
    show_tab_btn = gr.Button("Show Selected Tab", variant="primary")
    show_tab_btn.click(
        fn=show_selected_tab,
        inputs=current_tab,
        outputs=output_text
    )

if __name__ == "__main__":
    logger.info("Application started with session-based tab tracking")
    demo.launch()