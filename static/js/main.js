let loadInfoData = [];
let responseMessageData = [];

// Handle form submission time and fetch response
let timerInterval;
let startTime;
let apiCallTime;
let controller; // Controller for aborting fetch request
let apiCallSeconds;

// Handle form submission, including loader, timer, and cancel functionality
function submitCommand(event) {
event.preventDefault(); 

// Start loading spinner and timer
startLoading();

// Get the current time and form data
startTime = new Date().getTime();
const currentTime = new Date().toISOString();
document.getElementById('submissionTime').value = currentTime;
const formData = new FormData(document.getElementById('inputForm'));

// Create an AbortController for this request
controller = new AbortController();
const signal = controller.signal;

// Fetch API call with AbortController
fetch('/', {
method: 'POST',
body: formData,
signal: signal,  // Attach the signal to the fetch request
})
.then(response => {
console.log("...........RESPONSE ",response);

apiCallTime = new Date().getTime() - startTime; // Capture API call time
return response.json();
})
.then(data => {
console.log("DATA ",data);
// Stop loader and timer once the response is received
stopLoading();

// Process and display the results
loadInfoData = data.load_info_data || [];
responseMessageData = data.response_message || [];
populateResultsTable(responseMessageData); // Populate the table with results
})
.catch(error => {
if (error.name === 'AbortError') {
    console.log('Request was cancelled');
} else {
    console.error('Error:', error);
}
stopLoading(); // Ensure to stop loader and timer even on error
});
}

// Function to start loader and timer
function startLoading() {
document.getElementById('loader').style.display = 'inline-block'; // Show loader
document.getElementById('timer').style.display = 'block';          // Show timer
document.getElementById('cancelButton').style.display = 'inline-block'; // Show cancel button

// Start timer
let elapsedSeconds = 0;
timerInterval = setInterval(() => {
elapsedSeconds++;
document.getElementById('timeElapsed').textContent = elapsedSeconds;
}, 100);

// Add event listener to cancel button
document.getElementById('cancelButton').addEventListener('click', cancelRequest);
}

// Function to stop loader and timer
function stopLoading() {
document.getElementById('loader').style.display = 'none';  // Hide loader
document.getElementById('timer').style.display = 'none';   // Hide timer
document.getElementById('cancelButton').style.display = 'none';  // Hide cancel button
clearInterval(timerInterval);  // Stop timer

// Calculate total time and display (API call time vs total time)
const totalTime = (new Date().getTime() - startTime) / 1000;
apiCallSeconds = apiCallTime / 1000;
result_time = document.getElementById("result_time").textContent = `Results(with in (${apiCallSeconds})):`
console.log(`Total Time: ${totalTime} seconds (API Call Time: ${apiCallSeconds} seconds)`);
}

// Function to cancel the request
function cancelRequest() {
controller.abort();  // Abort the fetch request
stopLoading();  // Stop the loader and timer
}


function populateResultsTable(data) {
const tableBody = document.getElementById('table');

// Clear the previous content (for testing, let's avoid clearing it for now)
tableBody.innerHTML = ''; 

// Test if the tableBody element is correctly targeted
if (!tableBody) {
console.error("Table body element not found.");
return;
} else {
console.log("Table body found");
}

// Test if data is available
if (!data || data.length === 0) {
console.error("No data available to populate the table.");
return;
}


// Construct the rows and assign them using innerHTML
let rows = '';
data.forEach(result => {
console.log(result);  // Make sure data is logged
rows += `
    <tr>
        <td>${result.text_item}</td>
        <td>${(result.similarity * 100).toFixed(2)}%</td>
        <td>${result.row_number}</td>
        <td>${result.paragraph}</td>
        <td>${result.char_start_pos}</td>
        <td><button class="btn btn-info view-record-btn" data-full-text="${result.full_text}">View</button></td>
    </tr>
`;
});


// Update the table's innerHTML
tableBody.insertAdjacentHTML('beforeend', rows);

// Attach event listeners to the new "View" buttons
document.querySelectorAll('.view-record-btn').forEach(button => {
button.addEventListener('click', function() {
    const fullText = this.getAttribute('data-full-text');
    document.getElementById('fullTextContent').textContent = fullText;
    document.getElementById('fullTextPopup').style.display = 'flex';
});
});
}

// Toggle AI Command Section

function aicommandClick(){
    const aiCommandDiv = document.getElementById('aiCommandDiv');
    if (aiCommandDiv.style.display === 'none' || aiCommandDiv.style.display === '') {
        aiCommandDiv.style.display = 'block';
        aiCommandButton.textContent = 'Cancel AI Command';
    } else {
        aiCommandDiv.style.display = 'none';
        aiCommandButton.textContent = 'AI Command';
    }
}










// SUBMIT AI COMMAND
    
    function  submitAICommand() {
        startLoading();
    const aiCommandInput = document.getElementById('aiCommandInput').value;
    fetch('/submit-ai-command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: aiCommandInput }),
    })
    .then(response => response.json())
    .then(data => {
        const aiCommandResponse = document.getElementById('aiCommandResponse');
        aiCommandResponse.innerHTML = `<div class="alert alert-info">Response: ${data.response}</div>`;
    })
    .catch(error => console.error('Error:', error)).finally(function(){
        stopLoading(); 

    });
};











// Load info popup trigger
    
    function loadInfoButton() {
    document.getElementById('loadInfoPopup').style.display = 'flex';
    const tableBody = document.getElementById('loadInfoTableBody');
    tableBody.innerHTML = '';  // Clear previous content

    // Populate the table with load info data
    loadInfoData.forEach(item => {
        const row = `<tr><td>${item.text}</td><td>${item.instances}</td></tr>`;
        tableBody.insertAdjacentHTML('beforeend', row);
    });
};






// Close load info popup
    
function  closeLoadInfo() {
    document.getElementById('loadInfoPopup').style.display = 'none';
};



// Close full text popup
    
    function closeFullText() {
    document.getElementById('fullTextPopup').style.display = 'none';
};
