import api from "./api";

export const upload = async (formData) => {
  return api.post("/kyc/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};
