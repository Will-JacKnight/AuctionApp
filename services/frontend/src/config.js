// Runtime configuration
let API_URL = window.API_URL || import.meta.env.VITE_API_GATEWAY_DOCKER_URL;

export const setApiUrl = (url) => {
  API_URL = url;
};

export const getApiUrl = () => API_URL; 