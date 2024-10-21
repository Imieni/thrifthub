// Get CSRF token from cookies
function getCSRFToken() {
    const cookieValue = document.cookie.match(/csrftoken=([^ ;]+)/);
    return cookieValue ? cookieValue[1] : null;
}

// Initialize Dropzone
Dropzone.autoDiscover = false;
const csrfToken = getCSRFToken();


// Configure Dropzone
var myDropzone = new Dropzone("#kt_ecommerce_add_product_media", {
    url: 'media/sales_images', // URL where files should be uploaded
    paramName: "file", // Name of the parameter used to send the file to the server
    maxFiles: 10, // Maximum number of files that can be uploaded
    maxFilesize: 2, // Maximum file size allowed (in MB)
    addRemoveLinks: true, // Show links to remove files from the queue
    acceptedFiles: 'image/*', // Accept only image files
    headers: {
        'X-CSRFToken': csrfToken // Include CSRF token in request headers
    },
    dictDefaultMessage: 'Drop files here or click to upload.', // Default message displayed in the Dropzone area
    dictMaxFilesExceeded: 'You have reached the maximum number of files.', // Message displayed when maximum files exceeded
    dictInvalidFileType: 'Invalid file type. Only images are allowed.', // Message displayed for invalid file type
    dictFileTooBig: 'File is too big. Maximum file size is 2 MB.' // Message displayed for files that exceed the maximum size
});

// Event handler for when a file is added
myDropzone.on("addedfile", function(file) {
    console.log("File added:", file);
});

// Event handler for when a file is removed
myDropzone.on("removedfile", function(file) {
    console.log("File removed:", file);
});
