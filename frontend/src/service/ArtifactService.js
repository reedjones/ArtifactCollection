export default class ArtifactService {
    getArtifactMaster(params) {
        const url = "http://127.0.0.1:8000/api/artifact-master/"
        const queryString = new URLSearchParams(params).toString();
        return fetch(`${url}?${queryString}`, {method:'GET'})
            .then((res) => res.json())
            .then((data) => data);
    }

    getDataListSimple(params){
        const url = "http://127.0.0.1:8000/artifacts-api/artifacts-simple/";
        const queryString = new URLSearchParams(params).toString();
        return fetch(`${url}?${queryString}`, {method:'GET'})
            .then((res) => res.json())
            .then((data) => data);

    }

    postArtifactMaster(params, data) {
        const queryString = new URLSearchParams(params).toString();
        const payload = JSON.stringify(data);
        return fetch(`/api/artifact-master/?${queryString}`, {
            method:'POST',
            body: payload
        }
        )
            .then((res) => res.json())
            .then((data) => data);
    }

    getArtifactCountByTypeCategory() {
        return fetch('/api/artifact-count-by-type-category/')
            .then((res) => res.json())
            .then((data) => data);
    }
    // Add more methods for other artifact-related services


    getArtifactsSimple(){
        return fetch('/api/arti')
    }

    fixImages(items){
        items.forEach((item) => {

        })
    }


}