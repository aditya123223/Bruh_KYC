import React from "react";
import { Box, Card, Typography, CircularProgress } from "@mui/material";

function Result({ loading = true, message, videoPreview }) {
  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "linear-gradient(135deg, #eef2ff, #f8fafc)",
        p: 3,
      }}
    >
      <Card
        sx={{
          maxWidth: 600,
          width: "100%",
          borderRadius: 3,
          boxShadow: "0 6px 20px rgba(0,0,0,0.1)",
          p: 4,
          textAlign: "center",
        }}
      >
        <Typography variant="h5" fontWeight={600} gutterBottom>
          {message}
        </Typography>

        {videoPreview && (
          <video
            src={videoPreview}
            autoPlay
            loop
            muted={loading}
            controls={!loading}
            style={{
              width: "100%",
              height: "auto",
              borderRadius: 12,
              objectFit: "cover",
              marginBottom: 20,
            }}
          />
        )}

        {loading && (
          <CircularProgress
            sx={{ color: "#0070ba", mt: 2 }}
            size={60}
            thickness={5}
          />
        )}

        {!loading && (
          <Typography variant="body1" sx={{ mt: 2 }}>
            KYC submitted successfully!
          </Typography>
        )}
      </Card>
    </Box>
  );
}

export default Result;
