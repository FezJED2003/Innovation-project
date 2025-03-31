function getMovieTitle(){

let titleElement = document.querySelector(".previewModal--player-titleTreatment-logo") ||
document.querySelector(".video-title"); 

if(titleElement){

return titleElement.textContent.trim();
    
}
    return null;

}


setInterval(() => {
    let movieTitle = getMovieTitle();
    if (movieTitle) {
        console.log("Currently Watching:", movieTitle);
        chrome.runtime.sendMessage({ action: "fetchRecommendations", title: movieTitle });
    }
}, 5000);



const chatbotContainer = document.createElement("div");
chatbotContainer.id = "movieChatbot";

document.body.appendChild(chatbotContainer);


