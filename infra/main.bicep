targetScope = 'subscription'

param environmentName string
param location string = 'japaneast'
param resourceGroupName string = environmentName

var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))

param openAiResourceGroupLocation string = 'eastus'
param openAiGptModelName string = 'gpt-4o'
param openAiGptModelApiVersion string = '2023-05-15'
param openAiGptDeploymentName string = 'gpt-4o-deploy'

param aiSearchIndexName string = 'gptkbindex'
param storageContainerName string = 'content'
param fileSharedName string = 'shared'

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

module aiService 'aiservices.bicep' = {
  name: 'aiservice'
  scope: resourceGroup
  params: {
    name: 'aiservice-${resourceToken}'
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
      name: openAiGptDeploymentName
      model: {
        format: 'OpenAI'
        name: openAiGptModelName
        version: openAiGptModelApiVersion
      }
    }
  }
}

module storage 'storage.bicep' = {
  name: 'storage'
  scope: resourceGroup
  params: {
    name: 'storage${resourceToken}'
    location: location
    containers: [
      {
        name: storageContainerName
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
    azureOpenAiGptDeployment: openAiGptDeploymentName
    azureOpenAiToken: aoai.outputs.token
    azureOpenAiApiVersion: openAiGptModelApiVersion
    storageName: storage.outputs.name
    storageKey: storage.outputs.key
    fileSharedName: fileSharedName
  }
}

output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_RESOURCE_GROUP string = resourceGroup.name

output AZURE_AI_SERVICES_KEY string = aiService.outputs.key

output AZURE_SEARCH_INDEX string = aiSearchIndexName
output AZURE_SEARCH_SERVICE string = aiSearch.outputs.name
output AZURE_SEARCH_SERVICE_KEY string = aiSearch.outputs.key

output AZURE_OPENAI_SERVICE string = aoai.outputs.name
output AZURE_OPENAI_GPT_DEPLOYMENT string = openAiGptDeploymentName
output AZURE_OPENAI_API_VERSION string = openAiGptModelApiVersion
output AZURE_OPENAI_TOKEN string = aoai.outputs.token

output AZURE_STORAGE_ACCOUNT string = storage.outputs.name
output AZURE_STORAGE_CONTAINER string = storageContainerName
output AZURE_STORAGE_KEY string = storage.outputs.key

output AZURE_FUNCTIONS string = functions.outputs.name
