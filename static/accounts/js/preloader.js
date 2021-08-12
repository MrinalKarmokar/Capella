// Used dor showing black screen before video loads in background

window.addEventListener("load", function(){
    const loader = document.querySelector(".loading");
    loader.className += " hidden";
});