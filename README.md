<h1>Informatica EDC Scanner for API Sources</h1>
<b>Note: This was tested on Informatica EDC 10.2.2, however, since this is an independent python code, it should work in a similar fashion for all versions</b>
<b>This is not an official scanner from Informatica and is a professional services effort to create a custom scanner for API based sources</b>

<h2>Use Case</h2>
In several organizations, there is a move towards using ReST API based data access, where the original database or other data providing service is made transparent via an API framework.
At present, Informatica EDC does not directly support extracting metadata out of these sources. This code helps in extracting metadata and formatting them to EDC's requirements(objects and links.csv file)
<h2>The Scripts</h2>
There are two scripts present in this repostory, which are of interest here. The API_Metadata_Extractor.py and API_MetadataExtractor_Yaml.py. THe API metadata extractor simply uses a 
ReST API url to extract metadata from it. The API MetadataExtractor Yaml is a simple script to extract metadata from yaml file for specific API, and can extract from OpenAPI 3.0 or above compliant yaml files

<h2>Usage</h2>
<h4>API_Metadata_Extractor.py</h4>
This script connects to the API methods directly to fetch metadata out of it. As of now, no iteration has been built in if you need to extract metadata out of multiple methods, however this can be built fairly easily
The script has also not been completely parameterized, the api URL, API key or other methods of authentication has to be changed in the code, you can parameterize them if required. 
Please change these values in the payload header part of the code, which is the first few lines. The model name should also be customized based on the customer needs. 
<h4>API_MetadataExtractor_Yaml.py</h4>
This script picks up metadata from OpenAPI 3.0 compliant yaml files. If you try this on a different version of yaml, it might error out. This script is parameterized and the parameters are
added to the config.yaml file. 
<b>The three mandatory parameters required are:</b>
<li>yamlfile_input: This is the location of the yaml file which needs to be parsed </li>
<li>jsonfile_output: This is a temporary json file used for processing, please use a temp location</li>
<li>zipfile_output: This is the final output zip file containing objects.csv and links.csv file for EDC</li>
<b> The optional parameter is </b>
<li>URL: This is the url of the API Service, which helps identify the service in EDC</li>

<h4>FDP_API.xml</h4>
This is the model required for the creation of custom resource in EDC

<h3><b> Important Notes</b></h3>
1. Please make sure to change the model package name if required. It is recommended to change to something that reflects the customer conventions. For example, if Informatica internally uses this, we would have com.informatica.rest.api or something similar
2. Please make sure to change the code according to the changes made to the package name in the model, else the upload to EDC will fail
3. Based on our customer requirements, we had a few fields were added(URL), please review and remove them if needed
4. If you are planning to use this with a lower version of API spec, you will have to change the code accordingly.
5. In both the scripts certificate verification is disabled, since ours was an internal API gateway. In case a certificate verification is required, you will have to change the code accordingly.

