import React, { useState } from "react";
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  MenuItem,
  Grid,
  Stepper,
  Step,
  StepLabel,
  Checkbox,
  FormControlLabel,
  Alert,
  Divider,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

const steps = ["Identity Info", "Face Verification", "Confirmation"];

const KYC = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    age: "",
    gender: "",
  });

  const [preview, setPreview] = useState(null);
  const [consent, setConsent] = useState(false);

  // -------------------------
  // handlers
  // -------------------------

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onloadend = () => setPreview(reader.result);
    reader.readAsDataURL(file);
  };

  const isFormValid =
    formData.name &&
    formData.age &&
    formData.gender &&
    preview &&
    consent;

  const handleProceed = () => {
    if (!isFormValid) return;

    // navigate to webcam verification page
    navigate("/verify-camera");
  };

  // -------------------------
  // UI
  // -------------------------

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "linear-gradient(135deg, #eef2ff, #f8fafc)",
        padding: 3,
      }}
    >
      <Card sx={{ width: "100%", maxWidth: 1100, borderRadius: 4, boxShadow: 6 }}>
        <CardContent>

          {/* Step indicator */}
          <Stepper activeStep={0} sx={{ mb: 3 }}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>

          <Typography variant="h4" align="center" fontWeight="bold" gutterBottom>
            KYC Identity Enrollment
          </Typography>

          {/* Fraud warning */}
          <Alert severity="warning" sx={{ mb: 2 }}>
            Duplicate or spoof identity attempts will be automatically rejected.
          </Alert>

          <Grid container spacing={4}>

            {/* LEFT — FORM */}
            <Grid item xs={12} md={6}>
              <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>

                <TextField
                  label="Full Name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  fullWidth
                  required
                />

                <TextField
                  label="Age"
                  name="age"
                  type="number"
                  value={formData.age}
                  onChange={handleChange}
                  fullWidth
                  required
                />

                <TextField
                  select
                  label="Gender"
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  fullWidth
                  required
                >
                  <MenuItem value="">Select</MenuItem>
                  <MenuItem value="Male">Male</MenuItem>
                  <MenuItem value="Female">Female</MenuItem>
                  <MenuItem value="Other">Other</MenuItem>
                </TextField>

                <Button variant="outlined" component="label">
                  Upload Face Image
                  <input hidden type="file" accept="image/*" onChange={handleImageUpload} />
                </Button>

                {/* consent */}
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={consent}
                      onChange={(e) => setConsent(e.target.checked)}
                    />
                  }
                  label="I confirm this identity belongs to me."
                />

              </Box>
            </Grid>

            {/* RIGHT — PREVIEW + INSTRUCTIONS */}
            <Grid item xs={12} md={6}>

              {/* image preview */}
              <Box
                sx={{
                  height: 250,
                  border: "2px dashed #ccc",
                  borderRadius: 3,
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  backgroundColor: "#fafafa",
                  mb: 2,
                }}
              >
                {preview ? (
                  <img
                    src={preview}
                    alt="Preview"
                    style={{ maxWidth: "100%", maxHeight: "100%", borderRadius: 8 }}
                  />
                ) : (
                  <Typography color="text.secondary">
                    Uploaded face preview
                  </Typography>
                )}
              </Box>

              <Divider sx={{ mb: 2 }} />

              {/* capture instructions */}
              <Typography variant="h6" gutterBottom>
                Verification Instructions
              </Typography>

              <Typography variant="body2" color="text.secondary">
                • Ensure good lighting  
                • Remove glasses/hats  
                • Face centered in camera  
                • Follow blink/head prompts  
                • Stay still during verification
              </Typography>

            </Grid>
          </Grid>

          {/* identity summary */}
          <Divider sx={{ my: 3 }} />

          <Typography variant="h6">Identity Summary</Typography>
          <Typography variant="body2" color="text.secondary">
            Name: {formData.name || "-"}  
            <br />
            Age: {formData.age || "-"}  
            <br />
            Gender: {formData.gender || "-"}
          </Typography>

          {/* proceed button */}
          <Box sx={{ mt: 3, textAlign: "center" }}>
            <Button
              variant="contained"
              size="large"
              disabled={!isFormValid}
              onClick={handleProceed}
              sx={{ borderRadius: 2, fontWeight: "bold" }}
            >
              Proceed to Face Verification
            </Button>
          </Box>

        </CardContent>
      </Card>
    </Box>
  );
};

export default KYC;

