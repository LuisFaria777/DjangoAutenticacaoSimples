// scripts.js

document.addEventListener("DOMContentLoaded", function() {
    console.log("Page loaded");

    const button = document.querySelector("button");

    if (button) {
        button.addEventListener("click", function() {
            alert("Button clicked!");
        });
    }
});
