from flask import Flask, render_template, request, jsonify
import requests
import random

app = Flask(__name__)

WIKI_API = "https://en.wikipedia.org/api/rest_v1/page/summary/"


def get_topic_data(topic):

    url = WIKI_API + topic.replace(" ", "_")

    headers = {
        "User-Agent": "RabbitHoleApp/1.0"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return {
                "title": topic,
                "summary": "Could not find information."
            }

        data = response.json()

        return {
            "title": data.get("title", topic),
            "summary": data.get("extract", "No summary found.")
        }

    except:
        return {
            "title": topic,
            "summary": "System failed to resolve node."
        }


def get_related_topics(topic):

    search_url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "titles": topic,
        "prop": "links",
        "pllimit": 20
    }

    headers = {
        "User-Agent": "RabbitHoleApp/1.0"
    }

    try:
        response = requests.get(search_url, params=params, headers=headers)
        data = response.json()

        pages = data["query"]["pages"]

        related = []

        for page_id in pages:

            links = pages[page_id].get("links", [])

            for link in links:

                title = link["title"]

                if ":" not in title and len(title) < 40:
                    related.append(title)

        return related

    except:
        return []


def fake_system_log(topic_a, topic_b, depth):

    logs = [

        f"[WARN] semantic drift detected between '{topic_a}' and '{topic_b}'",

        f"[TRACE] recursive link stabilized at depth {depth}",

        f"[INFO] background correlation increased: {random.randint(14, 72)}%",

        f"[ERROR] unexpected association collapse in node '{topic_b}'",

        f"[DEBUG] traversal memory overlap detected",

        f"[ALERT] repeated conceptual signature emerging",

        f"[NOTICE] random traversal should not stabilize this quickly"
    ]

    return random.choice(logs)


def generate_conspiracy(path):

    if len(path) < 2:
        return "Insufficient traversal depth."

    openings = [
        "PATTERN ENGINE ACTIVE...",
        "SEMANTIC RECONSTRUCTION INITIATED...",
        "NON-RANDOM STRUCTURE DETECTED...",
        "WARNING: traversal coherence increasing..."
    ]

    linkers = [
        "is not isolated from",
        "forms recursive linkage with",
        "exhibits hidden correlation with",
        "appears structurally dependent on",
        "collapses into relationship with"
    ]

    escalations = [
        "The sequence stabilized too quickly.",
        "The same structures continue to reappear.",
        "Random traversal should not behave like this.",
        "Correlation persisted after divergence.",
        "Observer influence cannot be excluded.",
        "The path resisted entropy."
    ]

    endings = [
        "INTERPRETATION STATUS: unstable.",
        "SYSTEM WARNING: meaning density exceeds baseline.",
        "RESULT: traversal consistency unresolved.",
        "FINAL STATE: observer-pattern boundary degraded."
    ]

    output = []

    output.append(random.choice(openings))
    output.append("")

    for i in range(len(path) - 1):

        a = path[i]
        b = path[i + 1]

        output.append(
            f"{a} {random.choice(linkers)} {b}."
        )

        if random.random() > 0.55:
            output.append(
                random.choice(escalations)
            )

    output.append("")
    output.append(random.choice(endings))

    return "\n".join(output)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/rabbit-hole", methods=["POST"])
def rabbit_hole():

    data = request.json

    topic = data.get("topic")
    path = data.get("path", [])

    wiki_data = get_topic_data(topic)

    related = get_related_topics(topic)

    if not related:

        return jsonify({
            "error": "The trail went cold."
        })

    weighted = sorted(
        related,
        key=lambda x: len(x),
        reverse=True
    )

    next_topic = random.choice(
        weighted[:min(5, len(weighted))]
    )

    response = {
        "title": wiki_data["title"],
        "summary": wiki_data["summary"],
        "next_topic": next_topic,
        "log": fake_system_log(
            topic,
            next_topic,
            len(path)
        )
    }

    return jsonify(response)


@app.route("/report", methods=["POST"])
def report():

    data = request.json

    path = data.get("path", [])

    return jsonify({
        "report": generate_conspiracy(path)
    })


if __name__ == "__main__":
    app.run(debug=True)
