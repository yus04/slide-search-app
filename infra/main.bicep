targetScope = 'subscription'

param environmentName string
param location string = 'japaneast'
param resourceGroupName string = environmentName

var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))

param openAiResourceGroupLocation string = 'eastus2'
param openAiGpt4VTurboDeploymentName string = 'gpt-4-turbo-vision-deploy'

param aiSearchIndexName string = 'gptkbindex'
param storageContainerName string = 'content'

resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupName
  location: location
}

module aiSearch 'aisearch.bicep' = {
  name: 'aisearch'
  scope: resourceGroup
  params: {
    name: 'aisearch-${resourceToken}'
    location: location
  }
}

module aoai 'aoai.bicep' = {
  name: 'aoai'
  scope: resourceGroup
  params: {
    name: 'aoai-${resourceToken}'
    location: openAiResourceGroupLocation
    deployment: {
      name: openAiGpt4VTurboDeploymentName
      model: {
        format: 'OpenAI'
        name: 'gpt-4'
        version: 'turbo-2024-04-09'
      }
    }
  }
}

module storage 'blobstorage.bicep' = {
  name: 'storage'
  scope: resourceGroup
  params: {
    name: 'blobstorage${resourceToken}'
    location: location
    containers: [
      {
        name: 'content'
        publicAccess: 'None'
      }
    ]
  }
}

module functions 'functions.bicep' = {
  name: 'functions'
  scope: resourceGroup
  params: {
    name: 'functions-${resourceToken}'
    location: location
    tags: { 'azd-service-name': 'functions' }
    azureOpenAiService: aoai.outputs.name
    gptDeployment: openAiGpt4VTurboDeploymentName
    azureOpenAiToken: aoai.outputs.token
  }
}

output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_RESOURCE_GROUP string = resourceGroup.name

output AZURE_SEARCH_INDEX string = aiSearchIndexName
output AZURE_SEARCH_SERVICE string = aiSearch.outputs.name
output AZURE_SEARCH_SERVICE_KEY string = aiSearch.outputs.key

output AZURE_OPENAI_SERVICE string = aoai.outputs.name
output AZURE_OPENAI_GPT_4V_DEPLOYMENT string = openAiGpt4VTurboDeploymentName

output AZURE_STORAGE_ACCOUNT string = storage.outputs.name
output AZURE_STORAGE_CONTAINER string = storageContainerName
output AZURE_STORAGE_KEY string = storage.outputs.key

output AZURE_FUNCTIONS string = functions.outputs.name
// output AZURE_FUNCTIONS_KEY string = functions.outputs.key
