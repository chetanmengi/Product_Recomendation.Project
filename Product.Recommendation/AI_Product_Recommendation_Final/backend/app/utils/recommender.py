# Cleaned Recommender Utility
# - Reviewed and rewritten to remove verbatim/uncited text.
# - Uses sentence-transformers to compute embeddings and sklearn NearestNeighbors (cosine).
# - Returns structured recommendation results.



import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
import joblib

class Recommender:
    def __init__(self, data_path='data/cleaned_dataset.csv'):
        # locate project root
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        self.data_path = os.path.join(root, data_path)
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        # prepare text blob for embeddings
        self.df.fillna('', inplace=True)
        self.df['text_blob'] = self.df.apply(lambda r: ' '.join([str(r.get(c,'')) for c in ['title','brand','description','categories'] if c in r.index]), axis=1)
        # embeddings cache
        models_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
        os.makedirs(models_dir, exist_ok=True)
        self.emb_path = os.path.join(models_dir, 'embeddings.joblib')
        if os.path.exists(self.emb_path):
            try:
                saved = joblib.load(self.emb_path)
                self.embeddings = saved['emb']
                self.ids = saved.get('ids', list(range(len(self.df))))
            except Exception:
                self._compute_and_save_embeddings()
        else:
            self._compute_and_save_embeddings()

        # ensure a text_blob column
        if 'text_blob' not in self.df.columns:
            cols = []
            for c in ['title','brand','description','categories','category']:
                if c in self.df.columns:
                    cols.append(self.df[c].fillna('').astype(str))
            if cols:
                self.df['text_blob'] = (' ').join(cols)
            else:
                self.df['text_blob'] = self.df.iloc[:,0].astype(str)
        # load model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        models_dir = os.path.join(root, 'models')
        os.makedirs(models_dir, exist_ok=True)
        emb_path = os.path.join(models_dir, 'text_emb.npy')
        nn_path = os.path.join(models_dir, 'nn.joblib')
        if os.path.exists(emb_path) and os.path.exists(nn_path):
            self.embeddings = np.load(emb_path)
            self.nn = joblib.load(nn_path)
        else:
            texts = self.df['text_blob'].fillna('').tolist()
            self.embeddings = self.model.encode(texts, show_progress_bar=True)
            np.save(emb_path, self.embeddings)
            self.nn = NearestNeighbors(n_neighbors=min(20, len(self.embeddings)), metric='cosine')
            self.nn.fit(self.embeddings)
            joblib.dump(self.nn, nn_path)

    def recommend(self, query_text, k=5):
        qemb = self.model.encode([query_text])[0]
        n = min(len(self.embeddings), max(k,5))
        dists, idxs = self.nn.kneighbors([qemb], n_neighbors=n)
        res = []
        for dist, idx in zip(dists[0][:k], idxs[0][:k]):
            row = self.df.iloc[idx].to_dict()
            # try to extract an image field if present
            img = None
            for key in ['image','images','img','image_url','image_link']:
                if key in row and pd.notna(row.get(key)):
                    img = row.get(key)
                    break
            res.append({
                'uniq_id': row.get('uniq_id', str(idx)),
                'title': row.get('title', ''),
                'brand': row.get('brand',''),
                'price': row.get('price',''),
                'category': row.get('categories', row.get('category','')),
                'image': img,
                'score': float(1 - dist)
            })
        return res

    def analytics_summary(self):
        num_items = int(len(self.df))
        num_categories = int(self.df['categories'].nunique()) if 'categories' in self.df.columns else (int(self.df['category'].nunique()) if 'category' in self.df.columns else 0)
        avg_price = float(pd.to_numeric(self.df['price'], errors='coerce').dropna().astype(float).mean()) if 'price' in self.df.columns else 0.0
        return {'num_items': num_items, 'num_categories': num_categories, 'avg_price': avg_price}



def _compute_and_save_embeddings(self):
    # compute embeddings using sentence-transformers
    model = SentenceTransformer('all-MiniLM-L6-v2')
    texts = self.df['text_blob'].tolist()
    emb = model.encode(texts, show_progress_bar=False)
    self.embeddings = emb
    self.ids = list(range(len(self.df)))
    joblib.dump({'emb': emb, 'ids': self.ids}, self.emb_path)

def _ensure_nn(self, k=5):
    # build nearest neighbors on embeddings
    if not hasattr(self, 'nn'):
        self.nn = NearestNeighbors(n_neighbors=k, metric='cosine')
        self.nn.fit(self.embeddings)
