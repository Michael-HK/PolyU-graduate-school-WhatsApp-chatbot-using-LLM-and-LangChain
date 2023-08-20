# PolyU-graduate-school-WhatsApp-chatbot-using-LLM,-LangChain,and-Twilio
In this project, I developed a chatbot for Hong Kong Polytechnic University graduate school information and inquiries. LangChain and Hugginface are used as the framework. LLma2 is the chosen LLM model along with llmIndex for context embedding. Flask to expose the endpoint of the model, and Twilo for the WhatsApp platform implementation. The whole model is packaged in a Dockerfile for endpoint deployment using cloud services.
* LangChain is used as the framework for coupling LLM model with external data source
* llma-2 with 70B parameters was selected as the llm model from HuggingFace hub, this is achieved using the HuggingFace wrapper in LangChain
* The data context embedding (vector db) was achieved using llm-index with langChain and HuggingFace embedding rapper, followed by indexing the document.
* Twilio API was adopted to facilitate interaction between the client on the WhatsApp platform with the LLM model and receive responses.
* The model was packaged in Dockerfile for possible deployment using Heroku or available cloud services/servers.
* **Notice:** the URL generated after deploying the model will be embedded in the Twilio account, and Twilio will generate a WhatsApp number that users can chat with to make inquiries on their devices. It is also worth mentioning that load balancing and network traffic management will be handled on the cloud services side
