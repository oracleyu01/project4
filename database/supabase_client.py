"""
Supabase database client
"""
from supabase import create_client
#from sentence_transformers import SentenceTransformer
from config import settings


class SupabaseClient:
    def __init__(self):
        self.client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
       # self.model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    
    def search_exact(self, product_name):
        """Search for exact product name match"""
        return self.client.table('laptop_pros_cons').select("*").eq('product_name', product_name).execute()
    
    def search_partial(self, product_name):
        """Search for partial product name match"""
        return self.client.table('laptop_pros_cons').select("*").ilike('product_name', f'%{product_name}%').execute()
    
    def insert_pros_cons(self, product_name, pros, cons):
        """Insert pros and cons data"""
        data = []
        
        for pro in pros:
            data.append({
                'product_name': product_name,
                'type': 'pro',
                'content': pro
            })
        
        for con in cons:
            data.append({
                'product_name': product_name,
                'type': 'con',
                'content': con
            })
        
        if data:
            return self.client.table('laptop_pros_cons').insert(data).execute()
