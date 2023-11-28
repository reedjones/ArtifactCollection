export default class RegionService {
    getRegions() {
        return fetch('/api/regions/')
            .then((res) => res.json())
            .then((data) => data);
    }
    // Add more methods for other region-related services
}