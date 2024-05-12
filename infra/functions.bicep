param name string
param location string
param tags object
param azureOpenAiService string
param gptDeployment string
param azureOpenAiToken string

resource hostingPlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: name
  location: location
  sku: {
    name: 'B1'
  }
  properties: {
    reserved: true
  }
}

resource functionApp 'Microsoft.Web/sites@2022-09-01' = {
  name: name
  location: location
  tags: tags
  kind: 'functionapp'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: hostingPlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'AZURE_OPENAI_SERVICE'
          value: azureOpenAiService
        }
        {
          name: 'AZURE_OPENAI_API_VERSION'
          value: '2023-05-15'
        }
        {
          name: 'GPT_DEPLOYMENT'
          value: gptDeployment
        }
        {
          name: 'AZURE_OPENAI_TOKEN'
          value: azureOpenAiToken
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
      ]
      linuxFxVersion: 'Python|3.10'
      minTlsVersion: '1.2'
    }
    httpsOnly: true
  }
}

output id string = functionApp.id
output name string = functionApp.name