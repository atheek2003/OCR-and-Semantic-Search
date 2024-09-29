document.getElementById('upload-form').onsubmit = function(e) {
    e.preventDefault();
    var formData = new FormData();
    var fileInput = document.getElementById('file-input');
    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('results').innerHTML = `
            <h3>Extracted Text</h3>
            <p>${data.ocr_text}</p>
            <h3>Detected Language</h3>
            <p>${data.language}</p>
            <h3>Image Caption</h3>
            <p>${data.caption}</p>
        `;
        document.getElementById('search-container').style.display = 'block';
    })
    .catch(err => {
        console.error(err);
        alert('Error processing the image');
    });
};

function performSearch() {
    var query = document.getElementById('search-input').value;
    var text = document.getElementById('results').querySelector('p').innerText;
    
    fetch('/search', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({query: query, text: text})
    })
    .then(response => response.json())
    .then(data => {
        var resultsHtml = data.map(item => `<p>${item[0]} (Score: ${item[1].toFixed(2)})</p>`).join('');
        document.getElementById('search-results').innerHTML = resultsHtml;
    })
    .catch(err => {
        console.error(err);
        alert('Error performing search');
    });
}
