   
    // Function to set the selected option
    var storedOption = localStorage.getItem("selectedOption") || 'tokens';

    function setOption(option) {
        localStorage.setItem('selectedOption', option);  
        // location.reload();  
        storedOption = localStorage.getItem("selectedOption") || 'tokens';
        console.log(storedOption);
        updateDropdownLabel(storedOption);

        // Make a request to the current URL
        
        // Retrieve the selected option from localStorage
        storedOption = localStorage.getItem("selectedOption") || 'tokens';
        
        // Create a new URL with the model parameter
        const updatedHref =  "?model=" + storedOption;
        console.log(this.href);
        // Update the window location only after setting the href correctly
        window.location.href = updatedHref;

    }
    
        // Function to update the dropdown label
        function updateDropdownLabel(option) {
            document.getElementById("dropdownLabel").innerText = option.charAt(0).toUpperCase() + option.slice(1);
            // document.getElementById("selectedOption").innerText = "Selected Option: " + option; // Update selected option text
        }
    
        // Function to update the URL with the selected model parameter
        function updateUrlModel(option) {
            const url = new URL(window.location);
            url.searchParams.set('model', option); // Set or update the 'model' parameter
            window.history.replaceState({}, '', url); // Update the URL without reloading the page
        }
    
        // Function to initialize the model value if not present
        function initializeModel() {
            const url = new URL(window.location);
            let model = url.searchParams.get('model');
    
            if (!model) {
                model = storedOption; // Default value
                url.searchParams.set('model', model);
                window.history.replaceState({}, '', url); // Update the URL without reloading the page
            }
            updateDropdownLabel(model); // Update dropdown label based on the model
        }




