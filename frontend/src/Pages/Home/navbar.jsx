import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import Box from "@mui/material/Box";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <AppBar
      position="sticky"
      elevation={3}
      sx={{
        backgroundColor: "#0070ba",
      }}
    >
      <Toolbar className="container">
        {/* Mobile menu icon */}
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          sx={{ mr: 2, display: { md: "none" } }}
        >
          <MenuIcon />
        </IconButton>

        {/* Logo / Brand */}
        <Typography
          variant="h6"
          sx={{
            flexGrow: 1,
            fontWeight: 700,
            letterSpacing: 0.5,
          }}
        >
          <Link to="/" style={{ color: "white", textDecoration: "none" }}>
            KYC Verification
          </Link>
        </Typography>

        {/* Desktop Nav */}
        <Box sx={{ display: { xs: "none", md: "flex" }, gap: 2 }}>
          <Button color="inherit" sx={{ textTransform: "none" }}>
            Home
          </Button>
          <Button color="inherit" sx={{ textTransform: "none" }}>
            About
          </Button>
          <Button color="inherit" sx={{ textTransform: "none" }}>
            Contact
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
