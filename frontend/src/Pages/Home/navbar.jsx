import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";

function Navbar() {
  return (
    <AppBar
      position="static"
      color="primary"
      sx={{ backgroundColor: "#22a4fb" }}
    >
      <Toolbar>
        {/* Left side: Logo or Menu */}

        {/* Title */}
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          KYC Verification
        </Typography>

        {/* Right side: Navigation buttons */}
        <Button color="inherit">Home</Button>
        <Button color="inherit">About</Button>
        <Button color="inherit">Contact</Button>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
