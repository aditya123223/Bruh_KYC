import { Routes, Route } from "react-router-dom";
import Home from "./Pages/Home/home.jsx";
import KYC from "./Pages/KYC/KYC.jsx";
import Navbar from "./Pages/Home/navbar.jsx";
import Footer from "./Pages/Home/footer.jsx";

function App() {
  return (
    <>
      {/* Navbar always visible */}
      <Navbar />

      {/* Page content changes based on route */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/KycDetails" element={<KYC />} />
      </Routes>

      {/* Footer always visible */}
      <Footer />
    </>
  );
}

export default App;
