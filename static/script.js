let threadId = null;

const topic = document.getElementById("topic");
const submitBtn = document.getElementById("submitBtn");
const buttonText = document.getElementById("buttonText");
const buttonIcon = document.getElementById("buttonIcon");

const status = document.getElementById("status");
const result = document.getElementById("result");

const resultSection =
    document.getElementById("resultSection");

const researchStatus =
    document.getElementById("researchStatus");

const progressBar =
    document.getElementById("progressBar");

const charCount =
    document.getElementById("charCount");

const errorBox =
    document.getElementById("errorBox");

const errorMessage =
    document.getElementById("errorMessage");


/* Character Counter */

topic.addEventListener("input", () => {

    const length = topic.value.length;

    charCount.textContent =
        `${length} / 1000`;

});


/* Example Topics */

document.querySelectorAll(".example-chip")
    .forEach(button => {

        button.addEventListener("click", () => {

            topic.value =
                button.dataset.topic;

            topic.dispatchEvent(
                new Event("input")
            );

            topic.focus();

        });

    });


/* Run Research */

async function runResearch() {

    const userTopic =
        topic.value.trim();


    if (!userTopic) {

        showError(
            "Please enter a research topic before starting."
        );

        topic.focus();

        return;
    }


    setLoading(true);

    hideError();

    resultSection.classList.add("hidden");

    researchStatus.classList.remove("hidden");


    updateProgress(
        10,
        "Searching academic sources...",
        "progressSearch"
    );


    try {

        /*
         * Small visual delay so users can see
         * the research stages.
         */

        setTimeout(() => {

            updateProgress(
                35,
                "Analyzing research papers...",
                "progressAnalyze"
            );

        }, 1200);


        setTimeout(() => {

            updateProgress(
                60,
                "Comparing methodologies...",
                "progressCompare"
            );

        }, 2500);


        setTimeout(() => {

            updateProgress(
                80,
                "Identifying research gaps...",
                "progressGap"
            );

        }, 3800);


        const response =
            await fetch(
                "/api/research",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: userTopic,
                        thread_id: threadId
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                `Server error (${response.status})`
            );

        }


        const data =
            await response.json();


        if (!data.success) {

            throw new Error(
                data.error ||
                "Research agent failed."
            );

        }


        /*
         * Save conversation thread
         */

        threadId =
            data.thread_id;


        /*
         * Complete progress
         */

        updateProgress(
            100,
            "Research completed successfully.",
            "progressGap"
        );


        /*
         * Display statistics
         */

        document.getElementById(
            "papersFound"
        ).textContent =
            data.papers_found?.length ||
            data.papers_found ||
            0;


        document.getElementById(
            "llmCalls"
        ).textContent =
            data.llm_calls || 0;


        /*
         * Display answer
         */

        result.textContent =
            data.answer || 
            "No research report was generated.";


        /*
         * Show result
         */

        setTimeout(() => {

            researchStatus.classList.add(
                "hidden"
            );

            resultSection.classList.remove(
                "hidden"
            );

            resultSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }, 500);


    } catch (error) {

        console.error(
            "Research Error:",
            error
        );


        researchStatus.classList.add(
            "hidden"
        );


        showError(
            error.message ||
            "Unable to complete research."
        );


    } finally {

        setLoading(false);

    }

}


/* Loading State */

function setLoading(isLoading) {

    submitBtn.disabled =
        isLoading;


    if (isLoading) {

        buttonIcon.textContent =
            "◌";

        buttonText.textContent =
            "Researching...";

    } else {

        buttonIcon.textContent =
            "✦";

        buttonText.textContent =
            "Run Research Agent";

    }

}


/* Progress */

function updateProgress(
    percentage,
    message,
    activeId
) {

    progressBar.style.width =
        `${percentage}%`;

    status.textContent =
        message;


    const progressItems =
        document.querySelectorAll(
            ".agent-progress span"
        );


    progressItems.forEach(item => {

        item.classList.remove(
            "active"
        );

    });


    if (activeId) {

        const active =
            document.getElementById(
                activeId
            );

        if (active) {

            active.classList.add(
                "active"
            );

            active.textContent =
                active.textContent.replace(
                    "○",
                    "✓"
                );

        }

    }

}


/* Error */

function showError(message) {

    errorMessage.textContent =
        message;

    errorBox.classList.remove(
        "hidden"
    );

}


function hideError() {

    errorBox.classList.add(
        "hidden"
    );

}


/* Copy Report */

async function copyResult() {

    const text =
        result.textContent;


    if (!text) return;


    try {

        await navigator.clipboard.writeText(
            text
        );


        const button =
            document.querySelector(
                ".copy-button"
            );


        const original =
            button.textContent;


        button.textContent =
            "✓ Copied";


        setTimeout(() => {

            button.textContent =
                original;

        }, 1800);


    } catch (error) {

        console.error(
            "Copy failed:",
            error
        );

    }

}


/* Keyboard Shortcut */

topic.addEventListener(
    "keydown",
    event => {

        /*
         * Ctrl + Enter
         */

        if (
            event.ctrlKey &&
            event.key === "Enter"
        ) {

            runResearch();

        }

    }
);