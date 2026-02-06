import Button from "@mui/material/Button";
import { Typography, Stack } from "@mui/material";
import { useNavigate } from "react-router-dom";

function LeftSection() {
  const navigate = useNavigate();

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
          onClick={() => navigate("/KycDetails")}
        >
          Do KYC
        </Button>
      </div>
    </Stack>
  );
}

export default LeftSection;
