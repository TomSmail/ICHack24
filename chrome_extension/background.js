chrome.runtime.onMessage.addListener(function (message, sender, senderResponse) {
    {
      fetch('<https://api.openai.com/v1/chat/completions>', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer <<<<$OPENAI_API_KEY>>>>'
        },
        body: {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': 'only respond yes or no to my next question'}, 
            {'role': 'user', 'content': 'is this url related to ' + message.typeOfWork + ': ' + message.url  }],
            'temperature': 0.7
          }

      }).then(res => {
        return res.json();
      }).then(res => {
        senderResponse(res);
      })
    }
    return true
  });