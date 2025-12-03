"""
Insertion Sort Lab - Interactive Algorithm Visualization
Author: Aurik
Course: CISC 121 - Introduction to Computing Science I (Queen's University)

This application provides an interactive visualization of the insertion sort algorithm
with step-by-step execution tracking, performance metrics, and comparisons with
other sorting algorithms (bubble sort and quicksort).

Features:
- Real-time algorithm execution with detailed tracking
- Performance metrics (comparisons, moves, array accesses)
- Multi-algorithm comparison (insertion, bubble, quick sort)
- Interactive web-based UI using Gradio
- Comprehensive step-by-step execution trace
"""

import gradio as gr
import json


def parse_list(text):
    """
    Parse comma-separated integers from user input string.
    
    Args:
        text (str): Comma-separated string of integers (e.g., "5, 2, 9, 1")
    
    Returns:
        list: List of parsed integers
    
    Raises:
        ValueError: If any value cannot be converted to an integer
    
    Example:
        >>> parse_list("5, 2, 9")
        [5, 2, 9]
    """
    parts = text.split(",")
    nums = []
    
    for p in parts:
        p = p.strip()  # Remove leading/trailing whitespace
        if p == "":
            continue  # Skip empty strings
        try:
            nums.append(int(p))
        except ValueError:
            raise ValueError(f"'{p}' is not a valid integer")
    
    return nums


def insertion_sort_with_steps(arr):
    """
    Implement insertion sort algorithm with complete step-by-step tracking.
    
    Algorithm:
    - Start from index 1 (first element is trivially sorted)
    - For each element (key), compare with sorted portion
    - Shift larger elements right to make space
    - Insert key in correct position
    
    Complexity:
    - Time: O(n) best case, O(n²) average/worst case
    - Space: O(1) - sorts in place
    
    Args:
        arr (list): Input array of integers to sort
    
    Returns:
        tuple: (sorted_array, steps_list, comparisons, moves, accesses)
            - sorted_array: The sorted version of input array
            - steps_list: List of dictionaries recording each step
            - comparisons: Total number of element comparisons
            - moves: Total number of array writes
            - accesses: Total number of array read/write operations
    """
    steps = []
    a = arr[:]  # Create a copy to avoid modifying original
    comparisons = 0
    moves = 0
    array_accesses = 0

    # Record initial state
    steps.append({
        "array": a[:],
        "i": 0,
        "j": 0,
        "comparisons": comparisons,
        "moves": moves,
        "accesses": array_accesses,
        "description": "Initial array",
        "active_indices": []
    })

    # Main insertion sort loop
    for i in range(1, len(a)):
        key = a[i]  # Current element to insert
        j = i - 1   # Start comparing from position before key
        array_accesses += 1

        # Shift elements greater than key to the right
        while j >= 0:
            comparisons += 1  # Count each comparison
            array_accesses += 1
            
            if a[j] > key:
                # Shift element right
                a[j + 1] = a[j]
                moves += 1
                array_accesses += 1
                
                # Record this shift step
                steps.append({
                    "array": a[:],
                    "i": i,
                    "j": j,
                    "comparisons": comparisons,
                    "moves": moves,
                    "accesses": array_accesses,
                    "description": f"Shift {a[j+1]} right",
                    "active_indices": [j, j+1]
                })
                j -= 1
            else:
                # Found correct position, stop shifting
                break

        # Insert key in correct position
        a[j + 1] = key
        moves += 1
        array_accesses += 1
        
        # Record insertion step
        steps.append({
            "array": a[:],
            "i": i,
            "j": j + 1,
            "comparisons": comparisons,
            "moves": moves,
            "accesses": array_accesses,
            "description": f"Insert {key} at position {j+1}",
            "active_indices": [j+1]
        })

    return a, steps, comparisons, moves, array_accesses


def bubble_sort_comparison(arr):
    """
    Implement bubble sort for performance comparison with insertion sort.
    
    Algorithm:
    - Compare adjacent elements
    - Swap if they are in wrong order
    - Repeat until array is sorted
    
    Complexity: O(n²) time, O(1) space
    
    Args:
        arr (list): Input array of integers
    
    Returns:
        tuple: (sorted_array, comparisons, moves)
    """
    a = arr[:]  # Work on copy
    n = len(a)
    comparisons = 0
    moves = 0
    
    # Bubble sort implementation
    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            if a[j] > a[j + 1]:
                # Swap adjacent elements
                a[j], a[j + 1] = a[j + 1], a[j]
                moves += 1
    
    return a, comparisons, moves


def quick_sort_comparison(arr):
    """
    Implement quicksort for performance comparison with insertion sort.
    
    Algorithm:
    - Choose pivot element
    - Partition array into elements less than, equal to, and greater than pivot
    - Recursively sort left and right partitions
    
    Complexity: O(n log n) average case, O(n²) worst case, O(log n) space
    
    Args:
        arr (list): Input array of integers
    
    Returns:
        tuple: (sorted_array, comparisons, moves)
    """
    def quicksort(a, comparisons, moves):
        """
        Recursive quicksort helper function.
        """
        if len(a) <= 1:
            return a, comparisons, moves
        
        # Choose middle element as pivot
        pivot = a[len(a) // 2]
        left, middle, right = [], [], []
        
        # Partition elements
        for x in a:
            comparisons += 1
            if x < pivot:
                left.append(x)
            elif x == pivot:
                middle.append(x)
            else:
                right.append(x)
            moves += 1
        
        # Recursively sort partitions
        left, comparisons, moves = quicksort(left, comparisons, moves)
        right, comparisons, moves = quicksort(right, comparisons, moves)
        
        return left + middle + right, comparisons, moves
    
    sorted_arr, comp, mov = quicksort(arr[:], 0, 0)
    return sorted_arr, comp, mov


def run_lab(text, show_comparisons=True):
    """
    Main orchestration function that coordinates the entire sorting analysis.
    
    This function:
    1. Validates user input
    2. Executes insertion sort with tracking
    3. Runs bubble sort and quicksort for comparison
    4. Calculates efficiency metrics
    5. Formats comprehensive output for display
    
    Args:
        text (str): Comma-separated integers from user input
    
    Returns:
        tuple: (summary, trace, html_dashboard, json_data, status)
            All formatted for Gradio output components
    """
    # Input validation
    if not text.strip():
        return gr.Error("Please enter at least one number"), "", "", "", ""

    try:
        arr = parse_list(text)
    except ValueError as e:
        return gr.Error(f"Invalid input: {str(e)}"), "", "", "", ""

    if len(arr) == 0:
        return gr.Error("Please enter at least one number"), "", "", "", ""

    # Execute insertion sort with full tracking
    sorted_arr, steps, comparisons, moves, accesses = insertion_sort_with_steps(arr)
    
    # Optionally execute alternative algorithms for comparison
    bubble_comps = bubble_moves = quick_comps = quick_moves = None
    if show_comparisons:
        _, bubble_comps, bubble_moves = bubble_sort_comparison(arr)
        _, quick_comps, quick_moves = quick_sort_comparison(arr)

    # Build comprehensive analysis summary
    summary_lines = [
        "=" * 70,
        "INSERTION SORT ANALYSIS",
        "=" * 70,
        f"Sorted {len(arr)} elements successfully",
        "",
        "RESULTS",
        f"  Input:  {arr}",
        f"  Output: {sorted_arr}",
        "",
        "PERFORMANCE METRICS",
        f"  • Comparisons:     {comparisons:,}",
        f"  • Array Moves:     {moves:,}",
        f"  • Total Accesses:  {accesses:,}",
        f"  • Total Operations: {comparisons + moves + accesses:,}",
        "",
                *(["ALGORITHM COMPARISON",
                     f"  ┌─ Insertion Sort  → {comparisons} comparisons, {moves} moves",
                     f"  ├─ Bubble Sort     → {bubble_comps} comparisons, {bubble_moves} moves",
                     f"  └─ Quick Sort      → {quick_comps} comparisons, {quick_moves} moves"]
                    if show_comparisons else ["ALGORITHM COMPARISON (disabled)"]),
        "",
        "EFFICIENCY INSIGHTS",
        *(
            [
                f"  • Insertion vs Bubble: {bubble_comps/max(comparisons,1):.2f}x comparisons",
                f"  • Insertion vs Quick:  {quick_comps/max(comparisons,1):.2f}x comparisons",
            ] if show_comparisons else []
        ),
        f"  • Best Case: O(n) when array is sorted",
        f"  • Worst Case: O(n²) when array is reverse sorted",
        f"  • Average Case: O(n²)",
        "",
        "KEY CHARACTERISTICS",
        f"  • Adaptive: Performs well on nearly-sorted data",
        f"  • Stable: Preserves relative order of equal elements",
        f"  • In-place: Requires O(1) extra space",
        f"  • Online: Can sort data as it receives it",
        "=" * 70
    ]
    summary = "\n".join(summary_lines)

    # Build detailed step-by-step execution trace
    trace_lines = []
    trace_lines.append("+" + "-" * 68 + "+")
    trace_lines.append("| " + "STEP-BY-STEP EXECUTION TRACE".center(66) + " |")
    trace_lines.append("+" + "-" * 68 + "+")
    
    for idx, step in enumerate(steps):
        trace_lines.append(f"\n+-- STEP {idx:02d} " + "-" * 56)
        trace_lines.append(f"| Action: {step['description']}")
        
        # Format array with visual separators
        array_visual = " -> ".join(f"[{x}]" for x in step['array'])
        trace_lines.append(f"| Array:  {array_visual}")
        trace_lines.append(f"| Indices: i={step['i']}, j={step['j']}")
        trace_lines.append(f"| Stats:  {step['comparisons']} comps | {step['moves']} moves | {step['accesses']} accesses")
        trace_lines.append(f"+" + "-" * 68)

    steps_text = "\n".join(trace_lines)

    # Generate interactive HTML performance dashboard
    html_viz = f"""
    <div style="font-family: 'Courier New', monospace; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; overflow-x: auto;">
        <h3 style="margin-top: 0;">ALGORITHM PERFORMANCE DASHBOARD</h3>
        <table style="width: 100%; border-collapse: collapse; background: rgba(255,255,255,0.1); backdrop-filter: blur(10px);">
            <tr style="background: rgba(255,255,255,0.2); font-weight: bold; border-bottom: 2px solid white;">
                <th style="padding: 12px; text-align: left;">Metric</th>
                <th style="padding: 12px; text-align: center;">Insertion</th>
                {('<th style="padding: 12px; text-align: center;">Bubble</th>' if show_comparisons else '')}
                {('<th style="padding: 12px; text-align: center;">Quick</th>' if show_comparisons else '')}
                <th style="padding: 12px; text-align: center;">Best</th>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.2);">
                <td style="padding: 12px;"><b>Comparisons</b></td>
                <td style="padding: 12px; text-align: center;">{comparisons}</td>
                {('<td style="padding: 12px; text-align: center;">' + str(bubble_comps) + '</td>' if show_comparisons else '')}
                {('<td style="padding: 12px; text-align: center;">' + str(quick_comps) + '</td>' if show_comparisons else '')}
                <td style="padding: 12px; text-align: center;">{('Insertion' if not show_comparisons else ('Insertion' if comparisons <= min(bubble_comps, quick_comps) else 'Quick' if quick_comps <= bubble_comps else 'Bubble'))}</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.2);">
                <td style="padding: 12px;"><b>Array Moves</b></td>
                <td style="padding: 12px; text-align: center;">{moves}</td>
                {('<td style="padding: 12px; text-align: center;">' + str(bubble_moves) + '</td>' if show_comparisons else '')}
                {('<td style="padding: 12px; text-align: center;">' + str(quick_moves) + '</td>' if show_comparisons else '')}
                <td style="padding: 12px; text-align: center;">{'Best' if moves <= min(bubble_moves, quick_moves) else ''}</td>
            </tr>
            <tr>
                <td style="padding: 12px;"><b>Total Operations</b></td>
                <td style="padding: 12px; text-align: center;"><strong>{comparisons + moves + accesses}</strong></td>
                {('<td style="padding: 12px; text-align: center;">' + str(bubble_comps + bubble_moves) + '</td>' if show_comparisons else '')}
                {('<td style="padding: 12px; text-align: center;">' + str(quick_comps + quick_moves) + '</td>' if show_comparisons else '')}
                <td style="padding: 12px; text-align: center;">✓</td>
            </tr>
        </table>
        <br>
        <h4>Algorithm Rankings (Lower is Better):</h4>
        <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-top: 10px;">
            {('' if show_comparisons else '<p>Comparisons disabled for single-algorithm mode.</p>')}
            {('<p><strong>Insertion Sort wins on comparisons</strong></p>' if comparisons <= min(bubble_comps, quick_comps) else '') if show_comparisons else ''}
            {('<p><strong>Quick Sort is most efficient overall</strong></p>' if quick_comps + quick_moves <= comparisons + moves else '') if show_comparisons else ''}
            <p>Array Size: <strong>{len(arr)}</strong> elements</p>
        </div>
    </div>
    """

    # Prepare structured data for export/analysis
    json_data = json.dumps({
        "original": arr,
        "sorted": sorted_arr,
        "insertion": {
            "comparisons": comparisons,
            "moves": moves,
            "accesses": accesses
        },
        **({
            "bubble": {"comparisons": bubble_comps, "moves": bubble_moves},
            "quick": {"comparisons": quick_comps, "moves": quick_moves}
        } if show_comparisons else {})
    })

    return summary, steps_text, html_viz, json_data, "Analysis Complete"


# ==================== GRADIO USER INTERFACE ====================

# Create the Gradio web interface using Blocks for custom layout
with gr.Blocks(title="Insertion Sort Laboratory") as demo:
    
    # Header section
    gr.Markdown("""
    <div style="font-family: 'Georgia', 'Times New Roman', serif; background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); padding: 30px; border-radius: 8px; color: white; margin-bottom: 20px;">
        <h1 style="margin: 0; font-size: 2.5em; font-weight: 600;">Insertion Sort Laboratory</h1>
        <p style="margin: 10px 0 0 0; font-size: 1.1em; opacity: 0.95;">Interactive Algorithm Analysis and Visualization</p>
    </div>
    """)

    # Main input/instruction section
    with gr.Row():
        # Left column: Instructions and algorithm info
        with gr.Column(scale=1):
            gr.Markdown("""
            ### Quick Start
            
            Enter integers separated by commas:
            
            **Examples:**
            - Small: `5, 2, 9`
            - Medium: `7, 2, 8, 1, 5, 3`
            - Reverse: `10, 9, 8, 7, 6, 5`
            - Nearly sorted: `1, 2, 3, 5, 4, 6`
            
            The system will analyze insertion sort and compare it with bubble sort and quicksort.
            """)
            
            gr.Markdown("""
            ### Algorithm Characteristics
            
            **Time Complexity:**
            - Best: O(n)
            - Average: O(n²)
            - Worst: O(n²)
            
            **Space Complexity:** O(1)
            
            **Properties:**
            - Stable: ✓
            - In-place: ✓
            - Online: ✓
            """)

        # Right column: Input field and submit button
        with gr.Column(scale=2):
            input_field = gr.Textbox(
                label="Enter Array (comma-separated integers)",
                placeholder="e.g., 5, 2, 9, 1, 5",
                lines=4,
                interactive=True
            )
            comparisons_toggle = gr.Checkbox(label="Show algorithm comparisons (bubble & quick)", value=False)
            submit_btn = gr.Button("ANALYZE & VISUALIZE", size="lg", variant="primary")

    gr.Markdown("---")

    # Output sections
    with gr.Row():
        summary_output = gr.Textbox(
            label="Comprehensive Analysis",
            lines=20,
            interactive=False,
            show_label=True
        )

    with gr.Row():
        trace_output = gr.Textbox(
            label="Step-by-Step Execution Trace",
            lines=24,
            interactive=False,
            show_label=True
        )

    with gr.Row():
        html_output = gr.HTML(
            label="Performance Dashboard"
        )

    # Hidden outputs for data export
    data_output = gr.Textbox(visible=False)
    status_output = gr.Textbox(visible=False)

    # Connect button click event
    submit_btn.click(
        fn=run_lab,
        inputs=[input_field, comparisons_toggle],
        outputs=[summary_output, trace_output, html_output, data_output, status_output]
    )

    # Allow Enter key to submit (same as clicking button)
    input_field.submit(
        fn=run_lab,
        inputs=[input_field, comparisons_toggle],
        outputs=[summary_output, trace_output, html_output, data_output, status_output]
    )

    # Educational information section
    gr.Markdown("""
    ---
    ### How Insertion Sort Works
    
    1. **Start from Index 1**: The first element is trivially sorted
    2. **Extract Key**: Take the current element (key)
    3. **Compare Backwards**: Compare key with sorted portion from right to left
    4. **Shift Right**: Move larger elements one position to the right
    5. **Insert Key**: Place key in its correct position
    6. **Repeat**: Move to next element until array is sorted
    
    #### Why Use Insertion Sort?
    - **Adaptive**: Excellent for nearly-sorted data (O(n) best case)
    - **Online**: Can process data as it arrives
    - **Stable**: Maintains relative order of equal elements
    - **Practical**: Efficient for small datasets (< 50 elements)
    - **Memory Efficient**: Sorts in-place with O(1) space
    
    #### When to Use
    ✓ Small datasets  
    ✓ Nearly sorted data  
    ✓ Memory-constrained systems  
    ✓ Online sorting scenarios  
    
    #### When to Avoid
    ✗ Large random datasets (use quicksort or mergesort)  
    ✗ Performance-critical applications requiring O(n log n)
    """)


# Main entry point - launch the Gradio app
if __name__ == "__main__":
    demo.launch(share=True)
