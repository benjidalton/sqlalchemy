const apiBase = import.meta.env.VITE_API_URL;

export const AssetsAPI = {
    getImageUrl(path) {
        const cleanPath = path.replace(/^"+|"+$/g, "");
        return `${apiBase}/${cleanPath}`;
    }
}