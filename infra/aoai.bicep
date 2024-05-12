param name string
param location string 
param deployment object

resource account 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: name
  location: location
  tags: {}
  kind: 'OpenAI'
  properties: {
    customSubDomainName: name
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
    }
  }
  sku: {
    name: 'S0'
  }
}

resource deploy 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  parent: account
  name: deployment.name
  properties: {
    model: deployment.model
    raiPolicyName: contains(deployment, 'raiPolicyName') ? deployment.raiPolicyName : null
  }
  sku: contains(deployment, 'sku') ? deployment.sku : {
    name: 'Standard'
    capacity: 30
  }
}

output endpoint string = account.properties.endpoint
output id string = account.id
output name string = account.name
output token string = account.listkeys().key1
