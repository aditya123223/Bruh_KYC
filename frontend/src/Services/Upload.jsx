import api from "./api";

export const upload = async (formData) => {
  try {
    // Get session token from FormData
    const sessionToken = formData.get("session_token"); // FormData method

    const response = await api.post("/kyc/verify-video", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        "x-api-key": sessionToken, // send to backend
      },
    });

    return response;
  } catch (err) {
    console.error("Upload error:", err);
    throw err;
  }
};
