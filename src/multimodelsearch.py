import os
from haystack import Document
from haystack import Pipeline
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes.retriever.multimodal import MultiModalRetriever
from config import MODEL_DIM, MODEL_NAME

class MultiModelSearch:
    def __init__(self):
        self.document_stores = InMemoryDocumentStore(embedding_dim=MODEL_DIM)
        document_directory = os.path.join(os.getcwd(),"data")
        # fetch all images and write into haystack document
        images = [
            Document(content= f"{document_directory}/{filename}",content_type="image" )
            for filename in os.listdir(document_directory)
        ]

        self.document_stores.write_documents(images)
        self.retriever_text_to_image = MultiModalRetriever(
            document_store= self.document_stores,
            query_embedding_model= MODEL_NAME,
            query_type="text",
            document_embedding_models= {"image":MODEL_NAME},
)
        
        self.document_stores.update_embeddings(retriever=self.retriever_text_to_image)

        self.pipeline = Pipeline()
        self.pipeline.add_node(component=self.retriever_text_to_image, name="retriever_text_to_image", inputs=["Query"])

    def search(self,query, top_k = 3):
        results = self.pipeline.run(query=query, params={"retriever_text_to_image": {"top_k":top_k}})
        return sorted(results["documents"],key= lambda d:d.score, reverse=True)
