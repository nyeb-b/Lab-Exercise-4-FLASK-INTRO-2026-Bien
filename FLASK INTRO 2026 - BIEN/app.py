import math

from flask import Flask, render_template, request, session


app = Flask(__name__)
# Used only to keep the linked-list demo available while a visitor browses the site.
app.config["SECRET_KEY"] = "change-this-before-deploying-your-portfolio"


class Node:
    """One item in a singly linked list."""

    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    """A small linked-list implementation used by the interactive lab page."""

    def __init__(self, values=None):
        self.head = None
        self.length = 0
        for value in values or []:
            self.append(value)

    def append(self, value):
        node = Node(value)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node
        self.length += 1

    def prepend(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node
        self.length += 1

    def remove(self, value):
        """Remove the first matching node and return whether it was found."""
        previous = None
        current = self.head
        while current is not None:
            if current.value == value:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                self.length -= 1
                return True
            previous, current = current, current.next
        return False

    def pop_front(self):
        if self.head is None:
            return None
        value = self.head.value
        self.head = self.head.next
        self.length -= 1
        return value

    def find(self, value):
        current = self.head
        index = 0
        while current is not None:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return None

    def clear(self):
        self.head = None
        self.length = 0

    def to_list(self):
        values = []
        current = self.head
        while current is not None:
            values.append(current.value)
            current = current.next
        return values


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


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
