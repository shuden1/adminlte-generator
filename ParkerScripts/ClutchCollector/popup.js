document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('start').addEventListener('click', function() {
        chrome.runtime.sendMessage({action: "start"});
    });
    document.getElementById('downloadButton').addEventListener('click', function() {
        chrome.runtime.sendMessage({action: "download"});
    });
});

