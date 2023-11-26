export default class CategoryService {
    getTypeCategories() {
        return fetch('/api/categories/')
            .then((res) => res.json())
            .then((data) => data);
    }
    // Add more methods for other type category-related services
}