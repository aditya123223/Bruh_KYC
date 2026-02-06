import { Box, TextField, MenuItem, Button, Typography } from "@mui/material";
import AddPhotoAlternateIcon from "@mui/icons-material/AddPhotoAlternate";

const GeneralInfo = ({ formData, onChange, imagePreview, onImageUpload }) => {
  return (
    <Box
      sx={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: { xs: "column", md: "row" },
        gap: 3,
        p: 3,
      }}
    >
      {/* Left: Image Upload */}
      <Box
        sx={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          border: "2px dashed #90a4ae",
          borderRadius: 3,
          backgroundColor: "#f1f5f9",
          height: { xs: 250, md: "60%" },
          position: "relative",
          overflow: "hidden",
        }}
      >
        {imagePreview ? (
          <img
            src={imagePreview}
            alt="Face Preview"
            style={{
              width: "100%",
              height: "60%",
              objectFit: "cover",
            }}
          />
        ) : (
          <Box
            sx={{
              textAlign: "center",
              color: "#607d8b",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              height: "60%",
            }}
          >
            <AddPhotoAlternateIcon sx={{ fontSize: 50, mb: 1 }} />
            <Typography>Drag & Drop or Click to Upload</Typography>
          </Box>
        )}
        <input
          type="file"
          accept="image/*"
          onChange={onImageUpload}
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            opacity: 0,
            cursor: "pointer",
          }}
        />
      </Box>

      {/* Right: Form Inputs */}
      <Box sx={{ flex: 2, display: "flex", flexDirection: "column", gap: 3 }}>
        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          General Information
        </Typography>

        <TextField
          label="Full Name"
          name="name"
          value={formData.name}
          onChange={onChange}
          fullWidth
          variant="outlined"
          size="medium"
        />
        <TextField
          label="Age"
          name="age"
          type="number"
          value={formData.age}
          onChange={onChange}
          fullWidth
          variant="outlined"
          size="medium"
        />
        <TextField
          select
          label="Gender"
          name="gender"
          value={formData.gender}
          onChange={onChange}
          fullWidth
          variant="outlined"
          size="medium"
        >
          <MenuItem value="">Select</MenuItem>
          <MenuItem value="Male">Male</MenuItem>
          <MenuItem value="Female">Female</MenuItem>
          <MenuItem value="Other">Other</MenuItem>
        </TextField>

        <Button
          variant="contained"
          sx={{
            mt: 1,
            backgroundColor: "#0070ba",
            "&:hover": { backgroundColor: "#005ea3" },
            color: "#fff",
            textTransform: "none",
            py: 1.5,
            borderRadius: 2,
          }}
        >
          Save Information
        </Button>
      </Box>
    </Box>
  );
};

export default GeneralInfo;
