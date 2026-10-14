import math

from flask import Flask, render_template, request, session

from data_structures import LinkedList, Stack


app = Flask(__name__)
# Used only to keep the linked-list demo available while a visitor browses the site.
app.config["SECRET_KEY"] = "change-this-before-deploying-your-portfolio"


def get_measurement(field_name, label):
    """Return a non-negative finite float or a friendly form error."""
    raw_value = request.form.get(field_name, "").strip()
    if not raw_value:
        return None, f"Please enter a {label}."

    try:
        value = float(raw_value)
    except ValueError:
        return None, f"{label.capitalize()} must be a number."

    if not math.isfinite(value) or value < 0:
        return None, f"{label.capitalize()} must be a non-negative finite number."
    return value, None


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/works", methods=["GET", "POST"])
def works():
    result = None
    input_string = ""
    error = None

    if request.method == "POST":
        input_string = request.form.get("inputString", "")
        if input_string.strip():
            result = input_string.upper()
        else:
            error = "Enter some text to convert."

    return render_template(
        "touppercase.html", result=result, input_string=input_string, error=error
    )


@app.route("/works/area/circle", methods=["GET", "POST"])
def circle_area():
    result = None
    error = None
    radius = request.form.get("radius", "")

    if request.method == "POST":
        radius_value, error = get_measurement("radius", "radius")
        if error is None:
            result = math.pi * radius_value**2

    return render_template("circle.html", result=result, error=error, radius=radius)


@app.route("/works/area/triangle", methods=["GET", "POST"])
def triangle_area():
    result = None
    error = None
    base_value = request.form.get("base", "")
    height_value = request.form.get("height", "")

    if request.method == "POST":
        base, base_error = get_measurement("base", "base")
        height, height_error = get_measurement("height", "height")
        error = base_error or height_error
        if error is None:
            result = 0.5 * base * height

    return render_template(
        "triangle.html", result=result, error=error, base=base_value, height=height_value
    )


@app.route("/works/linked-list", methods=["GET", "POST"])
def linked_list():
    linked_list = LinkedList(session.get("linked_list_values", []))
    message = None
    message_type = "info"
    submitted_value = ""

    if request.method == "POST":
        action = request.form.get("action", "")
        submitted_value = request.form.get("value", "").strip()

        if action in {"append", "prepend", "remove", "find"} and not submitted_value:
            message = "Enter a value before choosing that action."
            message_type = "error"
        elif action == "append":
            linked_list.append(submitted_value)
            message = f'Added "{submitted_value}" to the end of the list.'
            submitted_value = ""
        elif action == "prepend":
            linked_list.prepend(submitted_value)
            message = f'Added "{submitted_value}" to the beginning of the list.'
            submitted_value = ""
        elif action == "remove":
            if linked_list.remove(submitted_value):
                message = f'Removed the first "{submitted_value}" node.'
                submitted_value = ""
            else:
                message = f'No node contains "{submitted_value}".'
                message_type = "error"
        elif action == "find":
            index = linked_list.find(submitted_value)
            if index is None:
                message = f'"{submitted_value}" is not in the list.'
                message_type = "error"
            else:
                message = f'Found "{submitted_value}" at index {index}.'
        elif action == "pop":
            removed_value = linked_list.pop_front()
            if removed_value is None:
                message = "The list is already empty."
                message_type = "error"
            else:
                message = f'Removed "{removed_value}" from the beginning of the list.'
        elif action == "clear":
            linked_list.clear()
            message = "Cleared every node from the list."
        else:
            message = "Choose a valid linked-list action."
            message_type = "error"

        session["linked_list_values"] = linked_list.to_list()

    return render_template(
        "linked_list.html",
        nodes=linked_list.to_list(),
        length=linked_list.length,
        message=message,
        message_type=message_type,
        submitted_value=submitted_value,
    )


@app.route("/works/stack", methods=["GET", "POST"])
def stack():
    stack = Stack(session.get("stack_values", []))
    message = None
    message_type = "info"
    submitted_value = ""

    if request.method == "POST":
        action = request.form.get("action", "")
        submitted_value = request.form.get("value", "").strip()

        if action == "push":
            if not submitted_value:
                message = "Enter a value before pushing it onto the stack."
                message_type = "error"
            elif len(submitted_value) > 40:
                message = "Stack values must be 40 characters or fewer."
                message_type = "error"
            else:
                stack.push(submitted_value)
                message = f'Pushed "{submitted_value}" onto the top of the stack.'
                submitted_value = ""
        elif action == "pop":
            removed_value = stack.pop()
            if removed_value is None:
                message = "The stack is already empty."
                message_type = "error"
            else:
                message = f'Removed "{removed_value}" from the top of the stack.'
        elif action == "peek":
            top_value = stack.peek()
            if top_value is None:
                message = "The stack is empty, so it has no top value."
                message_type = "error"
            else:
                message = f'The top value is "{top_value}".'
        elif action == "clear":
            stack = Stack()
            message = "Cleared every value from the stack."
        else:
            message = "Choose a valid stack action."
            message_type = "error"

        session["stack_values"] = stack.to_list()

    return render_template(
        "stack.html",
        values=stack.to_list(),
        length=stack.length,
        message=message,
        message_type=message_type,
        submitted_value=submitted_value,
    )


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
