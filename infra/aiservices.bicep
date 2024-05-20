param name string
param location string

resource aiService 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: name
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'CognitiveServices'
  properties: {
    apiProperties: {
      statisticsEnabled: false
    }
  }
}

output key string = aiService.listKeys().key1
