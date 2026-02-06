import Button from "@mui/material/Button";
import { Typography, Stack } from "@mui/material";
import { useNavigate } from "react-router-dom";
import api from "../../Services/api"; // your axios instance

function LeftSection() {
  const navigate = useNavigate();

  const handleStartKYC = async () => {
    try {
      // Call backend /kyc/session to get a session token
      const response = await api.get("/kyc/session", {
        headers: {
          "x-api-key": "hackathon-demo-key", // if required
        },
      });

      const sessionToken = response.data.session_token;

      // Store session token in localStorage
      localStorage.setItem("kycSessionToken", sessionToken);

      // Navigate to KYC page
      navigate("/KycDetails");
    } catch (err) {
      console.error("Failed to get session token", err);
      alert("Unable to start KYC. Try again later.");
    }
  };

  return (
    <Stack spacing={3}>
      <Typography variant="h3" fontWeight={700}>
        Complete Your KYC
        <br />
        in Minutes
      </Typography>

      <Typography variant="body1" color="text.secondary">
        Verify your identity securely and unlock full access to all platform
        features. Fast, simple, and 100% safe.
      </Typography>

      <div>
        <Button
          variant="contained"
          size="large"
          sx={{
            borderRadius: "10px",
            px: 5,
            py: 1.5,
            textTransform: "none",
            fontSize: "1rem",
          }}
          onClick={handleStartKYC}
        >
          Do KYC
        </Button>
      </div>
    </Stack>
  );
}

export default LeftSection;
