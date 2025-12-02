import gradio as gr

def parse_list(text):

    parts = text.split(",")
    nums = []
    for p in parts:
        p = p.strip()
        if p == "":
            continue
        nums.append(int(p))
    return nums


def insertion_sort_with_steps(arr):

    steps = []
    a = arr[:]  # work on a copy
    comparisons = 0
    moves = 0

    # Initial state
    steps.append({
        "array": a[:],
        "i": 0,
        "j": 0,
        "comparisons": comparisons,
        "moves": moves,
        "description": "Initial array"
    })

    for i in range(1, len(a)):
        key = a[i]
        j = i - 1

        # Shift larger elements to the right
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                moves += 1
                steps.append({
                    "array": a[:],
                    "i": i,
                    "j": j,
                    "comparisons": comparisons,
                    "moves": moves,
                    "description": f"Move {a[j+1]} right to make space for {key}"
                })
                j -= 1
            else:
                # key is in the correct spot relative to a[j]
                break

        # Place key in its correct position
        a[j + 1] = key
        moves += 1
        steps.append({
            "array": a[:],
            "i": i,
            "j": j + 1,
            "comparisons": comparisons,
            "moves": moves,
            "description": f"Insert {key} at index {j+1}"
        })

    return a, steps, comparisons, moves


def run_lab(text):

    # Handle bad / empty input
    try:
        arr = parse_list(text)
    except ValueError:
        return "Error: please enter integers separated by commas.", ""

    if len(arr) == 0:
        return "Please enter at least one number.", ""

    sorted_arr, steps, comparisons, moves = insertion_sort_with_steps(arr)

    # Build detailed steps text (teaching focus)
    lines = []
    for idx, step in enumerate(steps):
        line = (
            f"Step {idx}: {step['array']} | "
            f"i={step['i']}, j={step['j']}, "
            f"comparisons={step['comparisons']}, moves={step['moves']} | "
            f"{step['description']}"
        )
        lines.append(line)
    steps_text = "\n".join(lines)

    # Short summary for quick understanding
    summary = (
        f"Original array: {arr}\n"
        f"Sorted array:   {sorted_arr}\n"
        f"Total comparisons: {comparisons}\n"
        f"Total moves:       {moves}"
    )

    return summary, steps_text


demo = gr.Interface(
    fn=run_lab,
    inputs="text",
    outputs=["text", "text"],
    title="Insertion Sort Lab",
    description=(
        "Explore how insertion sort works. "
        "See each step and track how many comparisons and moves it uses."
    ),
)

if __name__ == "__main__":
    demo.launch()
