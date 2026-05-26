const terminal = document.getElementById("terminal");
const input = document.getElementById("cmd");

let currentTopic = "";
let nextTopic = "";
let path = [];

let state = "START";


function addLine(text, className="") {

    const div = document.createElement("div");

    div.className = className;

    div.textContent = text;

    terminal.appendChild(div);

    terminal.scrollTop = terminal.scrollHeight;
}


async function runStep(topic) {

    state = "WAITING";

    const res = await fetch("/rabbit-hole", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            topic: topic,
            path: path
        })
    });

    const data = await res.json();

    if (data.error) {

        addLine(data.error);

        return;
    }

    path.push(topic);

    addLine("");
    addLine("================================================");
    addLine(`TOPIC: ${data.title}`);
    addLine("================================================");
    addLine(data.summary);
    addLine("================================================");

    addLine("");
    addLine(`'${topic}' connects to '${data.next_topic}'`);

    if (Math.random() > 0.4) {
        addLine(data.log, "system-log");
    }

    nextTopic = data.next_topic;

    addLine("");
    addLine("GO DEEPER? (y/n)");

    state = "CHOICE";
}


async function getReport() {

    const res = await fetch("/report", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            path: path
        })
    });

    const data = await res.json();

    addLine("");
    addLine("CLASSIFIED PATTERN REPORT");
    addLine("================================================");

    addLine(data.report, "report");
}


input.addEventListener("keydown", async (e) => {

    if (e.key !== "Enter") return;

    const val = input.value.trim();

    input.value = "";

    addLine(`> ${val}`);

    if (state === "START") {

        currentTopic = val;

        runStep(currentTopic);
    }

    else if (state === "CHOICE") {

        if (val.toLowerCase() === "y") {

            currentTopic = nextTopic;

            runStep(currentTopic);
        }

        else {

            await getReport();

            addLine("");
            addLine("You escaped the rabbit hole.");

            input.disabled = true;
        }
    }
});


addLine("RABBIT HOLE TERMINAL");
addLine("====================");
addLine("ENTER STARTING TOPIC");