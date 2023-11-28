export default class PersonService {
    getPersons() {
        return fetch('/api/persons/')
            .then((res) => res.json())
            .then((data) => data);
    }
    // Add more methods for other person-related services
}
