function setValue(text) {
    const textarea = document.getElementById("comment-text");
    textarea.style.height = 0;
    textarea.value = text;
    textarea.style.height = textarea.scrollHeight + "px";
}

const textareaHeight = document.getElementById("comment-text");

textareaHeight.addEventListener("input", (event) => {
    textareaHeight.style.height = 0;
    textareaHeight.style.height = textareaHeight.scrollHeight + "px";
})