import { Box, Paper } from "@mui/material";

function RightSection() {
  return (
    <Paper
      elevation={6}
      sx={{
        p: 2,
        borderRadius: 4,
        overflow: "hidden",
      }}
    >
      <Box
        component="img"
        src="heroimg.jpg"
        alt="KYC Illustration"
        sx={{
          width: "100%",
          height: { xs: 250, md: 380 },
          objectFit: "cover",
          borderRadius: 3,
        }}
      />
    </Paper>
  );
}

export default RightSection;
