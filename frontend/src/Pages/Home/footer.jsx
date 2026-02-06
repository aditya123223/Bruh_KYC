import { Typography, Stack, Link, Divider } from "@mui/material";

function Footer() {
  return (
    <footer className="bg-light mt-5">
      <div className="container py-5">
        <div className="row gy-4">
          {/* Brand / About */}
          <div className="col-12 col-md-4">
            <Typography variant="h6" fontWeight={700} gutterBottom>
              KYC Platform
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Secure and fast identity verification platform. Complete your KYC
              in minutes with full data protection.
            </Typography>
          </div>

          {/* Links */}
          <div className="col-6 col-md-2">
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>
              Company
            </Typography>
            <Stack spacing={1}>
              <Link href="#" underline="hover">
                About
              </Link>
              <Link href="#" underline="hover">
                Careers
              </Link>
              <Link href="#" underline="hover">
                Contact
              </Link>
            </Stack>
          </div>

          <div className="col-6 col-md-2">
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>
              Resources
            </Typography>
            <Stack spacing={1}>
              <Link href="#" underline="hover">
                Help Center
              </Link>
              <Link href="#" underline="hover">
                Privacy Policy
              </Link>
              <Link href="#" underline="hover">
                Terms
              </Link>
            </Stack>
          </div>

          {/* Social */}
          <div className="col-12 col-md-4">
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>
              Stay Connected
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Follow us for updates and announcements.
            </Typography>
            <Stack direction="row" spacing={2} mt={2}>
              <Link href="#" underline="hover">
                Twitter
              </Link>
              <Link href="#" underline="hover">
                LinkedIn
              </Link>
              <Link href="#" underline="hover">
                GitHub
              </Link>
            </Stack>
          </div>
        </div>

        <Divider sx={{ my: 4 }} />

        {/* Bottom */}
        <div className="text-center">
          <Typography variant="body2" color="text.secondary">
            © {new Date().getFullYear()} KYC Platform. All rights reserved.
          </Typography>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
