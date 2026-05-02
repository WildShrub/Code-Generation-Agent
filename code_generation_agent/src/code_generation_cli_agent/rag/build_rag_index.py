#!/usr/bin/env python3
"""
Build a FAISS RAG index over:
- dataset/outputs/tasks/task_*.py          (refactored code)
- dataset/outputs/error_logs/*.txt         (pytest logs)
- dataset/input/tests/test_task_*.py       (tests, optional but recommended)

Writes:
- dataset/outputs/rag_faiss_index/         (FAISS index + metadata)

Requirements:
  pip install langchain langchain-community langchain-ollama faiss-cpu
  ollama pull nomic-embed-text
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass(frozen=True)
class Paths:
    rag_root: Path
    rag_docs_dir: Path
    index_dir: Path


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def load_docs(paths: Paths) -> List[Document]:
    docs: List[Document] = []
    print("\n")
    print(os.listdir())
    print("\n")
    if paths.rag_docs_dir.exists():
        for p in sorted(paths.rag_docs_dir.glob("*.md")):
            docs.append(Document(page_content=read_text(p), metadata={"source": str(p), "type": "information"}))
    else:
        print(str(paths.rag_docs_dir) + " does not exist")

    return docs


def main() -> None:
    rag_root = Path("rag").resolve()
    paths = Paths(
        rag_root=rag_root,
        rag_docs_dir=rag_root / "rag_docs",    
        index_dir=rag_root / "rag_faiss_index",     #where it saves it to
    )
    
    print(str(paths))
    docs = load_docs(paths)
    print(str(docs))
    if not docs:        
        raise SystemExit("No documents found to index. Check rag/rag_docs.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    embed_model = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    embeddings = OllamaEmbeddings(model=embed_model)

    vectordb = FAISS.from_documents(chunks, embeddings)

    paths.index_dir.mkdir(parents=True, exist_ok=True)
    vectordb.save_local(str(paths.index_dir))


if __name__ == "__main__":
    main()

