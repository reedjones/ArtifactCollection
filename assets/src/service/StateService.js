export default class StateService {
    getStates() {
        return fetch('http://127.0.0.1:8000/artifacts-api/states/?format=json', {method:'GET'})
            .then((res) => res.json())
            .then((d) => d);
    }
}
