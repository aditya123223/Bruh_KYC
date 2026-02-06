import { Routes, Route } from "react-router-dom";

import KYC from "./Pages/KYC/KYC.jsx";

function App() {
  return (
    <Routes>
      <Route path="/" element={<KYC />} />
      <Route path="/verify-camera" element={<div>Camera Page Coming Soon</div>} />
    </Routes>
  );
}

export default App;
