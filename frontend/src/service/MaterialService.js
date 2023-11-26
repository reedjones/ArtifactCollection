export default class MaterialService {
    getMaterials() {
        return fetch('/api/materials/')
            .then((res) => res.json())
            .then((data) => data);
    }
    // Add more methods for other material-related services
}
