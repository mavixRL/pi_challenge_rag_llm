# from fastapi import FastAPI
# from app.api.endpoints import app

# app = app
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='0.0.0.0', port=8000)



import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app.api.endpoints import app as fastapi_app
from app.utils.utils import doc_to_paragraphs, split_text
from db.database import init_chromadb, add_documents_to_collection
import string 


ntoken_list, list_parrafo = doc_to_paragraphs('./docs/documento.docx')
docs = split_text(input=list_parrafo, chunk_size=500, chunk_overlap=20,unir_list=False,separators=None,verbose=False)#separators=["\n\n", "\n"]
collection = init_chromadb()


metadata_options = {
    "hnsw:space": "cosine"  # You can change this to "ip" or "cosine" if needed
}
collection = add_documents_to_collection(collection,docs=docs,model='embed-multilingual-v3.0',metadata_options=metadata_options)


app = fastapi_app

if __name__ == '__main__':
    import uvicorn
    # uvicorn.run(app, host='0.0.0.0', port=8003,reload =True)
    uvicorn.run(app, host='0.0.0.0', port=8003)
