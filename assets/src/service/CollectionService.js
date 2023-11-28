export default class CollectionService {
    getCollections() {
        return fetch('/api/categories/')
            .then((res) => res.json())
            .then((data) => data);
    }

    getDetail(pk) {
        return fetch(`/api/categories/${pk}/`)
            .then((res) => res.json())
            .then((data) => data);
    }
    // Add more methods for other type category-related services
}