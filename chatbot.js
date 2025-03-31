document.addEventListener("DOMContentLoaded", async function () {
    const chatbox = document.getElementById("chatbox");

    
    auth.onAuthStateChanged(async (user) => {
        if (user) {
            const userPreferences = await getUserPreferences();
            if (userPreferences.length > 0) {
                displayBotMessage("Welcome back! Your favorite genres: " + userPreferences.join(", "));
            } else {
                displayBotMessage("Hi! What movie genres do you like?");
            }
        } else {
            displayBotMessage("Please log in to get personalized recommendations.");
        }
    });

    document.getElementById("userInputBtn").addEventListener("click", function () {
        let userInput = document.getElementById("textInput").value.trim();
        if (userInput) {
            displayUserMessage(userInput);
            handleChatbotResponse(userInput);
            document.getElementById("textInput").value = "";
        }
    });

    async function handleChatbotResponse(input) {
        if (input.toLowerCase().includes("recommend")) {
            const recommendations = await fetchRecommendations();
            displayBotMessage("Here are some movies: " + recommendations.join(", "));
        } else if (input.toLowerCase().includes("watchlist")) {
            const watchlist = await getWatchlist();
            displayBotMessage("Your watchlist: " + (watchlist.length > 0 ? watchlist.join(", ") : "No movies added yet."));
        } else {
            displayBotMessage("I didn't understand that. Try asking for recommendations.");
        }
    }
});

function displayUserMessage(msg) {
    const chatbox = document.getElementById("chatbox");
    const bubble = document.createElement("div");
    bubble.className = "speech-bubble-user";
    bubble.innerHTML = msg;
    chatbox.appendChild(bubble);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function displayBotMessage(msg) {
    const chatbox = document.getElementById("chatbox");
    const bubble = document.createElement("div");
    bubble.className = "speech-bubble-bot";
    bubble.innerHTML = msg;
    chatbox.appendChild(bubble);
    chatbox.scrollTop = chatbox.scrollHeight;
}


async function fetchRecommendations() {
    return ["Inception", "Interstellar", "The Matrix"];
}
