#!/usr/bin/env python3
"""
Interactive RAG chat over FAISS index:
- retrieves relevant refactored code + error logs (+ tests if indexed)
- answers grounded questions about failures and next steps

Usage:
  python tools/rag_chat.py

Environment:
  OLLAMA_MODEL=devstral-small-2:24b-cloud
  OLLAMA_TEMPERATURE=0.0
  OLLAMA_EMBED_MODEL=nomic-embed-text
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


@dataclass(frozen=True)
class Paths:
    index_dir: Path


def format_docs(docs: List[Document]) -> str:
    parts: List[str] = []
    for i, d in enumerate(docs, start=1):
        src = d.metadata.get("source", "unknown")
        typ = d.metadata.get("type", "unknown")
        text = d.page_content.strip()
        if len(text) > 1400:
            text = text[:1400] + "\n...[truncated]..."
        parts.append(f"[{i}] type={typ} source={src}\n{text}")
    return "\n\n".join(parts)


def main() -> None:
    dataset_root = Path("dataset").resolve()
    paths = Paths(index_dir=dataset_root / "rag" / "rag_faiss_index")

    if not paths.index_dir.exists():
        raise SystemExit("Missing dataset/rag/rag_faiss_index. Run tools/build_faiss_rag.py first.")
    #for figuring out which files are most applicable
    embed_model = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    embeddings = OllamaEmbeddings(model=embed_model)
    vectordb = FAISS.load_local(str(paths.index_dir), embeddings, allow_dangerous_deserialization=True)

    #the one thats doing the explaining, will need to be replaced
    llm_model = os.environ.get("OLLAMA_MODEL", "devstral-small-2:24b-cloud")
    llm_temp = float(os.environ.get("OLLAMA_TEMPERATURE", "0.0"))
    llm = ChatOllama(model=llm_model, temperature=llm_temp)

    #the part that decides which documents are most relevant
    docs = vectordb.similarity_search(prompt, k=8)
    context = format_docs(docs)
    #should probably just return it here and then put the context into the big prompt
    new_prompt = f"""

        Retrieved context:
        {context}

        Task:
        {prompt}
        """
    #can probably just return the new prompt here to be used on the real thing
    resp = llm.invoke(new_prompt)
    answer = resp.content if isinstance(resp.content, str) else str(resp.content)
    print(answer)
        
def get_context(prompt: str) -> str:
    dataset_root = Path("rag").resolve()
    paths = Paths(index_dir=dataset_root / "rag_faiss_index")

    if not paths.index_dir.exists():
        raise SystemExit("Missing rag/rag_faiss_index. Run build_rag_index.py first.")
    
    embed_model = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    embeddings = OllamaEmbeddings(model=embed_model)
    vectordb = FAISS.load_local(str(paths.index_dir), embeddings, allow_dangerous_deserialization=True)

    #the part that decides which documents are most relevant
    docs = vectordb.similarity_search(prompt, k=8)
    context = format_docs(docs)
    
    return context
    


if __name__ == "__main__":
    main()