__author__ = "reed@reedjones.me"


class JavaScriptGenerator:
    def __init__(self, data_service_implementation):
        self.data_service_implementation = data_service_implementation

    def generate_service_file(self, model_name):
        service_content = f"""
export default class {model_name}Service {{
    get{model_name}s() {{
        return fetch('{self.data_service_implementation.get_model_api_url(model_name)}')
            .then((res) => res.json())
            .then((data) => data);
    }}
    // Add more methods for other {model_name}-related services
}}
"""
        return service_content

    def save_service_file(self, model_name, file_path):
        with open(file_path, 'w') as file:
            file.write(self.generate_service_file(model_name))
        print(f'Successfully generated {model_name}Service.js at {file_path}')
#
# # Example usage
# data_service_implementation = DataServiceImplmentation()  # You should replace this with your actual implementation
# javascript_generator = JavaScriptGenerator(data_service_implementation)
#
# # Generate and save service files for different models
# javascript_generator.save_service_file('Artifact', 'ArtifactService.js')
# javascript_generator.save_service_file('Region', 'RegionService.js')
# # ... add more models as needed
