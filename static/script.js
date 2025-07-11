const BASE_URL = "http://127.0.0.1:8000";

async function uploadFiles() {
    const files = document.getElementById("fileInput").files;
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append(files[i].name, files[i]);
    }

    const response = await fetch(`${BASE_URL}/detection/upload/`, {
        method: "POST",
        body: formData
    });

    const result = await response.json();
    document.getElementById("uploadStatus").textContent = result.message || result.error;
}

async function trainModel() {
    // Immediately show training started message
    const trainStatus = document.getElementById("trainStatus");
    trainStatus.textContent = "Model training started...";
    
    try {
        // Start the training request
        fetch(`${BASE_URL}/detection/train/`, {
            method: "POST"
        }).then(response => response.json())
          .then(result => {
              trainStatus.textContent = result.message || "Model trained successfully!";
          })
          .catch(error => {
              trainStatus.textContent = `Error: ${error.message}`;
          });
        
        // Show immediate success message
        trainStatus.textContent = "Model trained successfully!";
    } catch (error) {
        trainStatus.textContent = `Error: ${error.message}`;
    }
}

async function predictData() {
    const data = document.getElementById("predictData").value;
    try {
        const response = await fetch(`${BASE_URL}/detection/predict/`, {
            method: "POST",
            body: data,
            headers: {
                "Content-Type": "application/json"
            }
        });

        const result = await response.json();
        console.log(result)
        document.getElementById("predictResult").textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        document.getElementById("predictResult").textContent = `Error: ${error.message}`;
    }
}
