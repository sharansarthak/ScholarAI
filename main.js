document.addEventListener("DOMContentLoaded", function() {
    const videoLive = document.getElementById("videoLive");
    const videoRecorded = document.getElementById("videoRecorded");
    const buttonStart = document.getElementById("buttonStart");
    const buttonStop = document.getElementById("buttonStop");
    const buttonUpload = document.getElementById("buttonUpload"); // Add an upload button in your HTML
    let mediaRecorder;
    let recordedChunks = [];


    async function startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            videoLive.srcObject = stream;
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };
            mediaRecorder.onstop = () => {
                const videoBlob = new Blob(recordedChunks, { type: "video/mp4" });
                const videoURL = URL.createObjectURL(videoBlob);
                videoRecorded.src = videoURL;
                videoRecorded.style.display = "block";
            };
            mediaRecorder.start();
            buttonUpload.style.display = 'none'; // Hide upload button during recording

        } catch (error) {
            console.error("Error starting recording:", error);
        }
    }

    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
            videoLive.srcObject.getTracks().forEach(track => track.stop());
            videoLive.srcObject = null;
            recordedChunks = [];
        }
        buttonUpload.style.display = 'block'; // Show upload button after recording

    }
    function uploadVideo() {
        const videoBlob = new Blob(recordedChunks, { type: "video/mp4" });
        const formData = new FormData();
        formData.append("video", videoBlob, "interview.mp4");

        fetch('http://localhost:5000/upload_video', {  // Replace with your Flask server's URL
    method: 'POST',
    body: formData
})
        .then(response => response.json())
        .then(data => {
            console.log('Upload successful', data);
            console.log('Checking AI feedback:', data.ai_feedback);
        
            if (data.ai_feedback) {
                console.log('Displaying AI feedback');
                document.getElementById('aiFeedback').style.display = 'block';
                document.getElementById('feedbackText').innerHTML = data.ai_feedback;
            } else {
                console.log('No AI feedback found');
                document.getElementById('aiFeedback').style.display = 'none';
                document.getElementById('feedbackText').innerHTML = '';
            }
        })
        
    .catch(error => {
        console.error('Error in upload:', error);
        // Handle upload error here
        // Optionally hide or clear the feedback section
        document.getElementById('aiFeedback').style.display = 'none';
        document.getElementById('feedbackText').textContent = '';
    });
    }

    buttonStart.addEventListener("click", () => {
        startRecording();
        buttonStart.disabled = true;
        buttonStop.disabled = false;

    });

    buttonStop.addEventListener("click", () => {
        stopRecording();
        buttonStart.disabled = false;
        buttonStop.disabled = true;

    });
    buttonUpload.addEventListener("click", () => {
        uploadVideo();
    });
});