// Runtime configuration
let API_URL;

// Determine the API URL based on the runtime environment
if (window.API_URL) {
  API_URL = window.API_URL;
} else {
  API_URL = import.meta.env.VITE_API_GATEWAY_LOCAL_URL;
}

export const setApiUrl = (url) => {
  API_URL = url;
};

export const getApiUrl = () => API_URL; 