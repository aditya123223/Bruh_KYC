import React, { useState, useRef, useEffect } from "react";
import { Box, Button, Typography } from "@mui/material";

const VideoVerification = ({ videoPreview, onVideoUpload }) => {
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const recordedChunksRef = useRef([]);
  const videoRef = useRef();
  const [stream, setStream] = useState(null);

  // Clean up stream on unmount
  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [stream]);

  const startRecording = async () => {
    try {
      const userStream = await navigator.mediaDevices.getUserMedia({
        video: { width: 1280, height: 720 },
        audio: true,
      });
      setStream(userStream);
      videoRef.current.srcObject = userStream;
      videoRef.current.play();

      recordedChunksRef.current = [];
      const mediaRecorder = new MediaRecorder(userStream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) recordedChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(recordedChunksRef.current, { type: "video/mp4" });
        const videoURL = URL.createObjectURL(blob);
        onVideoUpload({ target: { files: [blob], preview: videoURL } });

        // Stop all tracks
        userStream.getTracks().forEach((track) => track.stop());
        setStream(null);
      };

      mediaRecorder.start();
      setRecording(true);
    } catch (err) {
      console.error("Camera access denied:", err);
      alert("Camera access is required to record video.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) mediaRecorderRef.current.stop();
    setRecording(false);
  };

  return (
    <Box
      sx={{
        width: "100%",
        display: "flex",
        flexDirection: "column",
        gap: 3,
        p: 3,
      }}
    >
      <Box
        sx={{
          width: "100%",
          border: "2px dashed #90a4ae",
          borderRadius: 3,
          backgroundColor: "#f9fafb",
          position: "relative",
          overflow: "hidden",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          minHeight: 400,
        }}
      >
        <video
          ref={videoRef}
          src={videoPreview || undefined} // if there's recorded video, play it
          autoPlay
          muted={!videoPreview} // mute live stream
          controls={!!videoPreview} // show controls only for recorded video
          playsInline
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            borderRadius: 8,
          }}
        />

        {!recording && !videoPreview && (
          <Typography
            sx={{
              position: "absolute",
              color: "#607d8b",
              textAlign: "center",
            }}
          >
            Tap "Start Recording" to capture your verification video
          </Typography>
        )}
      </Box>

      <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
        {!recording ? (
          <Button
            variant="contained"
            onClick={startRecording}
            sx={{
              backgroundColor: "#0070ba",
              "&:hover": { backgroundColor: "#005ea3" },
              color: "#fff",
              textTransform: "none",
              py: 1.5,
              borderRadius: 2,
            }}
          >
            Start Recording
          </Button>
        ) : (
          <Button
            variant="contained"
            onClick={stopRecording}
            sx={{
              backgroundColor: "#d32f2f",
              "&:hover": { backgroundColor: "#b71c1c" },
              color: "#fff",
              textTransform: "none",
              py: 1.5,
              borderRadius: 2,
            }}
          >
            Stop Recording
          </Button>
        )}

        <Typography color="text.secondary">
          Record a short video to verify your identity. Supported on mobile and
          desktop webcams.
        </Typography>
      </Box>
    </Box>
  );
};

export default VideoVerification;
