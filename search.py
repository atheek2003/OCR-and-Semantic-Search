
from sentence_transformers import SentenceTransformer, util
import torch

class SemanticSearch:
    def __init__(self):
        self.sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    def semantic_search(self, query, text, top_k=5, min_score=0.2):
        """Perform semantic search with a minimum score threshold."""
        try:
            sentences = text.split('.')
            sentence_embeddings = self.sentence_model.encode(sentences)
            query_embedding = self.sentence_model.encode(query)

            # Calculate cosine similarity scores
            cos_scores = util.cos_sim(query_embedding, sentence_embeddings)[0]
            top_results = torch.topk(cos_scores, k=min(top_k, len(sentences)))

            # Filter and return only results above the minimum score
            results = []
            for score, idx in zip(top_results[0], top_results[1]):
                if score.item() >= min_score:
                    results.append((sentences[idx].strip(), score.item()))
            
            return results
        except Exception as e:
            return {"error": str(e)}
