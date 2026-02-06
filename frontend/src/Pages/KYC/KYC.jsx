import React, { useState } from "react";
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Stepper,
  Step,
  StepLabel,
  Button,
  Checkbox,
  FormControlLabel,
  Divider,
} from "@mui/material";
import GeneralInfo from "./GeneralInfo.jsx";
import VideoVerification from "./VideoVerification.jsx";
import Result from "./Result.jsx";

const steps = ["Identity Info", "Face Verification", "Confirmation"];

const KYC = () => {
  const [activeStep, setActiveStep] = useState(0);

  const [formData, setFormData] = useState({ name: "", age: "", gender: "" });
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [videoFile, setVideoFile] = useState(null);
  const [videoPreview, setVideoPreview] = useState(null);
  const [consent, setConsent] = useState(false);

  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((p) => ({ ...p, [name]: value }));
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setImageFile(file);

    const reader = new FileReader();
    reader.onloadend = () => setImagePreview(reader.result);
    reader.readAsDataURL(file);
  };

  const handleVideoUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setVideoFile(file);
    setVideoPreview(URL.createObjectURL(file));
  };

  const canProceedStep1 =
    formData.name && formData.age && formData.gender && imageFile;
  const canSubmit = canProceedStep1 && videoFile && consent;

  const handleSubmit = async () => {
    setLoading(true);

    // Simulate API call
    setTimeout(() => {
      setLoading(false);
      setSubmitted(true); // mark KYC as submitted
    }, 2000);
  };

  // Show Result component while submitting OR after submission
  if (loading) {
    return (
      <Result
        loading={true}
        message="Submitting your KYC..."
        videoPreview={videoPreview}
      />
    );
  }

  if (submitted) {
    return (
      <Result
        loading={false}
        message="KYC Submitted Successfully!"
        videoPreview={videoPreview}
      />
    );
  }

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
        }}
      >
        <CardContent sx={{ p: 4 }}>
          <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 4 }}>
            {steps.map((s) => (
              <Step key={s}>
                <StepLabel>{s}</StepLabel>
              </Step>
            ))}
          </Stepper>

          <Typography
            variant="h5"
            align="center"
            fontWeight={600}
            gutterBottom
            sx={{ mb: 3 }}
          >
            KYC Identity Enrollment
          </Typography>

          <Grid container spacing={3}>
            <Grid item xs={12}>
              {activeStep === 0 && (
                <GeneralInfo
                  formData={formData}
                  onChange={handleChange}
                  imagePreview={imagePreview}
                  onImageUpload={handleImageUpload}
                />
              )}
              {activeStep === 1 && (
                <VideoVerification
                  videoPreview={videoPreview}
                  onVideoUpload={handleVideoUpload}
                />
              )}
            </Grid>
          </Grid>

          <Divider sx={{ my: 3 }} />

          <FormControlLabel
            control={
              <Checkbox
                checked={consent}
                onChange={(e) => setConsent(e.target.checked)}
                sx={{ color: "#0070ba", "&.Mui-checked": { color: "#0070ba" } }}
              />
            }
            label="I confirm this identity belongs to me."
            sx={{ mb: 3 }}
          />

          <Box sx={{ textAlign: "center" }}>
            {activeStep < 1 ? (
              <Button
                variant="contained"
                disabled={!canProceedStep1}
                onClick={() => setActiveStep(1)}
                sx={{
                  backgroundColor: "#0070ba",
                  "&:hover": { backgroundColor: "#005ea3" },
                  textTransform: "none",
                  py: 1.5,
                  px: 5,
                  borderRadius: 2,
                }}
              >
                Continue
              </Button>
            ) : (
              <Button
                variant="contained"
                disabled={!canSubmit}
                onClick={handleSubmit}
                sx={{
                  backgroundColor: "#0070ba",
                  "&:hover": { backgroundColor: "#005ea3" },
                  textTransform: "none",
                  py: 1.5,
                  px: 5,
                  borderRadius: 2,
                }}
              >
                Submit KYC
              </Button>
            )}
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default KYC;
