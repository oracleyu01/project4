"""
Supabase database client with vector search support
"""
from supabase import create_client
from embeddings import OpenAIEmbeddings
from config import settings
import json


class SupabaseClient:
    def __init__(self):
        self.client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.embeddings = OpenAIEmbeddings()
    
    def search_exact(self, product_name):
        """Search for exact product name match"""
        return self.client.table('laptop_pros_cons').select("*").eq('product_name', product_name).execute()
    
    def search_partial(self, product_name):
        """Search for partial product name match"""
        return self.client.table('laptop_pros_cons').select("*").ilike('product_name', f'%{product_name}%').execute()
    
    def search_similar(self, product_name, threshold=0.7):
        """Search using vector similarity"""
        try:
            # Get embedding for search query
            query_embedding = self.embeddings.get_embedding(product_name)
            if not query_embedding:
                return None
            
            # Get all products with embeddings
            result = self.client.table('laptop_pros_cons').select("*").execute()
            
            similar_products = []
            checked_products = set()
            
            for item in result.data:
                if item['product_name'] in checked_products:
                    continue
                
                if item.get('embedding'):
                    # Calculate similarity
                    embedding = json.loads(item['embedding']) if isinstance(item['embedding'], str) else item['embedding']
                    similarity = self.embeddings.cosine_similarity(query_embedding, embedding)
                    
                    if similarity >= threshold:
                        similar_products.append({
                            'product_name': item['product_name'],
                            'similarity': similarity
                        })
                        checked_products.add(item['product_name'])
            
            # Sort by similarity
            similar_products.sort(key=lambda x: x['similarity'], reverse=True)
            
            # Get top match
            if similar_products:
                best_match = similar_products[0]['product_name']
                return self.search_exact(best_match)
            
            return None
            
        except Exception as e:
            print(f"Error in similarity search: {e}")
            return None
    
    def insert_pros_cons_with_embedding(self, product_name, pros, cons):
        """Insert pros and cons with product embedding"""
        try:
            # Get embedding for product name
            embedding = self.embeddings.get_embedding(product_name)
            
            data = []
            
            for pro in pros:
                data.append({
                    'product_name': product_name,
                    'type': 'pro',
                    'content': pro,
                    'embedding': embedding
                })
            
            for con in cons:
                data.append({
                    'product_name': product_name,
                    'type': 'con',
                    'content': con,
                    'embedding': embedding
                })
            
            if data:
                return self.client.table('laptop_pros_cons').insert(data).execute()
                
        except Exception as e:
            print(f"Error inserting data: {e}")
            return None
