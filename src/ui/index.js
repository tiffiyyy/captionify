import addOnUISdk from "https://new.express.adobe.com/static/add-on-sdk/sdk.js";

addOnUISdk.ready.then(async () => {
    console.log("addOnUISdk is ready for use.");

    // Get the UI runtime.
    const { runtime } = addOnUISdk.instance;

    // Get the proxy object, which is required
    // to call the APIs defined in the Document Sandbox runtime
    // i.e., in the `code.js` file of this add-on.
    const sandboxProxy = await runtime.apiProxy("documentSandbox");

    const createRectangleButton = document.getElementById("createRectangle");
    createRectangleButton.addEventListener("click", async event => {
        await sandboxProxy.createRectangle();
    });

    const videoInput = document.getElementById('video-upload');
    const fileNameDisplay = document.getElementById('file-name');

    videoInput.addEventListener('change', function(event) {
        //await sandboxProxy.
        const selectedFile = event.target.files[0];
        console.log(selectedFile);


        if (selectedFile) {
            fileNameDisplay.textContent = `Selected Video: ${selectedFile.name}`;
          } else {
            fileNameDisplay.textContent = ''; // Clear it if no file
          }
    });

    const formData = new FormData();
    formData.append('video', fileInput.files[0]);

    fetch('https://18ae-129-210-115-230.ngrok-free.app/uploads/', {
        method: 'POST',
        body: formData
    })
    .then(r => r.text())
    .then(console.log("success"))
    .catch(error => console.error("Error uploading:", error));

    // Enable the button only when:
    // 1. `addOnUISdk` is ready,
    // 2. `sandboxProxy` is available, and
    // 3. `click` event listener is registered.
    createRectangleButton.disabled = false;
});
