import React from 'react';

class InterviewPage extends React.Component {
  constructor(props) {
    super(props);
    
    // Refs for video elements
    this.videoLive = React.createRef();
    this.videoRecorded = React.createRef();

    // Binding methods to 'this' context
    this.initVideoStream = this.initVideoStream.bind(this);
    this.startRecording = this.startRecording.bind(this);
    this.stopRecording = this.stopRecording.bind(this);
    this.uploadVideo = this.uploadVideo.bind(this);

    // Initialize state
    this.state = {
        isRecording: false,            // To track if recording is in progress
        isUploadButtonVisible: false,  // To control the visibility of the upload button
        aiFeedback: '',                // To store AI feedback
        error: null,                   // To handle any errors
        stream: null,                  // To store the media stream
        mediaRecorder: null,           // To reference the MediaRecorder instance
        recordedChunks: [],            // To store the recorded video chunks
        showAiFeedback: false          // To control the display of AI feedback
    };
}


  componentDidMount() {
      this.initVideoStream();
  }

  initVideoStream = async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        
        // Use the ref to set the stream to the video element
        if (this.videoLive.current) {
            this.videoLive.current.srcObject = stream;
        }

        // Update the component's state, e.g., to indicate that the stream is ready
        this.setState({
            isStreamReady: true,
            error: null
        });

        return stream;
    } catch (error) {
        console.error("Error accessing media devices:", error);
        
        // Update the component's state to handle the error
        this.setState({
            isStreamReady: false,
            error: error.message // Storing the error message in the state
        });

        return null;
    }
}


startRecording = async () => {
  try {
    let stream = this.state.stream;

    // Check if the stream is not already active
    if (!stream || stream.getTracks().every(track => track.readyState === 'ended')) {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        this.setState({ stream });
    }

    if (this.videoLive.current) {
        this.videoLive.current.srcObject = stream;
        this.videoLive.current.style.display = 'block'; // Ensure the live feed is visible
    }

    // Initialize MediaRecorder with the stream
    const mediaRecorder = new MediaRecorder(this.state.stream);
    let recordedChunks = [];

      // Event handler for when data is available
      mediaRecorder.ondataavailable = event => {
          if (event.data.size > 0) {
              recordedChunks.push(event.data);
          }
      };

      // Event handler for when recording stops
      mediaRecorder.onstop = () => {
          const videoBlob = new Blob(recordedChunks, { type: "video/mp4" });
          const videoURL = URL.createObjectURL(videoBlob);
          if (this.videoRecorded.current) {
              this.videoRecorded.current.src = videoURL;
              this.videoRecorded.current.style.display = "block";
          }
      };

      // Start recording
      mediaRecorder.start();

      // Update component state
      this.setState({
          mediaRecorder,
          isRecording: true,
          isUploadButtonVisible: false
      });
  } catch (error) {
      console.error("Error starting recording:", error);
      this.setState({ error: error.message });
  }
};


stopRecording = () => {
  // Check if the mediaRecorder is currently recording
  if (this.state.mediaRecorder && this.state.mediaRecorder.state === "recording") {
      // Stop the media recorder
      this.state.mediaRecorder.stop();

      // Stop all media tracks in the stream
      if (this.state.stream) {
          this.state.stream.getTracks().forEach(track => track.stop());
      }

      // Update component state to reflect changes
      this.setState({
          isRecording: false,
          isUploadButtonVisible: true,
          // Do not clear the stream here; keep it for reuse
      });

      // If using refs to manage DOM elements
      if (this.videoLive.current) {
          this.videoLive.current.srcObject = null;
          this.videoLive.current.style.display = 'none';
      }
  }
};
uploadVideo = () => {
  // Assuming 'recordedChunks' is stored in the component's state
  const videoBlob = new Blob(this.state.recordedChunks, { type: "video/mp4" });
  const formData = new FormData();
  formData.append("video", videoBlob, "interview.mp4");

  // Fetch API call
  fetch('http://localhost:5000/upload_video', {
    method: 'POST',
    body: formData
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
})
.then(data => {
    console.log('Upload successful', data);
    console.log('Checking AI feedback:', data.ai_feedback); 

    if (data.ai_feedback) {
        console.log('Displaying AI feedback');
        this.setState({
            aiFeedback: data.ai_feedback,
            showAiFeedback: true
        });
    } else {
        console.log('No AI feedback found');
        this.setState({
            aiFeedback: '',
            showAiFeedback: false
        });
    }this.setState({
        recordedChunks: [],
    });
})

.catch(error => {
    console.error('Error in upload:', error);
    this.setState({
        error: error.message,
        showAiFeedback: false
    });
});
};

render() {
  const { isRecording, isUploadButtonVisible, aiFeedback, showAiFeedback } = this.state;

  return (
      <div className="container">
          <h2>Practice Interview Recorder</h2>
          <div className="question-section">
              <p>Here is your interview question:</p>
              <p><strong>Q: Tell us about the biggest challenge you've ever faced</strong></p>
          </div>
          <div className="video-container">
              <video autoPlay muted playsInline ref={this.videoLive}></video>
              <video controls playsInline ref={this.videoRecorded} style={{ display: 'none' }}></video>
          </div>
        
          <div className="controls">
                {!isRecording && (
                    <button 
                        type="button" 
                        className="button start" 
                        onClick={this.startRecording}
                    >
                        Start Recording
                    </button>
                )}
                {isRecording && (
                    <button 
                        type="button" 
                        className="button stop" 
                        onClick={this.stopRecording}
                    >
                        Stop Recording
                    </button>
                )}
                {isUploadButtonVisible && (
                    <button 
                        type="button" 
                        className="button" 
                        onClick={this.uploadVideo}
                    >
                        Submit Video
                    </button>
                )}
          </div>
          <div className="time-indicator">
              <h3>Answer Time Limit: 2 Minutes</h3>
          </div>
          {showAiFeedback && (
              <div className="answer-section" id="aiFeedback">
                  <p>AI Feedback:</p>
                  <div dangerouslySetInnerHTML={{ __html: aiFeedback }} />
              </div>
          )}
      </div>
  );
}
}
export default InterviewPage;
