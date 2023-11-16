import React, { useState, useEffect } from 'react';

const InterviewPage = () => {
  const [recording, setRecording] = useState(false);
  const [globalStream, setGlobalStream] = useState(null);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [recordedChunks, setRecordedChunks] = useState([]);
  const [videoURL, setVideoURL] = useState('');

  const initVideoStream = async () => {
    try {
      setGlobalStream(await navigator.mediaDevices.getUserMedia({ video: true, audio: true }));
    } catch (error) {
      console.error("Error accessing media devices:", error);
      // Handle the error appropriately
    }
  };

  const startRecording = async () => {
    try {
      setRecordedChunks([]);
      
      // Ensure globalStream is initialized before proceeding
      if (!globalStream) {
        await initVideoStream();
      }

      // Double-check if globalStream is now available
      if (globalStream) {
        const mediaRecorderInstance = new MediaRecorder(globalStream);
        setMediaRecorder(mediaRecorderInstance);

        mediaRecorderInstance.ondataavailable = event => {
          if (event.data.size > 0) {
            setRecordedChunks(prevChunks => [...prevChunks, event.data]);
          }
        };

        mediaRecorderInstance.onstop = () => {
          const videoBlob = new Blob(recordedChunks, { type: "video/mp4" });
          const blobURL = URL.createObjectURL(videoBlob);
          setVideoURL(blobURL);
          document.getElementById("videoRecorded").src = blobURL;
        };

        mediaRecorderInstance.start();
        document.getElementById("buttonUpload").style.display = 'none';
        document.getElementById("videoRecorded").style.display = 'none';
        document.getElementById("videoLive").style.display = 'block';
      } else {
        console.error("globalStream is still not available");
      }
    } catch (error) {
      console.error("Error starting recording:", error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
      globalStream.getTracks().forEach(track => track.stop());
      setGlobalStream(null);
      document.getElementById("videoLive").style.display = 'none';
    }
    document.getElementById("buttonUpload").style.display = 'block';
  };

  const uploadVideo = () => {
    const formData = new FormData();
    recordedChunks.forEach((chunk, index) => {
      formData.append(`chunk${index}`, chunk);
    });

    fetch('http://localhost:5000/upload_video', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        console.log('Upload successful', data);
        console.log('Checking AI feedback:', data.ai_feedback);
      })
      .catch(error => {
        console.error('Error in upload:', error);
      });
  };

  useEffect(() => {
    const videoLive = document.getElementById("videoLive");
    const videoRecorded = document.getElementById("videoRecorded");
    const buttonStart = document.getElementById("buttonStart");
    const buttonStop = document.getElementById("buttonStop");
    const buttonUpload = document.getElementById("buttonUpload");

    if (buttonStart && buttonStop && buttonUpload) {
      buttonStart.addEventListener("click", startRecording);
      buttonStop.addEventListener("click", stopRecording);
      buttonUpload.addEventListener("click", uploadVideo);
    }

    return () => {
      if (globalStream) {
        globalStream.getTracks().forEach(track => track.stop());
      }
    };
  }, [globalStream, mediaRecorder, recordedChunks]);


  return (
    <div style={{ fontFamily: 'Roboto', backgroundColor: '#f4f4f4', display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100vh', margin: 0 }}>
      <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)', textAlign: 'center', maxWidth: '600px' }}>
        <h2>Practice Interview Recorder</h2>
        <div style={{ backgroundColor: '#e9ecef', padding: '15px', marginBottom: '20px', borderRadius: '8px' }}>
          <p>Here is your interview question:</p>
          <p><strong>Q: Tell us about the biggest challenge you've ever faced</strong></p>
        </div>
        <div style={{ marginBottom: '15px' }}>
          <video autoPlay muted playsInline id="videoLive" style={{ width: '100%', borderRadius: '5px' }}></video>
          <video controls playsInline id="videoRecorded" style={{ display: 'none', width: '100%', borderRadius: '5px' }}></video>
        </div>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', marginBottom: '20px' }}>
          <button type="button" onClick={startRecording} style={{ backgroundColor: '#007bff', color: 'white', border: 'none', padding: '10px 15px', borderRadius: '5px', cursor: 'pointer', fontSize: '16px', transition: 'background-color 0.3s' }} disabled={recording}>
            {recording ? 'Recording...' : 'Start Recording'}
          </button>
          <button type="button" onClick={stopRecording} style={{ backgroundColor: '#007bff', color: 'white', border: 'none', padding: '10px 15px', borderRadius: '5px', cursor: 'pointer', fontSize: '16px', transition: 'background-color 0.3s' }} disabled={!recording}>
            Stop Recording
          </button>
          <button type="button" onClick={uploadVideo} style={{ backgroundColor: '#007bff', color: 'white', border: 'none', padding: '10px 15px', borderRadius: '5px', cursor: 'pointer', fontSize: '16px', transition: 'background-color 0.3s' }}>
            Upload Video
          </button>
        </div>
        <div style={{ color: '#d35400', fontSize: '1.2em', textAlign: 'center', marginTop: '10px' }}>
          <h3>Answer Time Limit: 2 Minutes</h3>
        </div>

        <div style={{ backgroundColor: '#f9f9f9', border: '1px solid #ddd', borderRadius: '4px', padding: '20px', marginTop: '20px', textAlign: 'left' }}>
          <p>AI Feedback:</p>
          <p id="feedbackText"></p>
        </div>
      </div>
    </div>
  );
}

export default InterviewPage;
